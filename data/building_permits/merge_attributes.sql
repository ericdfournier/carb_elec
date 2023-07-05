-- Index ZTRAX Parcel Boundaries Prior to Spatial Join
CREATE INDEX IF NOT EXISTS idx_sgc_parcel_attributes_geom ON ztrax.parcel_attributes USING gist (geom);

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
        F."rowid" AS ztrax_rowid
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

-- Test Final Assembly Join
SELECT A.*,
       C.*
INTO permits.panel_upgrades_final
FROM permits.panel_upgrades_geocoded AS A
JOIN permits.panel_upgrades_geocoded_geographies AS B
    ON A.id = B.id
JOIN ztrax.parcel_attributes AS C
    ON B.ztrax_rowid = C.rowid;

-- Select Out Sampled Territories
SELECT A.*
INTO permits.permit_sample_territories
FROM census.acs_ca_2019_place_geom AS A
JOIN (SELECT DISTINCT place_name AS place_name
    FROM permits.panel_upgrades_geocoded_geographies) AS B
ON A."NAMELSAD" = B."place_name";


