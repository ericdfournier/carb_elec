-- Count the number of distinct municipal data providers in the full permit database
SELECT  COUNT(*) AS total_raw_records,
        COUNT(DISTINCT file_name) AS total_raw_municipalities
FROM permits.combined;

-- Count the population of DAC vs. Non-DAC census tracts in the permit data sampled territories
SELECT SUM(ces."population") AS total_population_sampled,
       SUM(ces."population") FILTER (WHERE ces."ciscorep" >= 75.0) AS total_dac_population_sampled,
       SUM(census."DP04_0001E") AS total_housing_units_sampled,
       SUM(census."DP04_0001E") FILTER (WHERE ces."ciscorep" >= 75.0) AS total_dac_housing_units_sampled,
       COUNT(DISTINCT ces."tract") AS total_tracts_sampled,
       COUNT(DISTINCT ces."tract") FILTER (WHERE ces."ciscorep" >= 75.0) AS total_dac_tracts_sampled
FROM oehha.ca_ces4 AS ces 
JOIN permits.sampled_territories AS sampled
ON ST_INTERSECTS(ST_CENTROID(ces.geom), sampled.geometry)
JOIN census.acs_ca_2019_tr_housing AS census
    ON ces."tract" = census."GEOID"::NUMERIC;

-- Tally the min-max range of the dates associated with different classess of identified panel upgrade permit records by municipal provider.
SELECT * 
FROM ( 
    SELECT  INITCAP(permits.place) AS municipality,
            COUNT(*) AS all_panel_related_permits,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS TRUE AND permits.upgraded_panel_size IS NOT NULL) AS direct_upgrade_observations,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS TRUE AND permits.upgraded_panel_size IS NULL) AS indirect_upgrade_observations,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS NOT TRUE) AS assumed_upgrades,
            COALESCE(MIN(permits.applied_date), MIN(permits.issued_date), MIN(permits.finaled_date)) AS min_date,
            COALESCE(MAX(permits.applied_date), MAX(permits.issued_date), MAX(permits.finaled_date)) AS max_date
    FROM permits.panel_upgrades AS permits
    WHERE permits.place IS NOT NULL
    GROUP BY permits.place
    UNION
    SELECT  INITCAP(permits.county_name) AS municipality,
            COUNT(*) AS all_panel_related_permits,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS TRUE AND permits.upgraded_panel_size IS NOT NULL) AS direct_upgrade_observations,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS TRUE AND permits.upgraded_panel_size IS NULL) AS indirect_upgrade_observations,
            COUNT(*) FILTER (WHERE permits.main_panel_upgrade IS NOT TRUE) AS assumed_upgrades,
            COALESCE(MIN(permits.applied_date), MIN(permits.issued_date), MIN(permits.finaled_date)) AS min_date,
            COALESCE(MAX(permits.applied_date), MAX(permits.issued_date), MAX(permits.finaled_date)) AS max_date
    FROM permits.panel_upgrades AS permits
    WHERE permits.county_name IS NOT NULL
    GROUP BY permits.county_name 
    ) AS stats
ORDER BY stats.all_panel_related_permits DESC;

-- Tally the Proportion of the sf/mf properties modeled by County
SELECT  
        cn."NAMELSAD",
        stats.total_sf_parcels,
        stats.modeled_sf_parcels,
        stats.modeled_sf_percentage, 
        stats.total_mf_parcels, 
        stats.modeled_mf_parcels,
        stats.modeled_mf_percentage,
        cn.geometry
INTO manuscript.county_level_parcel_counts
FROM (SELECT  
        sf.*, 
        mf.total_mf_parcels,
        mf.modeled_mf_parcels,
        mf.modeled_mf_percentage
    FROM (SELECT A.county_name, 
           A.count AS total_sf_parcels,
           B.count AS modeled_sf_parcels,
           ROUND((B.count::NUMERIC / A.count::NUMERIC) * 100.0, 2) AS modeled_sf_percentage
        FROM (
            SELECT  gg.county_name,
                    COUNT(mp.*)
            FROM corelogic.megaparcels AS mp
            JOIN corelogic.megaparcels_geocoded_geographies AS gg 
                ON gg.megaparcelid = mp.megaparcelid
            WHERE mp.usetype = 'single_family'
            GROUP BY gg.county_name) AS A
        JOIN (SELECT  gg.county_name,
                    COUNT(mp.*)
            FROM corelogic.model_data_sf_inference AS mp
            JOIN corelogic.megaparcels_geocoded_geographies AS gg 
                ON gg.megaparcelid = mp.megaparcelid
            WHERE panel_size_existing IS NOT NULL
            GROUP BY gg.county_name) AS B
        ON A.county_name = B.county_name ) AS sf
    JOIN (SELECT A.county_name, 
               A.count AS total_mf_parcels,
               B.count AS modeled_mf_parcels,
               ROUND((B.count::NUMERIC / A.count::NUMERIC) * 100.0, 2) AS modeled_mf_percentage
        FROM (
            SELECT  gg.county_name,
                    COUNT(mp.*)
            FROM corelogic.megaparcels AS mp
            JOIN corelogic.megaparcels_geocoded_geographies AS gg 
                ON gg.megaparcelid = mp.megaparcelid
            WHERE mp.usetype = 'multi_family'
            GROUP BY gg.county_name) AS A
        JOIN (SELECT  gg.county_name,
                    COUNT(mp.*)
            FROM corelogic.model_data_mf_inference AS mp
            JOIN corelogic.megaparcels_geocoded_geographies AS gg 
                ON gg.megaparcelid = mp.megaparcelid
            WHERE panel_size_existing IS NOT NULL
            GROUP BY gg.county_name) AS B
        ON A.county_name = B.county_name) AS mf
    ON sf.county_name = mf.county_name) AS stats
FULL JOIN census.acs_ca_2019_county_geom AS cn
ON stats.county_name = cn."NAMELSAD" ;

-- Inspect attribute coverage for missing counties in original corelogic data
SELECT DISTINCT("situs county") FROM corelogic.corelogic_20231228;

SELECT  "clip",
        "universal building square feet",
        "year built _ piq",
        "land use code _ piq"
FROM corelogic.corelogic_20231228 WHERE "situs county" = 'SAN LUIS OBISPO' AND "land use code _ piq" = 163;

-- Look at records which land is SLO within derived megaparcel data
SELECT * 
FROM corelogic.megaparcels AS mp
JOIN corelogic.megaparcels_geocoded_geographies AS gg
ON mp.megaparcelid = gg.megaparcelid
WHERE county_name = 'San Luis Obispo County';
-- No hits here

-- Look at records whose geometries land in SLO in derived megaparcel data table.
SELECT *
INTO slo_test_megaparcels
FROM corelogic.megaparcels AS mp
JOIN census.acs_ca_2019_county_geom AS cty
ON ST_INTERSECTS(mp.centroid, cty.geometry)
WHERE cty."NAMELSAD" = 'San Luis Obispo County';

-- Look at records whose geometries land in SLO in derived model data table.
SELECT *
INTO slo_test_model_data
FROM corelogic.model_data AS md
JOIN census.acs_ca_2019_county_geom AS cty
ON ST_INTERSECTS(md.centroid, cty.geometry)
WHERE cty."NAMELSAD" = 'San Luis Obispo County';

