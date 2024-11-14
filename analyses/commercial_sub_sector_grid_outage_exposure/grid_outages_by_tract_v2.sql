-- NOTE: This code needs to be run on the database server

-- Index geom field on all circuits geom table
CREATE INDEX idx_ious_all_circuits_geom 
ON project.ious_all_circuits
USING GIST(geom);

-- Generate unified table of all unique non-residential customer premises with NAICS code identifiers
WITH
unified_naics AS 
    (
    SELECT DISTINCT * 
    FROM cpuc2022_nonres_geocode.pge_gas_keyacctid_to_point
        UNION
    SELECT DISTINCT *
    FROM cpuc2022_nonres_geocode.scg_gas_keyacctid_to_point
        UNION
    SELECT DISTINCT * 
    FROM cpuc2022_nonres_geocode.sdge_gas_keyacctid_to_point)
SELECT  unified_naics.keyacctid,
        unified_naics.premiseid,
        unified_naics.fuel,
        unified_naics.naics_code,
        unified_naics.ceus_sector,
        cw.ceus_subsector,
        unified_naics.centroid,
        CASE WHEN ces."ciscorep" >= 75.0 THEN TRUE ELSE FALSE END AS dac
INTO project.unified_naics
FROM unified_naics
JOIN geo.calenviroscreen40_gdb AS ces
    ON ST_INTERSECTS(unified_naics."centroid", ces."geom")
JOIN crosswalk.naics_to_ceus AS cw
    ON unified_naics.naics_code = cw.naics_code;

-- Index centroid field on unified naics table
CREATE INDEX idx_unified_naics_centroid 
ON project.unified_naics 
USING GIST(centroid);

-- Compute premise to circuit and premise NAICS to CEUS sub-sector associations
WITH
cw AS (
    SELECT  a.naics_code,
            b.naics_title, 
            b.ceus_sector,
            b.ceus_subsector
    FROM crosswalk.premnaics_to_naics AS a
    JOIN crosswalk.naics_to_ceus AS b 
        ON a.naics_code = b.naics_code
),
ceus AS (
    SELECT  unified_naics."premiseid",
            unified_naics."dac",
            cw."ceus_subsector",
            unified_naics."centroid"
    FROM project.unified_naics
    JOIN cw
        ON unified_naics."naics_code" = cw."naics_code"
    WHERE cw."ceus_subsector" NOT IN (
        'Forestry', 
        'Residential',
        'National Security',
        'Mining & Extraction',
        'Industrial',
        'Ag & Pumping',
        'Fishing',
        'TCU',
        'Construction') AND 
    cw."ceus_subsector" IS NOT NULL
)
SELECT  DISTINCT ceus."premiseid",
        ceus."ceus_subsector",
        ceus."dac",
        circuits."circuit_name",
        ("geom" <-> ceus."centroid") AS circuit_distance,
        ceus."centroid"
INTO    project.subsector_premises_to_circuits
FROM    ceus
CROSS JOIN LATERAL 
    (SELECT  "circuit_name", "geom"
        FROM project.ious_all_circuits
        ORDER BY "geom" <-> ceus."centroid"
        LIMIT 1) AS circuits;
    
-- NULL out negative outage hours
UPDATE project.psps_outages_2013_2023_simplified
SET outage_hours = NULL
WHERE outage_hours < 0;

-- Map circuits with outages
WITH
outages AS (
    SELECT  circuit_name::text,
            SUM(outage_hours) AS cumulative_outage_hours 
    FROM project.psps_outages_2013_2023_simplified
    GROUP BY circuit_name
    ),
circuits AS (
    SELECT  circuit_name::text, 
            geom
    FROM project.ious_all_circuits)
SELECT  circuits.circuit_name AS source_circuit_name,
        product.circuit_name AS target_circuit_name,
        (REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(product.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '')) AS match_similarity_score,
        product.cumulative_outage_hours,
        circuits.geom
INTO project.all_circuits_outages_geo
FROM circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(outages.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') ASC
        LIMIT 1) AS product;
    
-- Filter records based upon match similarity
UPDATE project.all_circuits_outages_geo
SET cumulative_outage_hours = NULL
WHERE match_similarity_score > 0.5;
        
-- Join parcel level data to circuit level PSPS Data
WITH 
circuits AS (
    SELECT  circuit_name,
            ceus_subsector,
            dac,
            COUNT(DISTINCT premiseid) AS cumulative_facilities
    FROM    project.subsector_premises_to_circuits
    GROUP BY circuit_name, ceus_subsector, dac
    ),
