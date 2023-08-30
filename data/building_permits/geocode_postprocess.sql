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

-- Join County, Place, and Other Attributes Based Upon Centroid Intersections
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
        F."megaparcelid" AS megaparcelid
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
JOIN ztrax.megaparcels AS F
    ON ST_INTERSECTS(A.centroid, F.geom);

-- Index Geocoded Panel Upgrade table on Megaparcel ID Field
CREATE INDEX IF NOT EXISTS idx_megaparcelid_idx
ON permits.panel_upgrades_geocoded (megaparcelid);
