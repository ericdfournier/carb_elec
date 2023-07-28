-- Index the shoreline geometry linestring prior to runnning calculation
CREATE INDEX idx_us_medium_shoreline_geom_idx IF NOT EXISTS ON noaa.us_medium_shoreline USING gist (geom);

-- Compute the distance to shore from each parcel centroid
SELECT DISTINCT rowid,
    (SELECT FLOOR(ST_Distance(pt.centroid, ln.geom))::INTEGER
        FROM   noaa.us_medium_shoreline AS ln
        ORDER BY
            pt.centroid <-> ln.geom
        LIMIT  1) AS shoreline_distance_m
INTO ztrax.distance
FROM ztrax.parcel_attributes AS pt;

-- Compute the elevation of each parcel centroid using a cross lateral join
SELECT parcels.rowid,
       elevation.elevation_m
INTO    ztrax.elevation
FROM    ztrax.parcel_attributes AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS elevation_m
        FROM srtm.ca_elevation
        WHERE ST_Intersects(parcels.centroid, rast)) AS elevation;

-- Compute the slope at each parcel centroid using a cross lateral join
SELECT parcels.rowid,
       slope.slope_pct
INTO    ztrax.slope
FROM    ztrax.parcel_attributes AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS slope_pct
        FROM srtm.ca_slope
        WHERE ST_Intersects(parcels.centroid, rast)) AS slope;