outages AS (
    SELECT  circuit_name,
            SUM(outage_hours) AS cumulative_outage_hours 
    FROM project.psps_outages_2013_2023_simplified
    GROUP BY circuit_name
    )
SELECT  DISTINCT circuits.circuit_name AS target_circuit_name,
        product.circuit_name  AS match_circuit_name,
        circuits.ceus_subsector AS ceus_subsector,
        circuits.dac,
        (REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(product.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '')) AS match_similarity_score,
        product.cumulative_outage_hours,
        circuits.cumulative_facilities
INTO project.circuit_psps_join_v2
FROM circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(outages.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') ASC
        LIMIT 1) AS product;
    
-- Might make sense to create a copy of the original output here before doing the filtering based upon match similarity score.
CREATE TABLE project.circuit_psps_join_v2_filtered AS 
SELECT * FROM project.circuit_psps_join_v2;

-- Filter records based upon match similarity
UPDATE project.circuit_psps_join_v2_filtered
SET cumulative_outage_hours = NULL
WHERE match_similarity_score > 0.5;

UPDATE project.circuit_psps_join_v2_filtered
SET cumulative_facilities = NULL
WHERE match_similarity_score > 0.5;

-- Compute annual average outage hours per CEUS sector facility type - disaggregated by DAC status - over 10 year data collection period.
SELECT  ceus_subsector,
        dac,
        ROUND(AVG(cumulative_outage_hours) / 10,3) AS annual_average_psps_outage_hours
FROM    project.circuit_psps_join_v2_filtered
GROUP BY ceus_subsector, dac
ORDER BY ceus_subsector, dac ASC;

-- Compute total outage hours per CEUS sector facility type - disaggregated by DAC status - over 10 year data collection period.
SELECT  ceus_subsector,
        dac,
        SUM(cumulative_outage_hours) AS annual_total_psps_outage_hours
FROM    project.circuit_psps_join_v2_filtered
GROUP BY ceus_subsector, dac
ORDER BY ceus_subsector, dac ASC;

-- Compute annual average outage hours per CEUS sector facility type - NOT disaggregated by DAC status - over 10 year data collection period.
SELECT  ceus_subsector,
        ROUND(AVG(cumulative_outage_hours) / 10,2) AS annual_average_psps_outage_hours
FROM    project.circuit_psps_join_v2_filtered
GROUP BY ceus_subsector
ORDER BY ceus_subsector ASC;

-- Compute total annual outage hours per CEUS sector facility type - NOT disaggregated by DAC status - over 10 year data collection period.
SELECT  ceus_subsector,
        SUM(cumulative_outage_hours) AS annual_total_psps_outage_hours
FROM    project.circuit_psps_join_v2_filtered
GROUP BY ceus_subsector
ORDER BY ceus_subsector ASC;

-- Report documentation queries

SELECT COUNT( DISTINCT circuit_name)
FROM project.psps_outages_2013_2023_simplified;

SELECT COUNT( DISTINCT match_circuit_name)
FROM project.circuit_psps_join_v2_filtered;

-- Count total number of facilities within each sub-sector
WITH
unified_naics AS 
    (
    SELECT DISTINCT * 
    FROM cpuc2022_nonres_geocode.pge_gas_keyacctid_to_point
        UNION
    SELECT DISTINCT *
    FROM cpuc2022_nonres_geocode.scg_gas_keyacctid_to_point
        UNION
    SELECT DISTINCT * 
    FROM cpuc2022_nonres_geocode.sdge_gas_keyacctid_to_point),
cw AS (
    SELECT  a.naics_code,
            b.naics_title, 
            b.ceus_sector,
            b.ceus_subsector
    FROM crosswalk.premnaics_to_naics AS a
    JOIN crosswalk.naics_to_ceus AS b 
        ON a.naics_code = b.naics_code
)
SELECT  cw.ceus_subsector, 
        COUNT(DISTINCT unified_naics.premiseid)
FROM unified_naics 
JOIN cw
    ON unified_naics.naics_code = cw.naics_code
WHERE
    cw.ceus_subsector NOT IN (
        'Forestry', 
        'Residential',
        'National Security',
        'Mining & Extraction',
        'Industrial',
        'Ag & Pumping',
        'Fishing',
        'TCU',
        'Construction')
GROUP BY cw.ceus_subsector;

