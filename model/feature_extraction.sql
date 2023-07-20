-- Index the shoreline geometry linestring prior to runnning calculation
CREATE INDEX idx_us_medium_shoreline_geom_idx IF NOT EXISTS ON noaa.us_medium_shoreline USING gist (geom);

-- Compute the distance to shore for all ztrax parcels
SELECT DISTINCT rowid,
    (SELECT ST_Distance(pt.centroid, ln.geom)
    FROM   noaa.us_medium_shoreline AS ln
    ORDER BY
        pt.centroid <-> ln.geom
    LIMIT  1) AS coast_dist_m
INTO ztrax.physical_attributes
FROM ztrax.parcel_attributes AS pt;

-- Compute the neighborhood window mean elevation for all ztrax parcels
