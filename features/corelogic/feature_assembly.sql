-- NOTE: The block below needs to be run on the DB server...
-- Generate Polygon Aggregated CoreLogic data as Megaparcels
SELECT  parcels."geom" AS geom,
        MODE() WITHIN GROUP (ORDER BY parcels.centroid) AS "centroid",
        ARRAY_AGG(parcels."clip") AS "RowIDs",
        ARRAY_AGG(parcels."land use code _ piq") AS "PropertyLandUseStndCodes",
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY parcels."year built _ piq") AS "YearBuilt",
        SUM(parcels."number of buildings") AS "TotalNoOfBuildings",
        MODE() WITHIN GROUP(ORDER BY parcels."land square footage _ piq") AS "LotSizeSquareFeet",
        SUM(parcels."universal building square feet") AS "TotalBuildingAreaSqFt",
        MODE() WITHIN GROUP (ORDER BY parcels."number of units") AS "TotalNoOfUnits",
        SUM(parcels."bedrooms") AS "TotalNoOfBedrooms",
        SUM(parcels."assessed land value"::NUMERIC) AS "TotalLandAssessedValue",
        SUM(parcels."assessed improvement value"::NUMERIC) AS "TotalImprovementAssessedValue",
        MODE() WITHIN GROUP(ORDER BY parcels."heating type code") AS "HeatingTypeorSystemStndCode",
        MODE() WITHIN GROUP(ORDER BY parcels."air conditioning code") AS "AirConditioningTypeorSystemStndCode"
INTO projects.carb_megaparcels
FROM corelogic.corelogic_20231228 AS parcels
WHERE type_code IN ('CEN','FIP') AND
    ST_GeometryType("geom") IN ('ST_Polygon', 'ST_MultiPolygon')
GROUP BY parcels."geom";

-- NOTE: Switching to local PostGRES server from here on out
-- Add Permit ID Field
ALTER TABLE corelogic.megaparcels
ADD COLUMN megaparcelid SERIAL;

-- Index the megaparcel id field
CREATE INDEX IF NOT EXISTS idx_megaparcelid_idx
ON corelogic.megaparcels (megaparcelid);

-- Assign permits to megaparcels
ALTER TABLE permits.panel_upgrades_geocoded
ADD COLUMN corelogic_megaparcelid NUMERIC;

-- Update Each Panel Upgrade Permit with the Associated Megaparcel ID
UPDATE permits.panel_upgrades_geocoded AS A
SET corelogic_megaparcelid = B.megaparcelid
FROM corelogic.megaparcels AS B
WHERE ST_INTERSECTS(A.centroid, B.geom);

-- Add boolean field to megaparcel layer to indicate sampled territories
ALTER TABLE corelogic.megaparcels
ADD COLUMN sampled BOOL DEFAULT FALSE;

-- Index megaparcel centroids prior to spatial join
CREATE INDEX IF NOT EXISTS idx_megaparcels_centroid
ON corelogic.megaparcels USING GIST(centroid);

-- Join County, Place, and Other Attributes Based Upon Megaparcel Centroid Intersections
SELECT DISTINCT ON (A.megaparcelid)
        A.megaparcelid,
        B."NAMELSAD" AS place_name,
        C."NAMELSAD" AS county_name,
        D.dac AS dac,
        D.lowincome AS low_income,
        D.nondesignated AS non_designated,
        D.bufferlowincome AS buffer_low_income,
        D.bufferlih AS bufferlih,
        E."GEOID" AS tract_geoid_2019,
        G."name" AS air_basin,
        H."name" AS air_district,
        I."coabdis_id" AS county_air_basin_district_id
INTO corelogic.megaparcels_geocoded_geographies
FROM corelogic.megaparcels AS A
JOIN census.acs_ca_2019_place_geom AS B
    ON ST_INTERSECTS(A.centroid, B.geometry)
JOIN census.acs_ca_2019_county_geom AS C
    ON ST_INTERSECTS(A.centroid, C.geometry)
JOIN carb.priority_populations_ces4 AS D
    ON ST_INTERSECTS(A.centroid, D.geom)
JOIN census.acs_ca_2019_tr_geom AS E
    ON ST_INTERSECTS(A.centroid, E.geometry)
