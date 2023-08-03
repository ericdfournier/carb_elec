-- Add Centroid Field for Parcel Attributes
ALTER TABLE ztrax.parcel_attributes ADD COLUMN centroid geometry(Point,3310);

-- Compute Centroids from Parcel Boundaries
UPDATE ztrax.parcel_attributes
SET centroid = ST_CENTROID(geom);

-- Index ZTRAX Parcel Boundaries Prior to Spatial Join
CREATE INDEX IF NOT EXISTS idx_sgc_parcel_attributes_geom ON ztrax.parcel_attributes USING gist (geom);
CREATE INDEX IF NOT EXISTS idx_sgc_parcel_attributes_centroid ON ztrax.parcel_attributes USING gist (centroid);

-- Generate Geocoded Geographies Table
SELECT DISTINCT ON (A.id)
        A.id,
        B."NAMELSAD" AS place_name,
        C."NAMELSAD" AS county_name,
        D.dac AS dac,
        D.lowincome AS low_income,
        D.nondesignated AS non_designated,
        D.bufferlowincome AS buffer_low_income,
        D.bufferlih AS bufferlih,
        E."GEOID" AS tract_geoid_2019,
        F."rowid" AS ztrax_rowid,
        F."geom" AS geom,
        F."centroid" AS centroid
INTO permits.panel_upgrades_geocoded_geographies
FROM permits.panel_upgrades_geocoded AS A
JOIN census.acs_ca_2019_place_geom AS B
    ON ST_INTERSECTS(A.centroid, B.geometry)
JOIN census.acs_ca_2019_county_geom AS C
    ON ST_INTERSECTS(A.centroid, C.geometry)
JOIN carb.priority_populations_ces4 AS D
    ON ST_INTERSECTS(A.centroid, D.geom)
JOIN census.acs_ca_2019_tr_geom AS E
    ON ST_INTERSECTS(A.centroid, E.geometry)
JOIN ztrax.parcel_attributes AS F
    ON ST_INTERSECTS(A.centroid, F.geom);

-- TODO: There is an issue with overlapping boundaries for the parcel attribute intersections
-- Need to think about how to assign the right parcel attributes to the centroid for each permit
-- This probably requires generating a "megaparcel" like layer from the ztrax attributes for the spatial join

-- Enumerate Sampled Places
SELECT *
INTO permits.sampled_places 
FROM census.acs_ca_2019_place_geom
WHERE "NAMELSAD" IN (
    'Alameda city',
    'Anaheim city',
    'Ceres city',
    'Clovis city',
    'Corona city',
    'Elk Grove city',
    'Fairfield city',
    'Fresno city',
    'Garden Grove city',
    'Hanford city',
    'Los Angeles city',
    'Los Gatos town',
    'Moreno Valley city',
    'Oakland city',
    'Oceanside city',
    'Ojai city',
    'Pasadena city',
    'Paso Robles city',
    'Pleasanton city',
    'Rancho Cucamonga city',
    'Redding city',
    'Richmond city',
    'Riverside city',
    'Roseville city',
    'San Diego city',
    'San Mateo city',
    'San Rafael city',
    'Santa Ana city',
    'Santa Clara city',
    'Santa Monica city',
    'Santa Rosa city',
    'Stockton city',
    'Victorville city',
    'West Sacramento city',
    'Yorba Linda city',
    'Yolo CDP',
    'Yuba City city',
    'San Francisco city');

ALTER TABLE permits.sampled_places
ADD COLUMN union_code BOOL DEFAULT TRUE;

-- Enumerate Sampled Counties
SELECT * 
INTO permits.sampled_counties
FROM census.acs_ca_2019_county_geom
WHERE "NAMELSAD" IN (
    'Contra Costa County',
    'El Dorado County',
    'Humboldt County',
    'Kern County',
    'Lake County',
    'Marin County',
    'Nevada County',
    'Placer County',
    'Riverside County',
    'Sacramento County',
    'San Bernardino County',
    'San Francisco County',
    'San Mateo County',
    'Tulare County',
    'Yolo County');

ALTER TABLE permits.sampled_counties
ADD COLUMN union_code BOOL DEFAULT TRUE;

-- Select Out Sampled Territories
SELECT ST_UNION(territory.geometry) AS geometry
INTO permits.sampled_territory
FROM (  SELECT "NAMELSAD", union_code, geometry FROM permits.sampled_counties 
            UNION
        SELECT "NAMELSAD", union_code, geometry FROM permits.sampled_places) AS territory
GROUP BY union_code;

-- Index Sample Territories Prior to Spatial Join
CREATE INDEX IF NOT EXISTS idx_sgc_sampled_territory_geom ON permits.sampled_territory USING gist (geometry);

-- Select ZTRAX Parcels That in Sampled Territories 
SELECT  A.*
INTO    permits.sampled_territory_all_parcels
FROM    ztrax.parcel_attributes AS A
JOIN permits.sampled_territory AS B
    ON ST_INTERSECTS(A.centroid, B.geometry);

SELECT COUNT(*)
FROM permits.panel_upgrades_geocoded_geographies;