-- Index the shoreline geometry linestring prior to runnning calculation
CREATE INDEX IF NOT EXISTS idx_us_medium_shoreline_geom_idx
ON noaa.us_medium_shoreline
USING gist (geom);

-- Compute the distance to shore from each parcel centroid
SELECT DISTINCT megaparcels."megaparcelid",
    (SELECT FLOOR(ST_Distance(megaparcels.centroid, shoreline.geom))::INTEGER
        FROM   noaa.us_medium_shoreline AS shoreline
        ORDER BY
            megaparcels.centroid <-> shoreline.geom
        LIMIT  1) AS shorelinedistm
INTO corelogic.distance_20240126
FROM corelogic.corelogic_20240126_varchar_megaparcels AS megaparcels;

-- Compute the elevation of each parcel centroid using a cross lateral join
SELECT DISTINCT megaparcels."megaparcelid",
       elevation.elevationm
INTO    corelogic.elevation_20240126
FROM    corelogic.corelogic_20240126_varchar_megaparcels AS megaparcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, megaparcels.centroid))::INTEGER AS elevationm
        FROM srtm.ca_elevation
        WHERE ST_INTERSECTS(megaparcels.centroid, rast)) AS elevation;

-- Compute the slope at each parcel centroid using a cross lateral join
SELECT DISTINCT megaparcels."megaparcelid",
       slope.slopepct
INTO    corelogic.slope_20240126
FROM    corelogic.corelogic_20240126_varchar_megaparcels AS megaparcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, megaparcels.centroid))::INTEGER AS slopepct
        FROM srtm.ca_slope
        WHERE ST_INTERSECTS(megaparcels.centroid, rast)) AS slope;

-- Compute the aspect at each parcel centroid using a cross lateral join
SELECT DISTINCT megaparcels."megaparcelid",
        aspect.aspectdeg
INTO corelogic.aspect_20240126
FROM corelogic.corelogic_20240126_varchar_megaparcels AS megaparcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_VALUE(rast, megaparcels.centroid))::INTEGER AS aspectdeg
        FROM srtm.ca_aspect
        WHERE ST_INTERSECTS(megaparcels.centroid, rast)) AS aspect;

-- Index Join Tables on MegaparcelID
CREATE INDEX IF NOT EXISTS idx_mp_mpid_idx
ON corelogic.corelogic_20240126_varchar_megaparcels ("megaparcelid");

CREATE INDEX IF NOT EXISTS idx_distance_mpid_idx
ON corelogic.distance_20240126 ("megaparcelid");

CREATE INDEX IF NOT EXISTS idx_elevation_mpid_idx
ON corelogic.elevation_20240126 ("megaparcelid");

CREATE INDEX IF NOT EXISTS idx_slope_mpid_idx
ON corelogic.slope_20240126 ("megaparcelid");

CREATE INDEX IF NOT EXISTS idx_aspect_mpid_idx
ON corelogic.aspect_20240126 ("megaparcelid");

CREATE INDEX IF NOT EXISTS idx_geom_geoid_idx
ON census.acs_ca_2019_tr_geom ("GEOID");

CREATE INDEX IF NOT EXISTS idx_housing_geoid_idx
ON census.acs_ca_2019_tr_housing ("GEOID");

CREATE INDEX IF NOT EXISTS idx_fuel_geoid_idx
ON census.acs_ca_2019_tr_fuel ("GEOID");

-- Extract housing features
SELECT A."GEOID",
       A."DP04_0047PE" / 100.0 AS "renterhouseholdspct",
       B."geometry" AS "geom"
INTO census.housing_features
FROM census.acs_ca_2019_tr_housing AS A,
     census.acs_ca_2019_tr_geom AS B
WHERE A."GEOID" = B."GEOID";

-- Index Geometry for Spatial Join
CREATE INDEX IF NOT EXISTS idx_housing_geom_idx
ON census.housing_features USING GIST("geom");

-- Extract fuel features
SELECT A."GEOID",
       A."DP04_0065PE" / 100.0 AS "elecheatinghouseholdspct",
       B."geometry" AS "geom"
INTO census.fuel_features
FROM census.acs_ca_2019_tr_fuel AS A,
     census.acs_ca_2019_tr_geom AS B
WHERE A."GEOID" = B."GEOID";

-- Index Geometry for Spatial Join
CREATE INDEX IF NOT EXISTS idx_fuel_geom_idx
ON census.fuel_features USING GIST("geom");

