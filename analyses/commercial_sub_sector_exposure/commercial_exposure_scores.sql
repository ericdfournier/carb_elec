-- Execute the following code on the Database Server in the IOUs database

-- Modify below to take as input the non-res customer centroids directly from the consumption dataset. 
WITH 
unified_naics AS 
    (WITH 
    pge_non_res_customer_naics AS (
        SELECT  keyacctid, 
                premnaics,
                centroid,
                'pge' AS utility
        FROM cpuc2022_nonres.pge_cis
        WHERE   premnaics IS NOT NULL AND 
                ST_ISEMPTY(centroid) = FALSE),
    scg_non_res_customer_naics AS (
        SELECT  keyacctid, 
                premnaics,
                centroid,
                'scg' AS utility
        FROM cpuc2022_nonres.scg_cis
        WHERE premnaics IS NOT NULL AND
                ST_ISEMPTY(centroid) = FALSE),
    sdge_non_res_customer_naics AS (
        SELECT  keyacctid,
                premnaics,
                centroid,
                'sdge' AS utility
        FROM cpuc2022_nonres.sdge_cis
        WHERE   premnaics IS NOT NULL AND
                ST_ISEMPTY(centroid) = FALSE)
    SELECT * 
    FROM pge_non_res_customer_naics
        UNION
    SELECT *
    FROM scg_non_res_customer_naics
        UNION
    SELECT * 
    FROM sdge_non_res_customer_naics)
SELECT  naics."ceus_subsector" AS "ceus_subsector",
    ST_UNION(ST_BUFFER(mp."geom", 200)) AS geom,
    COUNT(DISTINCT unified_naics."keyacctid") AS accounts_count
INTO temp.landuse_buffer
FROM unified_naics
JOIN corelogic.corelogic_20240126_megaparcel AS mp
    ON ST_INTERSECTS(unified_naics."centroid", mp."geom")
JOIN crosswalk.utility_account_naics_to_ceus AS naics
    ON unified_naics."premnaics"::text = naics."premnaics"
WHERE naics."ceus_subsector" NOT IN (
	'Forestry',
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
   mp."universal building square feet",
   CASE WHEN ces."ciscorep" >= 75.0 THEN TRUE ELSE FALSE END AS dac
INTO temp.residential_parcels
FROM corelogic.corelogic_20240126_megaparcel AS mp
JOIN geo.calenviroscreen40_gdb AS ces
    ON ST_INTERSECTS(ST_CENTROID(mp."geom"), ces."geom")
WHERE mp."land use code _ piq" IN ('100',
                                    '102',
                                    '109',
                                    '135',
                                    '137',
                                    '138',
                                    '148',
                                    '160',
                                    '163',
                                    '111',
                                    '112',
                                    '116',
                                    '117',
                                    '199',
                                    '115',
                                    '151',
                                    '165',
                                    '103',
                                    '106',
                                    '131',
                                    '132',
                                    '133',
                                    '167');

CREATE INDEX residential_parcels_centroid_idx
    ON temp.residential_parcels
    USING GIST(centroid);

SELECT  lb."ceus_subsector",
        res_parcels."dac",
        ST_UNION(res_parcels.centroid) AS "geom",
        COUNT(DISTINCT res_parcels.*) AS "nearby_residential_property_count",
        SUM(res_parcels."universal building square feet") AS "nearby_residential_property_square_footage"
INTO project.carb_ceus_sector_residential_exposure_dac_status
FROM temp.landuse_buffer AS lb
CROSS JOIN LATERAL
    (SELECT * FROM temp.residential_parcels AS rp WHERE ST_INTERSECTS(lb."geom", rp."centroid")) AS res_parcels
GROUP BY lb."ceus_subsector", res_parcels."dac";
