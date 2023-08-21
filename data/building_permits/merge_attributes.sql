-- Add centroid geometry field
ALTER TABLE ztrax.main
ADD COLUMN centroid GEOMETRY(point, 3310);

-- Generate Centroid from Existing Latitude Longitude Coordinates
UPDATE ztrax.main
SET centroid = ST_TRANSFORM(ST_SETSRID(ST_MAKEPOINT(
    "PropertyAddressLongitude", "PropertyAddressLatitude"), 4326), 3310);

-- Index the Ztrax centroid geometry field
CREATE INDEX IF NOT EXISTS idx_us_main_centroid_idx
ON ztrax.main
USING gist (centroid);

-- Add polygon geometry field to ZTRAX main from SGC Parcel Layer
ALTER TABLE ztrax.main
ADD COLUMN geom GEOMETRY(MULTIPOLYGON, 3310);

-- Assign Polygon Geometry to ztrax records
UPDATE ztrax.main
SET geom = sgc.geom
FROM sgc.ca_parcel_boundaries_2014 AS sgc
WHERE ST_INTERSECTS(centroid, sgc.geom);

-- Generate Polygon Aggregate ZTRAX data
SELECT  A.geom,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY B."YearBuilt") AS "MedianYearBuilt",
        SUM(C."BuildingAreaSqFt") AS "TotalBuildingAreaSqFt",
        ARRAY_AGG(B."PropertyLandUseStndCode") AS "PropertyLandUseStndCodes",
        ARRAY_AGG(A."RowID") AS "RowIDs"
INTO ztrax.megaparcels
FROM ztrax.main AS A
JOIN ztrax.building AS B
    ON A."RowID" = B."RowID"
JOIN ztrax.building_areas AS C
    ON A."RowID" = C."RowID"
GROUP BY A.geom;

-- Add Permit ID Field 
ALTER TABLE ztrax.megaparcels
ADD COLUMN MegaParcelID SERIAL;

-- Assign permits to megaparcels
ALTER TABLE permits.panel_upgrades_geocoded
ADD COLUMN MegaParcelID NUMERIC;

-- Update Each Panel Upgrade Permit with the Associated Megaparcel ID
UPDATE permits.panel_upgrades_geocoded
SET MegaParcelID = B.MegaParcelID
FROM ztrax.megaparcels AS B
WHERE ST_INTERSECTS(centroid, B.geom);

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

-- Add union code
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

-- Add union code
ALTER TABLE permits.sampled_counties
ADD COLUMN union_code BOOL DEFAULT TRUE;

-- Create Sampled Territory as Spatial Union of Sampled Places and Counties
SELECT ST_UNION(A.geometry) AS geometry,
    union_code
INTO permits.sampled_territories
FROM (SELECT geometry, union_code FROM permits.sampled_places 
        UNION
    SELECT geometry, union_code FROM permits.sampled_counties) AS A
GROUP BY A.union_code;
    
-- Add boolean field to megaparcel layer to indicate sampled territories
ALTER TABLE ztrax.megaparcels
ADD COLUMN sampled BOOL DEFAULT FALSE;

-- Add centroid field to megaparcel layer
ALTER TABLE ztrax.megaparcels
ADD COLUMN centroid GEOMETRY(POINT, 3310);

-- Update Centroid Geometries for Megaparcel Layer
UPDATE ztrax.megaparcels
SET centroid = ST_CENTROID(geom);

-- Index sampled territory geometries prior to spatial join
CREATE INDEX IF NOT EXISTS idx_sampled_territories_geometry ON permits.sampled_territories USING GIST(geometry);

-- Index megaparcel centroids prior to spatial join
CREATE INDEX IF NOT EXISTS idx_megaparcels_centroid ON ztrax.megaparcels USING GIST(centroid);

-- Mark Sampled Megaparcels Based Upon Sampled Territory Intersection
UPDATE ztrax.megaparcels
SET sampled = TRUE
FROM permits.sampled_territories AS B
WHERE ST_INTERSECTS(centroid, B.geometry);
