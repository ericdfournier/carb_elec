-- Index the shoreline geometry linestring prior to runnning calculation
CREATE INDEX IF NOT EXISTS idx_us_medium_shoreline_geom_idx ON noaa.us_medium_shoreline USING gist (geom);

-- Compute the distance to shore from each parcel centroid
SELECT DISTINCT parcels.rowid,
    (SELECT FLOOR(ST_Distance(parcels.centroid, shoreline.geom))::INTEGER
        FROM   noaa.us_medium_shoreline AS shoreline
        ORDER BY
            parcels.centroid <-> shoreline.geom
        LIMIT  1) AS shoreline_distance_m
INTO ztrax.distance
FROM ztrax.parcel_attributes AS parcels;

-- Compute the elevation of each parcel centroid using a cross lateral join
SELECT DISTINCT parcels.rowid,
       elevation.elevation_m
INTO    ztrax.elevation
FROM    ztrax.parcel_attributes AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS elevation_m
        FROM srtm.ca_elevation
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS elevation;

-- Compute the slope at each parcel centroid using a cross lateral join
SELECT DISTINCT parcels.rowid,
       slope.slope_pct
INTO    ztrax.slope
FROM    ztrax.parcel_attributes AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS slope_pct
        FROM srtm.ca_slope
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS slope;

-- Compute the aspect at each parcel centroid using a cross lateral join
SELECT DISTINCT parcels.rowid,
        aspect.aspect_deg
INTO ztrax.aspect
FROM ztrax.parcel_attributes AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_VALUE(rast, parcels.centroid))::INTEGER AS aspect_deg
        FROM srtm.ca_aspect
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS aspect;

-- Assemble unified physical attributes feature table and delete intermediate tables
SELECT  distance.rowid,
        distance.shoreline_distance_m,
        elevation.elevation_m,
        slope.slope_pct,
        aspect.aspect_deg
INTO ztrax.physical_attributes
FROM ztrax.distance AS distance 
JOIN ztrax.elevation AS elevation
    ON distance.rowid = elevation.rowid
JOIN ztrax.slope AS slope
    ON elevation.rowid = slope.rowid
JOIN ztrax.aspect AS aspect
    ON slope.rowid = aspect.rowid;
