-- Add Permit ID Field
ALTER TABLE corelogic.corelogic_20240126_varchar_megaparcels
ADD COLUMN megaparcelid SERIAL;

-- Index the megaparcel id field
CREATE INDEX IF NOT EXISTS idx_corelogic_20240126_megaparcelid_idx
ON corelogic.corelogic_20240126_varchar_megaparcels (megaparcelid);

-- Assign permits to megaparcels
ALTER TABLE permits.panel_upgrades_geocoded
ADD COLUMN corelogic_20240126_megaparcelid NUMERIC;

-- Update Each Panel Upgrade Permit with the Associated Megaparcel ID
UPDATE permits.panel_upgrades_geocoded AS A
SET corelogic_20240126_megaparcelid = B.megaparcelid
FROM corelogic.corelogic_20240126_varchar_megaparcels AS B
WHERE ST_INTERSECTS(A.centroid, B.geom);

-- Add Centroid Field
SELECT AddGeometryColumn('corelogic','corelogic_20240126_varchar_megaparcels','centroid',3310,'POINT',2);

-- Populate Centroid Field
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET "centroid" = ST_CENTROID("geom");

-- Index megaparcel centroids prior to spatial join
CREATE INDEX IF NOT EXISTS idx_corelogic_20240126_megaparcels_centroid
ON corelogic.corelogic_20240126_varchar_megaparcels USING GIST(centroid);

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
INTO corelogic.corelogic_20240126_varchar_megaparcels_geocoded_geographies
FROM corelogic.corelogic_20240126_varchar_megaparcels AS A
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
CREATE INDEX IF NOT EXISTS idx_gg_corelogic_20240126_megaparcelid_idx
ON corelogic.corelogic_20240126_varchar_megaparcels_geocoded_geographies (megaparcelid);

-- Index sampled territory geometries prior to spatial join
CREATE INDEX IF NOT EXISTS idx_sampled_territories_geometry
ON permits.sampled_territories USING GIST(geometry);

-- Index megaparcel geometry field
CREATE INDEX IF NOT EXISTS idx_corelogic_20240126_megaparcels_geom
ON corelogic.corelogic_20240126_varchar_megaparcels USING GIST(geom);

-- Add boolean field to megaparcel layer to indicate sampled territories
ALTER TABLE corelogic.corelogic_20240126_varchar_megaparcels
ADD COLUMN sampled BOOL DEFAULT FALSE;

-- Mark Sampled Megaparcels Based Upon Sampled Territory Intersection
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET sampled = TRUE
FROM permits.sampled_territories AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Create megaparcel usetype classification field
ALTER TABLE corelogic.corelogic_20240126_varchar_megaparcels
ADD COLUMN usetype TEXT DEFAULT NULL;

-- Single Family is defined strictly here as megaparcels that majorly consist of
-- one of the following property land use stnd codes listed below:
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET usetype = 'single_family'
WHERE   "land use code _ piq" = '100' OR
        "land use code _ piq" = '102' OR
        "land use code _ piq" = '109' OR
        "land use code _ piq" = '135' OR
        "land use code _ piq" = '137' OR
        "land use code _ piq" = '138' OR
        "land use code _ piq" = '148' OR
        "land use code _ piq" = '160' OR
        "land use code _ piq" = '163';

-- Multi Family is defined openly here as megaparcels which majorly consist of
-- one of the following property landuse standard codes:
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET usetype = 'multi_family'
WHERE   "land use code _ piq" = '103' OR
        "land use code _ piq" = '106' OR
        "land use code _ piq" = '115' OR
        "land use code _ piq" = '131' OR
        "land use code _ piq" = '132' OR
        "land use code _ piq" = '133' OR
        "land use code _ piq" = '151' OR
        "land use code _ piq" = '165' OR
        "land use code _ piq" = '450' OR
        "land use code _ piq" = '452';

-- Create As Built Panel Size Field
ALTER TABLE corelogic.corelogic_20240126_varchar_megaparcels
ADD COLUMN panel_size_as_built NUMERIC DEFAULT NULL;

