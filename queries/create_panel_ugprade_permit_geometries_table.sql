-- Create new panel upgrades geographies table
SELECT  id,
        centroid
INTO permits.panel_upgrades_geographies
FROM permits.panel_upgrades;

-- Add receiver attribute fieldss
ALTER TABLE permits.panel_upgrades_geographies
ADD COLUMN COUNTY_NAMELSAD TEXT DEFAULT NULL,
ADD COLUMN COUNTY_NS TEXT DEFAULT NULL,
ADD COLUMN COUNTY_FP TEXT DEFAULT NULL,
ADD COLUMN PLACE_NAMELSAD TEXT DEFAULT NULL,
ADD COLUMN PLACE_NS TEXT DEFAULT NULL,
ADD COLUMN PLACE_FP TEXT DEFAULT NULL,
ADD COLUMN PUMA_NAMELSAD TEXT DEFAULT NULL,
ADD COLUMN PUMA_GEOID TEXT DEFAULT NULL,
ADD COLUMN TRACT_NAMELSAD TEXT DEFAULT NULL,
ADD COLUMN TRACT_GEOID TEXT DEFAULT NULL;

-- Update county level field values on spatial intersection
UPDATE permits.panel_upgrades_geographies
SET county_namelsad = B."NAMELSAD",
    county_ns = B."COUNTYNS",
    county_fp = B."COUNTYFP"
FROM census.acs_ca_2019_county_geom AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Update place level field values on spatial intersection
UPDATE permits.panel_upgrades_geographies
SET place_namelsad = B."NAMELSAD",
    place_ns = B."PLACENS",
    cplace_fp = B."PLACEFP"
FROM census.acs_ca_2019_place_geom AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Update puma level field values on spatial intersection
UPDATE permits.panel_upgrades_geographies
SET puma_namelsad = B."NAMELSAD",
    puma_geoid = B."GEOID10"
    FROM census.acs_ca_2019_puma_geom AS B
WHERE ST_INTERSECTS(centroid, B.geometry);

-- Update tract level field values on spatial intersection
UPDATE permits.panel_upgrades_geographies
SET tract_namelsad = B."NAMELSAD",
    tract_geoid = B."GEOID"
    FROM census.acs_ca_2019_tract_geom AS B
WHERE ST_INTERSECTS(centroid, B.geometry);
