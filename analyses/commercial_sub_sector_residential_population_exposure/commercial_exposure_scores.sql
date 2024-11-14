-- Execute the following code on the Database Server in the IOUs database

-- Modify below to take as input the non-res customer centroids directly from the consumption dataset.
-- USE VIEW ON PREMISE ID THAT SPENCER WILL CREATE
 
-- Presume's that "unified_naics" table has already been generated

SELECT  naics."ceus_subsector" AS "ceus_subsector",
    ST_UNION(ST_BUFFER(mp."geom", 200)) AS geom,
    COUNT(unified_naics."premiseid") AS premiseid_count
INTO temp.landuse_buffer
FROM project.unified_naics
JOIN corelogic.corelogic_20240126_megaparcel AS mp
    ON ST_INTERSECTS(unified_naics."centroid", mp."geom")
JOIN crosswalk.naics_to_ceus AS naics
    ON unified_naics."naics_code" = naics."naics_code"
WHERE naics."ceus_subsector" NOT IN (
	'Forestry',
	'Construction',
	'Residential',
	'National Security',
	'Mining & Extraction',
	'Industrial',
	'Ag & Pumping',
	'Fishing',
	'TCU') AND
	naics."ceus_subsector" IS NOT NULL
GROUP BY naics."ceus_subsector";

CREATE INDEX landuse_buffer_geom_id
    ON temp.landuse_buffer
    USING GIST (geom);

SELECT ST_CENTROID(mp.geom) AS centroid,
   mp."number of units",
   census."geoid",
   census."percent_occupied", 
   census."avg_household_size_of_occupied",
   CASE WHEN ces."ciscorep" >= 75.0 THEN TRUE ELSE FALSE END AS dac
INTO temp.residential_parcels
FROM corelogic.corelogic_20240126_megaparcel AS mp
JOIN geo.calenviroscreen40_gdb AS ces
    ON ST_INTERSECTS(ST_CENTROID(mp."geom"), ces."geom")
JOIN census.cb_2022_acs AS census
    ON ST_INTERSECTS(ST_CENTROID(mp."geom"), census."geom")
WHERE mp."land use code _ piq" IN ('100',
                                    '102',
                                    '106',
                                    '109',
                                 -- '111', - exclude condos due to bogus unit counts
                                 -- '112', - exclude condos due to bogus unit counts
                                 -- '116', - exclude condos due to bogus unit counts
                                 -- '117', - exclude condos due to bogus unit counts
                                    '135',
                                    '137',
                                    '138',
                                    '148',
                                    '160',
                                    '163',
                                    '199',
                                    '115',
                                    '151',
                                    '165',
                                    '103',
                                    '131',
                                    '132',
                                    '133',
                                    '167') AND
     census."lsad" = 'CT';
                                
-- NOTE: Might need to exclude condos from the above as there are major issues with the unit counts that still need to be addressed

CREATE INDEX residential_parcels_centroid_idx
    ON temp.residential_parcels
    USING GIST(centroid);

-- Need to just do a straightforward intersection and not a cross lateral join

WITH unique_parcels AS (
    SELECT  DISTINCT res_parcels.*,
            lb."ceus_subsector"
    FROM temp.landuse_buffer AS lb
    JOIN TEMP.residential_parcels AS res_parcels
        ON ST_INTERSECTS(lb."geom", res_parcels."centroid"))
SELECT 
    unique_parcels."ceus_subsector",
    unique_parcels."dac",
    ST_UNION(unique_parcels.centroid) AS "geom",
    COUNT(unique_parcels.*) AS "nearby_residential_property_count",
    SUM(unique_parcels."number of units" * unique_parcels."avg_household_size_of_occupied" * (unique_parcels."percent_occupied"/100.0)) AS "nearby_residential_population_estimate"
INTO project.carb_ceus_sector_residential_exposure_dac_status_v2
FROM unique_parcels
GROUP BY unique_parcels."ceus_subsector", unique_parcels."dac";


-- Divide nearby residential population estimate by the total number of facilities within each sub-sector to estimate average exposure population per facility
WITH res_stats AS (
    SELECT  ceus_subsector,
            dac,
            nearby_residential_population_estimate
    FROM project.carb_ceus_sector_residential_exposure_dac_status_v2),
naics_stats AS (
    SELECT  ceus_subsector,
            dac,
            COUNT(DISTINCT premiseid) AS distinct_premises
    FROM project.unified_naics
    GROUP BY ceus_subsector, dac)
SELECT  res_stats.ceus_subsector,
        res_stats.dac,
        (res_stats.nearby_residential_population_estimate / naics_stats.distinct_premises) AS average_exposed_residential_population_per_facility
FROM res_stats
JOIN naics_stats
    ON res_stats.ceus_subsector = naics_stats.ceus_subsector AND res_stats.dac = naics_stats.dac
ORDER BY res_stats.ceus_subsector, res_stats.dac ASC;

-- Compute total residential population exposure per ceus subsector
WITH res_stats AS (
    SELECT  ceus_subsector,
            dac,
            nearby_residential_population_estimate
    FROM project.carb_ceus_sector_residential_exposure_dac_status_v2)
SELECT  res_stats.ceus_subsector,
        res_stats.dac,
        SUM(res_stats.nearby_residential_population_estimate) AS total_exposed_residential_population_per_facility
FROM res_stats
GROUP BY res_stats.ceus_subsector, res_stats.dac
ORDER BY res_stats.ceus_subsector, res_stats.dac ASC;

-- Count DISTINCT NAICS

SELECT  ceus_subsector,
        dac,
        COUNT(DISTINCT premiseid) AS distinct_premises
FROM project.unified_naics
WHERE ceus_subsector NOT IN (
    'Forestry',
    'Construction',
    'Residential',
    'National Security',
    'Mining & Extraction',
    'Industrial',
    'Ag & Pumping',
    'Fishing',
    'TCU')
GROUP BY ceus_subsector, dac
