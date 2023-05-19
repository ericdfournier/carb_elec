-- Load extensions
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "intarray";

-- Create array intersction function
CREATE FUNCTION ARRAY_INTERSECT(anyarray, anyarray)
  RETURNS anyarray
  language sql
as $FUNCTION$
    SELECT ARRAY(
        SELECT UNNEST($1)
        INTERSECT
        SELECT UNNEST($2)
    );
$FUNCTION$;

-- Drop unnecessary columns.
alter table permits.combined
    drop ogc_fid,
    drop field_1;

-- Add column for centroid in NAD83 / California Albers.
alter table permits.combined
    add centroid geometry(POINT, 3310);

-- Set centroid values, ignore those outside of WGS84 bounds.
update permits.combined
    set centroid = ST_Transform(centroid_4326, 3310)
    where
        ST_X(centroid_4326) >= -180
        and ST_X(centroid_4326) <= 180
        and ST_Y(centroid_4326) >= -90
        and ST_Y(centroid_4326) <= 90;

-- Create spatial index on centroid.
create index on permits.combined using gist (centroid);

-- Add UUID field with non-null constraints
ALTER TABLE permits.combined
ADD COLUMN id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY;

-- Create index on vector based representation of the project description field
CREATE INDEX IF NOT EXISTS permits_description_search_idx
ON permits.combined
USING GIN(to_tsvector('english', project_description));

-- Test selection based upon the a "panel" keyword match
SELECT
    id,
    project_description,
    rank_description,
    similarity,
    regexp_matches(project_description, '[0-9]+\.?[0-9]*')::NUMERIC[] AS panel_upgrade_size
INTO permits.panel_search_results
FROM
    permits.combined,
    to_tsvector(project_description) document,
    to_tsquery('panel | load & center | service & panel') query,
    NULLIF(ts_rank(to_tsvector(project_description), query), 0) rank_description,
    SIMILARITY('panel | load center | service panel', project_description) similarity
WHERE query @@ document AND similarity > 0
ORDER BY rank_description, similarity DESC NULLS LAST;

-- Infer Sub Panel
ALTER TABLE permits.panel_search_results
ADD COLUMN sub_panel BOOL DEFAULT FALSE,
ADD COLUMN upgraded_panel_size INT DEFAULT NULL;

UPDATE permits.panel_search_results
SET sub_panel = TRUE
WHERE to_tsquery('sub') @@ to_tsvector(project_description);

-- Update Valid Panel Size Ratings
UPDATE permits.panel_search_results
SET panel_upgrade_size = (SELECT ARRAY_INTERSECT(panel_upgrade_size,
    ARRAY[  15,
            20,
            30,
            40,
            50,
            60,
            70,
            100,
            125,
            150,
            175,
            200,
            225,
            250,
            320,
            400,
            600,
            800,
            1000,
            1200,
            1400,
            1600,
            1800,
            2000]::NUMERIC[]));

-- Test selection based upon the a "solar" keyword match
SELECT
    id,
    project_description,
    rank_description,
    similarity
INTO permits.solar_search_results
FROM
    permits.combined,
    to_tsvector(project_description) document,
    to_tsquery('solar | pv | photovoltaic | array') query,
    NULLIF(ts_rank(to_tsvector(project_description), query), 0) rank_description,
    SIMILARITY('solar | pv | photovoltaic | array', project_description) similarity
WHERE query @@ document AND similarity > 0
ORDER BY rank_description, similarity DESC NULLS LAST;

-- Test selection based upon the "heat-pump" keyword match with additional exclusions
SELECT
    id,
    project_description,
    rank_description,
    similarity
INTO permits.heat_pump_search_results
FROM
    permits.combined,
    to_tsvector(project_description) document,
    to_tsquery('heat & pump | heat-pump | heatpump | mini & split | mini-split | minisplit') query,
    NULLIF(ts_rank(to_tsvector(project_description), query), 0) rank_description,
    SIMILARITY('heat pump | heat-pump | heatpump | mini split | mini-split | minisplit', project_description) similarity
WHERE query @@ DOCUMENT AND
    similarity > 0 AND
    project_description !~* 'water' AND
    project_description !~* 'heater' AND
    project_description !~* 'sump'
ORDER BY rank_description, similarity DESC NULLS LAST;