-- Estimate As-Built Panel Size from Vintage Year and Size Combination for Single Family Megaparcels
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET panel_size_as_built = CASE
    -- Pre-1879
    WHEN "year built" <= 1879 THEN 0
    -- 1879-1950
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" <= 1000) THEN 30
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 1000 AND "universal building square feet" <= 2000) THEN 40
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 2000 AND "universal building square feet" <= 3000) THEN 60
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 3000 AND "universal building square feet" <= 4000) THEN 100
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 4000 AND "universal building square feet" <= 5000) THEN 125
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 5000 AND "universal building square feet" <= 8000) THEN 150
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 8000 AND "universal building square feet" <= 10000) THEN 200
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 10000 AND "universal building square feet" <= 20000) THEN 320
    WHEN ("year built" > 1879 AND "year built" <= 1950) AND ("universal building square feet" > 20000 ) THEN 400
    -- 1950-1978
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" <= 1000) THEN 60 -- Update to 60 from 40
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 1000 AND "universal building square feet" <= 2000) THEN 100 -- Update to 100 from 60
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 2000 AND "universal building square feet" <= 3000) THEN 100
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 3000 AND "universal building square feet" <= 4000) THEN 125
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 4000 AND "universal building square feet" <= 5000) THEN 150
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 5000 AND "universal building square feet" <= 8000) THEN 200
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 8000 AND "universal building square feet" <= 10000) THEN 320
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 10000 AND "universal building square feet" <= 20000) THEN 400
    WHEN ("year built" > 1950 AND "year built" <= 1978) AND ("universal building square feet" > 20000 ) THEN 600
    -- 1978-2010
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" <= 1000) THEN 100 -- Update to 100 from 60
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 1000 AND "universal building square feet" <= 2000) THEN 100
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 2000 AND "universal building square feet" <= 3000) THEN 125
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 3000 AND "universal building square feet" <= 4000) THEN 150
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 4000 AND "universal building square feet" <= 5000) THEN 200
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 5000 AND "universal building square feet" <= 8000) THEN 320
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 8000 AND "universal building square feet" <= 10000) THEN 400
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 10000 AND "universal building square feet" <= 20000) THEN 600
    WHEN ("year built" > 1978 AND "year built" <= 2010) AND ("universal building square feet" > 20000 ) THEN 800
    -- Post-2010
    WHEN ("year built" > 2010) AND ("universal building square feet" <= 1000) THEN 200
    WHEN ("year built" > 2010) AND ("universal building square feet" > 1000 AND "universal building square feet" <= 2000) THEN 200
    WHEN ("year built" > 2010) AND ("universal building square feet" > 2000 AND "universal building square feet" <= 3000) THEN 225
    WHEN ("year built" > 2010) AND ("universal building square feet" > 3000 AND "universal building square feet" <= 4000) THEN 320
    WHEN ("year built" > 2010) AND ("universal building square feet" > 4000 AND "universal building square feet" <= 5000) THEN 400
    WHEN ("year built" > 2010) AND ("universal building square feet" > 5000 AND "universal building square feet" <= 8000) THEN 600
    WHEN ("year built" > 2010) AND ("universal building square feet" > 8000 AND "universal building square feet" <= 10000) THEN 800
    WHEN ("year built" > 2010) AND ("universal building square feet" > 10000 AND "universal building square feet" <= 20000) THEN 1000
    WHEN ("year built" > 2010) AND ("universal building square feet" > 20000 ) THEN 1200
END
WHERE usetype = 'single_family';

-- Estimate As-Built Panel Size from Vintage Year for Multi Family Megaparcels
UPDATE corelogic.corelogic_20240126_varchar_megaparcels
SET panel_size_as_built = CASE
    -- Pre-1879
    WHEN "year built" <= 1879 THEN 0
    -- 1879-1950
    WHEN ("year built" > 1879 AND "year built" <= 1950) THEN 40
    -- 1950-1978
    WHEN ("year built" > 1950 AND "year built" <= 1978) THEN 60
    -- 1978-2010
    WHEN ("year built" > 1978 AND "year built" <= 2010) THEN 90
    -- Post-2010
    WHEN ("year built" > 2010) THEN 150
END
WHERE usetype = 'multi_family';