-- Coalesce Permit Records by Unique Megaparcel ID
SELECT  corelogic_megaparcelid,
        ARRAY_AGG(id) AS permit_id,
        MAX(issued_date) AS issued_date,
        bool_or(solar_pv_system) AS solar_pv_system,
        bool_or(battery_storage_system) AS battery_storage_system,
        bool_or(ev_charger) AS ev_charger,
        bool_or(heat_pump) AS heat_pump,
        bool_or(main_panel_upgrade) AS main_panel_upgrade,
        bool_or(sub_panel_upgrade) AS sub_panel_upgrade,
        MAX(upgraded_panel_size) AS upgraded_panel_size
INTO permits.panel_upgrades_geocoded_deduplicated_20240126
FROM permits.panel_upgrades_geocoded
GROUP BY corelogic_megaparcelid;

-- Extract Relevant Parcel Attributes for Model Training Data
SELECT  DISTINCT ON (mp."megaparcelid")
        mp."megaparcelid",
        mp."clips",
        mp."land use code _ piq",
        mp."year built _ piq",
        mp."universal building square feet",
        mp."sampled",
        mp."usetype",
        mp."panel_size_as_built",
        mp."centroid",
        mp."geom",
        dist."shorelinedistm",
        elev."elevationm",
        slope."slopepct",
        aspect."aspectdeg",
        ces4."ciscorep",
        pp."dac",
        pp."lowincome",
        pp."nondesignated",
        pp."bufferlowincome",
        pp."bufferlih",
        ejscreen."peopcolorpct",
        ejscreen."lowincpct",
        ejscreen."unemppct",
        ejscreen."lingisopct",
        ejscreen."lesshspct",
        ejscreen."under5pct",
        ejscreen."over64pct",
        ejscreen."lifeexppct",
        housing."renterhouseholdspct",
        fuel."elecheatinghouseholdspct",
        cz."bzone",
        ST_X(ST_GEOMETRYN(mp."centroid", 1)) AS "x",
        ST_Y(ST_GEOMETRYN(mp."centroid", 1)) AS "y",
        permits."permit_id",
        permits."issued_date",
        permits."solar_pv_system",
        permits."battery_storage_system",
        permits."ev_charger",
        permits."heat_pump",
        permits."main_panel_upgrade",
        permits."sub_panel_upgrade",
        permits."upgraded_panel_size"
INTO    corelogic.model_data_20240126
FROM    corelogic.corelogic_20240126_varchar_megaparcels AS mp
INNER JOIN corelogic.distance AS dist
    ON dist."megaparcelid" = mp."megaparcelid"
INNER JOIN corelogic.elevation_20240126 AS elev
    ON elev."megaparcelid" = mp."megaparcelid"
INNER JOIN corelogic.slope_20240126 AS slope
    ON slope."megaparcelid" = mp."megaparcelid"
INNER JOIN corelogic.aspect_20240126 AS aspect
    ON aspect."megaparcelid" = mp."megaparcelid"
INNER JOIN oehha.ca_ces4 AS ces4
    ON ST_INTERSECTS(mp."centroid", ces4."geom" )
INNER JOIN carb.priority_populations_ces4 AS pp
    ON ST_INTERSECTS(mp."centroid", pp."geom")
INNER JOIN usepa.ej_screen_ca_2023_tr AS ejscreen
    ON ST_INTERSECTS(mp."centroid", ejscreen."geom")
INNER JOIN cec.ca_building_climate_zones_2021 AS cz
    ON ST_INTERSECTS(mp."centroid", cz."geom")
INNER JOIN census.housing_features AS housing
    ON ST_INTERSECTS(mp."centroid", housing."geom")
INNER JOIN census.fuel_features AS fuel
    ON ST_INTERSECTS(mp."centroid", fuel."geom")
LEFT JOIN permits.panel_upgrades_geocoded_deduplicated_20240126 AS permits
    ON permits."corelogic_megaparcelid" = mp."megaparcelid";

-- Determine Missing Counties
SELECT county."NAMELSAD",
       county."geometry",
       COUNT(DISTINCT mp."megaparcelid") AS valid_megaparcels
INTO corelogic.valid_counties_20240126
FROM corelogic.corelogic_20240126_varchar_megaparcels AS mp
JOIN census.acs_ca_2019_county_geom AS county
    ON ST_INTERSECTS(mp."geom", county."geometry")
WHERE mp.panel_size_as_built IS NOT NULL
GROUP BY county."NAMELSAD", county."geometry";