JOIN carb.ca_air_basins AS G
    ON ST_INTERSECTS(A.centroid, G.geom)
JOIN carb.ca_air_districts AS H
    ON ST_INTERSECTS(A.centroid, H.geom)
JOIN carb.ca_county_air_basin_districts AS I
    ON ST_INTERSECTS(A.centroid, I.geom);

-- Index the megaparcel id field
CREATE INDEX IF NOT EXISTS idx_gg_megaparcelid_idx
ON corelogic.megaparcels_geocoded_geographies (megaparcelid);

-- Index sampled territory geometries prior to spatial join
CREATE INDEX IF NOT EXISTS idx_sampled_territories_geometry
ON permits.sampled_territories USING GIST(geometry);

-- Index megaparcel geometry field
CREATE INDEX IF NOT EXISTS idx_megaparcels_geom
ON corelogic.megaparcels USING GIST(geom);

-- Mark Sampled Megaparcels Based Upon Sampled Territory Intersection
UPDATE corelogic.megaparcels
SET sampled = TRUE
FROM permits.sampled_territories AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Create megaparcel usetype classification field
ALTER TABLE corelogic.megaparcels
ADD COLUMN usetype TEXT DEFAULT NULL;

-- Single Family is defined strictly here as megaparcels that consist of a
-- records with the property land use stnd codes as listed below:
UPDATE corelogic.megaparcels
SET usetype = 'single_family'
WHERE   "PropertyLandUseStndCodes" = ARRAY[100] OR
        "PropertyLandUseStndCodes" = ARRAY[102] OR
        "PropertyLandUseStndCodes" = ARRAY[109] OR
        "PropertyLandUseStndCodes" = ARRAY[135] OR
        "PropertyLandUseStndCodes" = ARRAY[137] OR
        "PropertyLandUseStndCodes" = ARRAY[138] OR
        "PropertyLandUseStndCodes" = ARRAY[148] OR
        "PropertyLandUseStndCodes" = ARRAY[160] OR
        "PropertyLandUseStndCodes" = ARRAY[163];

-- Multi Family is defined openly here as megaparcels that at least contain
-- one of the following property landuse standard codes:
UPDATE corelogic.megaparcels
SET usetype = 'multi_family'
WHERE   "PropertyLandUseStndCodes" @> ARRAY[103] OR
        "PropertyLandUseStndCodes" @> ARRAY[106] OR
        "PropertyLandUseStndCodes" @> ARRAY[131] OR
        "PropertyLandUseStndCodes" @> ARRAY[132] OR
        "PropertyLandUseStndCodes" @> ARRAY[133];

-- Create As Built Panel Size Field
ALTER TABLE corelogic.megaparcels
ADD COLUMN panel_size_as_built NUMERIC DEFAULT NULL;

-- Estimate As-Built Panel Size from Vintage Year and Size Combination for Single Family Megaparcels
UPDATE corelogic.megaparcels
SET panel_size_as_built = CASE
    -- Pre-1879
    WHEN "YearBuilt" <= 1879 THEN 0
    -- 1879-1950
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 30
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 40
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 60
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 100
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 125
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 150
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 200
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 320
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 400
    -- 1950-1978
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 60 -- Update to 60 from 40
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 100 -- Update to 100 from 60
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 100
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 125
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 150
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 200
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 320
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 400
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 600
    -- 1978-2010
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 100 -- Update to 100 from 60
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 100
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 125
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 150
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 200
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 320
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 400
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 600
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 800
    -- Post-2010
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 200
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 200
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 225
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 320
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 400
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 600
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 800
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 1000
    WHEN ("YearBuilt" > 2010) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 1200
END
WHERE usetype = 'single_family';

-- Estimate As-Built Panel Size from Vintage Year for Multi Family Megaparcels
UPDATE corelogic.megaparcels
SET panel_size_as_built = CASE
    -- Pre-1879
    WHEN "YearBuilt" <= 1879 THEN 0
    -- 1879-1950
    WHEN ("YearBuilt" > 1879 AND "YearBuilt" <= 1950) THEN 40
    -- 1950-1978
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) THEN 60
    -- 1978-2010
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) THEN 90
    -- Post-2010
    WHEN ("YearBuilt" > 2010) THEN 150
END
WHERE usetype = 'multi_family';