-- Test selection based upon the "ev charger" keyword match
SELECT
    id,
    project_description,
    rank_description,
    similarity
INTO permits.ev_charger_search_results
FROM
    permits.combined,
    to_tsvector(project_description) document,
    to_tsquery('electric & vehicle | ev | charger') query,
    NULLIF(ts_rank(to_tsvector(project_description), query), 0) rank_description,
    SIMILARITY('electric vehicle | ev | charger', project_description) similarity
WHERE query @@ document AND
    similarity > 0 AND
    project_description !~* 'water' AND
    project_description !~* 'heater'
ORDER BY rank_description, similarity DESC NULLS LAST;

-- Test selection based upon the "battery" keyword match
SELECT
    id,
    project_description,
    rank_description,
    similarity
INTO permits.battery_search_results
FROM
    permits.combined,
    to_tsvector(project_description) document,
    to_tsquery('power & wall | powerwall | batteries | battery | energy & storage') query,
    NULLIF(ts_rank(to_tsvector(project_description), query), 0) rank_description,
    SIMILARITY('power wall | powerwall | batteries | battery | energy storage', project_description) similarity
WHERE query @@ document AND
    similarity > 0
ORDER BY rank_description, similarity DESC NULLS LAST;

-- Create Boolean Fields For Panel Upgrade Triggers

ALTER TABLE permits.combined
ADD COLUMN solar_pv_system BOOL DEFAULT FALSE,
ADD COLUMN battery_storage_system BOOL DEFAULT FALSE,
ADD COLUMN ev_charger BOOL DEFAULT FALSE,
ADD COLUMN heat_pump BOOL DEFAULT FALSE,
ADD COLUMN main_panel_upgrade BOOL DEFAULT FALSE,
ADD COLUMN sub_panel_upgrade BOOL DEFAULT FALSE,
ADD COLUMN upgraded_panel_size NUMERIC DEFAULT NULL;

-- Update Trigger Boolean Values

UPDATE permits.combined AS A
SET solar_pv_system = TRUE
FROM permits.solar_search_results AS B
WHERE A."id" = B."id";

UPDATE permits.combined AS A
SET battery_storage_system = TRUE
FROM permits.battery_search_results AS B
WHERE A."id" = B."id";

UPDATE permits.combined AS A
SET ev_charger = TRUE
FROM permits.ev_charger_search_results AS B
WHERE A."id" = B."id";

UPDATE permits.combined AS A
SET heat_pump = TRUE
FROM permits.heat_pump_search_results AS B
WHERE A."id" = B."id";

UPDATE permits.combined AS A
SET main_panel_upgrade = TRUE
FROM permits.panel_search_results AS B
WHERE A."id" = B."id" AND
    B.sub_panel = FALSE;

UPDATE permits.combined AS A
SET sub_panel_upgrade = TRUE
FROM permits.panel_search_results AS B
WHERE A."id" = B."id" AND
    B.sub_panel = TRUE;

UPDATE permits.combined AS A
SET upgraded_panel_size = B.panel_upgrade_size[1] -- Might want to think about choosing the largest matching panel size here (instead of the first) - to account for cases where the to/from sizes are both mentioned in the description. Could cast the numeric array's to int and use the intarray package operators for this...
FROM permits.panel_search_results AS B
WHERE A."id" = B."id";

SELECT *
INTO permits.panel_upgrades
FROM permits.combined
WHERE   solar_pv_system = TRUE OR
        main_panel_upgrade = TRUE OR
        sub_panel_upgrade = TRUE OR
        heat_pump = TRUE OR
        ev_charger = TRUE OR
        battery_storage_system = TRUE;

ALTER TABLE permits.panel_upgrades
ADD COLUMN valid_centroid BOOL DEFAULT FALSE;

UPDATE permits.panel_upgrades
SET valid_centroid = TRUE
FROM census.acs_ca_2019_county_geom AS B
WHERE ST_INTERSECTS(centroid, geometry);

DROP TABLE IF EXISTS permits.battery_search_results;
DROP TABLE IF EXISTS permits.panel_search_results;
DROP TABLE IF EXISTS permits.ev_charger_search_results;
DROP TABLE IF EXISTS permits.solar_search_results;
DROP TABLE IF EXISTS permits.heat_pump_search_results;
