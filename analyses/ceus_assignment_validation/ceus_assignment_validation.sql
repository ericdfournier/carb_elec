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
SELECT  unified_naics.*,
        mp."land use code _ piq"
INTO temp.ceus_sector_validation_test
FROM unified_naics
JOIN corelogic.corelogic_20240126_megaparcel AS mp
    ON ST_INTERSECTS(unified_naics.centroid, mp.geom);
        
SELECT  customers.*,
        naics."ceus_subsector" AS naics_to_ceus_subsector,
        usetype."ceus_subsector" AS usetype_to_ceus_subsector
INTO temp.ceus_sector_validation_test_ii
FROM temp.ceus_sector_validation_test AS customers
JOIN crosswalk.utility_account_naics_to_ceus AS naics
    ON customers."premnaics"::text = naics."premnaics"
JOIN crosswalk.corelogic_landuse_code_to_ceus_sector_dictionary AS usetype
    ON customers."land use code _ piq" = usetype."corelogic_universal_landuse_code";

SELECT *
FROM TEMP.ceus_sector_validation_test_ii
WHERE "naics_to_ceus_subsector" != "usetype_to_ceus_subsector";



