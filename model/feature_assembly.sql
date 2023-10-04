-- Add centroid geometry field
ALTER TABLE ztrax.main
ADD COLUMN centroid GEOMETRY(point, 3310);

-- Generate Centroid from Existing Latitude Longitude Coordinates
UPDATE ztrax.main
SET centroid = ST_TRANSFORM(ST_SETSRID(ST_MAKEPOINT(
    "PropertyAddressLongitude", "PropertyAddressLatitude"), 4326), 3310);

-- Index the Ztrax centroid geometry field
CREATE INDEX IF NOT EXISTS idx_us_main_centroid_idx
ON ztrax.main USING gist (centroid);

-- Add polygon geometry field to ZTRAX main from SGC Parcel Layer
ALTER TABLE ztrax.main
ADD COLUMN geom GEOMETRY(MULTIPOLYGON, 3310);

-- Assign Polygon Geometries to Ztrax records from SGC data
UPDATE ztrax.main
SET geom = sgc.geom
FROM (SELECT DISTINCT geom FROM
        sgc.ca_parcel_boundaries_2014) AS sgc
WHERE ST_INTERSECTS(centroid, sgc.geom);

-- Generate Polygon Aggregated ZTRAX data as Megaparcels
SELECT  main.geom,
        ARRAY_AGG(main."RowID") AS "RowIDs",
        ARRAY_AGG(building."PropertyLandUseStndCode") AS "PropertyLandUseStndCodes",
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY building."YearBuilt") AS "YearBuilt",
        SUM(main."NoOfBuildings") AS "TotalNoOfBuildings",
        MODE() WITHIN GROUP(ORDER BY main."LotSizeSquareFeet") AS "LotSizeSquareFeet",
        SUM(areas."BuildingAreaSqFt") AS "TotalBuildingAreaSqFt",
        SUM(building."NoOfUnits") AS "TotalNoOfUnits",
        SUM(building."TotalBedrooms") AS "TotalNoOfBedrooms",
        SUM(value."LandAssessedValue"::NUMERIC) AS "TotalLandAssessedValue",
        SUM(value."ImprovementAssessedValue"::NUMERIC) AS "TotalImprovementAssessedValue",
        MODE() WITHIN GROUP(ORDER BY building."HeatingTypeorSystemStndCode") AS "HeatingTypeorSystemStndCode",
        MODE() WITHIN GROUP(ORDER BY building."AirConditioningTypeorSystemStndCode") AS "AirConditioningTypeorSystemStndCode"
INTO ztrax.megaparcels
FROM ztrax.main AS main
JOIN ztrax.building AS building
    ON main."RowID" = building."RowID"
JOIN ztrax.building_areas AS areas
    ON main."RowID" = areas."RowID"
JOIN ztrax.value AS value
    ON main."RowID" = value."RowID"
GROUP BY main.geom;

-- Add Permit ID Field
ALTER TABLE ztrax.megaparcels
ADD COLUMN MegaParcelID SERIAL;

-- Index the megaparcel id field
CREATE INDEX IF NOT EXISTS idx_megaparcelid_idx
ON ztrax.megaparcels (megaparcelid);

-- Assign permits to megaparcels
ALTER TABLE permits.panel_upgrades_geocoded
ADD COLUMN MegaParcelID NUMERIC;

-- Update Each Panel Upgrade Permit with the Associated Megaparcel ID
UPDATE permits.panel_upgrades_geocoded
SET MegaParcelID = B.MegaParcelID
FROM ztrax.megaparcels AS B
WHERE ST_INTERSECTS(centroid, B.geom);

-- Add boolean field to megaparcel layer to indicate sampled territories
ALTER TABLE ztrax.megaparcels
ADD COLUMN sampled BOOL DEFAULT FALSE;

-- Add centroid field to megaparcel layer
ALTER TABLE ztrax.megaparcels
ADD COLUMN centroid GEOMETRY(POINT, 3310);

-- Update Centroid Geometries for Megaparcel Layer
UPDATE ztrax.megaparcels
SET centroid = ST_CENTROID(geom);

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
INTO ztrax.megaparcels_geocoded_geographies
FROM ztrax.megaparcels AS A
JOIN census.acs_ca_2019_place_geom AS B
    ON ST_INTERSECTS(A.centroid, B.geometry)
JOIN census.acs_ca_2019_county_geom AS C
    ON ST_INTERSECTS(A.centroid, C.geometry)
JOIN carb.priority_populations_ces4 AS D
    ON ST_INTERSECTS(A.centroid, D.geom)
JOIN census.acs_ca_2019_tr_geom AS E
    ON ST_INTERSECTS(A.centroid, E.geometry)
