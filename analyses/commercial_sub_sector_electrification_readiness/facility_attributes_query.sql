WITH 
facility_stats AS (
    SELECT  A.ceus_subsector AS ceus_subsector,
            A.dac,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY B."year built _ piq") AS median_vintage,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY B."universal building square feet") AS median_sqft
    FROM project.unified_naics AS A
    JOIN corelogic.corelogic_20240126_megaparcel AS B
        ON ST_INTERSECTS(A.centroid, B.geom)
    GROUP BY A.ceus_subsector, dac
),
usage_per_facility AS (
    SELECT  ceus_subsector,
            "is_dac" AS dac,
            (SUM(therms_total) / SUM(premiseid_tally)) AS average_therms_per_premise
    FROM    cpuc2022_nonres_aggregations.gas_bill_data_by_tract
    WHERE "year" = 2021
    GROUP BY "ceus_subsector", "is_dac"
)
SELECT  facility_stats.*,
        usage_per_facility.average_therms_per_premise
INTO project.electrification_readiness_stats
FROM facility_stats
JOIN usage_per_facility
    ON  facility_stats.ceus_subsector = usage_per_facility.ceus_subsector AND
        facility_stats.dac = usage_per_facility.dac
WHERE facility_stats.ceus_subsector IN (
                                        'College',
                                        'Food Store',
                                        'Health Care',
                                        'Lodging',
                                        'Miscellaneous',
                                        'Office',
                                        'Refrigerated Warehouse',
                                        'Restaurant',
                                        'Retail',
                                        'School',
                                        'Unrefrigerated Warehouse');