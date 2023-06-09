-- Coalesce Geocoding Output Centroids
SELECT  A.id,
        A.permit_number,
        A.permit_class,
        A.permit_type,
        A.estimated_cost,
        A.applied_date,
        A.issued_date,
        A.finaled_date,
        A.solar_pv_system,
        A.battery_storage_system,
        A.ev_charger,
        A.heat_pump,
        A.main_panel_upgrade,
        A.sub_panel_upgrade,
        A.upgraded_panel_size,
        A.parcel_number,
        A.address,
        A.query_address,
        B.address AS match_address,
        COALESCE(A.centroid, B.centroid) AS centroid
INTO permits.panel_upgrades_geocoded
FROM permits.panel_upgrades AS A
LEFT JOIN permits.panel_upgrades_geocode_arcgis AS B
    ON A.id::TEXT = B.id;

-- Create Spatial Index on Coalesced Centroid Fields
CREATE INDEX idx_centroid_panel_upgrades_geocode ON permits.panel_upgrades_geocoded USING gist (centroid);

-- Delete In-Valid Records Based Upon Geographic Intersection
DELETE FROM permits.panel_upgrades_geocoded AS A
USING (SELECT ST_UNION(geometry) AS geometry FROM census.acs_ca_2019_county_geom) AS B
WHERE NOT ST_INTERSECTS(A.centroid, B.geometry) OR
    ST_ISEMPTY(A.centroid);