JOIN ztrax.megaparcels AS F
    ON ST_INTERSECTS(A.centroid, F.geom)
JOIN carb.ca_air_basins AS G
    ON ST_INTERSECTS(A.centroid, G.geom)
JOIN carb.ca_air_districts AS H
    ON ST_INTERSECTS(A.centroid, H.geom)
JOIN carb.ca_county_air_basin_districts AS I
    ON ST_INTERSECTS(A.centroid, I.geom);

-- Index the megaparcel id field
CREATE INDEX IF NOT EXISTS idx_gg_megaparcelid_idx
ON ztrax.megaparcels_geocoded_geographies (megaparcelid);

-- Index sampled territory geometries prior to spatial join
CREATE INDEX IF NOT EXISTS idx_sampled_territories_geometry ON permits.sampled_territories USING GIST(geometry);

-- Index megaparcel centroids prior to spatial join
CREATE INDEX IF NOT EXISTS idx_megaparcels_centroid ON ztrax.megaparcels USING GIST(centroid);

-- Index megaparcel geometry field
CREATE INDEX IF NOT EXISTS idx_megaparcels_geom ON ztrax.megaparcels USING GIST(geom);

-- Mark Sampled Megaparcels Based Upon Sampled Territory Intersection
UPDATE ztrax.megaparcels
SET sampled = TRUE
FROM permits.sampled_territories AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Create megaparcel usetype classification field
ALTER TABLE ztrax.megaparcels
ADD COLUMN usetype TEXT DEFAULT NULL;

-- Single Family is defined strictly here as megaparcels that consist of a single parcel number
-- with the property land use stnd code is either 'RR101' or 'RI101'.
-- There are a total of 5,967,714 of these in the dataset.
UPDATE ztrax.megaparcels
SET usetype = 'single_family'
WHERE   "PropertyLandUseStndCodes" = ARRAY['RR101'] OR
        "PropertyLandUseStndCodes" = ARRAY['RR999']

-- Multi Family is defined openly here as megaparcels that at least contain one of the following property
-- landuse standard codes that do not correspond to 'RR101' or 'RI101'.
-- There are a total of 995,411 of these in the dataset.
UPDATE ztrax.megaparcels
SET usetype = 'multi_family'
WHERE   "PropertyLandUseStndCodes" @> ARRAY['RI000'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI101'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI102'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI103'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI104'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI105'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI106'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI107'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI108'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI109'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI110'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI111'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI112'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI113'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RI114'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR000'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR102'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR103'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR104'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR105'] OR
        "PropertyLandUseStndCodes" @> ARRAY['RR106'];

-- Create As Built Panel Size Field
ALTER TABLE ztrax.megaparcels
ADD COLUMN panel_size_as_built NUMERIC DEFAULT NULL;

-- Estimate As-Built Panel Size from Vintage Year and Size Combination for Single Family Megaparcels
UPDATE ztrax.megaparcels
SET panel_size_as_built = CASE
    -- Pre-1883
    WHEN "YearBuilt" <= 1883 THEN 0
    -- 1883-1950
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 30
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 40
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 60
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 100
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 125
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 150
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 200
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 320
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 400
    -- 1950-1978
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 40
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 1000 AND "TotalBuildingAreaSqFt" <= 2000) THEN 60
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 2000 AND "TotalBuildingAreaSqFt" <= 3000) THEN 100
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 3000 AND "TotalBuildingAreaSqFt" <= 4000) THEN 125
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 4000 AND "TotalBuildingAreaSqFt" <= 5000) THEN 150
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 5000 AND "TotalBuildingAreaSqFt" <= 8000) THEN 200
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 8000 AND "TotalBuildingAreaSqFt" <= 10000) THEN 320
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 10000 AND "TotalBuildingAreaSqFt" <= 20000) THEN 400
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) AND ("TotalBuildingAreaSqFt" > 20000 ) THEN 600
    -- 1978-2010
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) AND ("TotalBuildingAreaSqFt" <= 1000) THEN 60
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
UPDATE ztrax.megaparcels
SET panel_size_as_built = CASE
    -- Pre-1883
    WHEN "YearBuilt" <= 1883 THEN 0
    -- 1883-1950
    WHEN ("YearBuilt" > 1883 AND "YearBuilt" <= 1950) THEN 40
    -- 1950-1978
    WHEN ("YearBuilt" > 1950 AND "YearBuilt" <= 1978) THEN 60
    -- 1978-2010
    WHEN ("YearBuilt" > 1978 AND "YearBuilt" <= 2010) THEN 90
    -- Post-2010
    WHEN ("YearBuilt" > 2010) THEN 150
END
WHERE usetype = 'multi_family';
