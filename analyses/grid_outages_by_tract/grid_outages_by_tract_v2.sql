-- Directly Compute Facility to Circuit Associations by Commercial Sub-Sector

SELECT AddGeometryColumn('corelogic','corelogic_20240126_megaparcel','centroid', 3310,'POINT', 2, false);

UPDATE corelogic.corelogic_20240126_megaparcel
SET centroid = ST_CENTROID(geom);

-- Index centroids
CREATE INDEX corelogic_20240126_megaparcel_centroid_idx
ON corelogic.corelogic_20240126_megaparcel USING GIST("centroid");

-- Create Megaparcelid
ALTER TABLE corelogic.corelogic_20240126_megaparcel
ADD COLUMN megaparcelid SERIAL;

-- Index megaparcelids
CREATE INDEX corelogic_20240126_megaparcel_megaparcelid_idx
ON corelogic.corelogic_20240126_megaparcel("megaparcelid");

-- Compute parcel to circuit associations
WITH 
unified_naics AS 
    (WITH 
        pge_non_res_customer_naics AS (
        SELECT  premiseid,
                premnaics,
                centroid,
                'pge' AS utility
        FROM cpuc2022_nonres.pge_cis
        WHERE   premnaics IS NOT NULL AND 
                ST_ISEMPTY(centroid) = FALSE),
        scg_non_res_customer_naics AS (
        SELECT  premiseid,
                premnaics,
                centroid,
                'scg' AS utility
        FROM cpuc2022_nonres.scg_cis
        WHERE premnaics IS NOT NULL AND
                ST_ISEMPTY(centroid) = FALSE),
        sdge_non_res_customer_naics AS (
        SELECT  premiseid,
                premnaics,
                centroid,
                'sdge' AS utility
        FROM cpuc2022_nonres.sdge_cis
        WHERE   premnaics IS NOT NULL AND
                ST_ISEMPTY(centroid) = FALSE)
    SELECT DISTINCT * 
    FROM pge_non_res_customer_naics
        UNION
    SELECT DISTINCT *
    FROM scg_non_res_customer_naics
        UNION
    SELECT DISTINCT * 
    FROM sdge_non_res_customer_naics),
ceus AS (
    SELECT  unified_naics."premiseid",
            cw."ceus_subsector",
            unified_naics."centroid"
    FROM unified_naics
    JOIN crosswalk.utility_account_naics_to_ceus_20240523 AS cw
        ON unified_naics."premnaics" = cw."premnaics"
    WHERE cw."ceus_subsector" NOT IN (
        'Forestry', 
        'Residential',
        'National Security',
        'Mining & Extraction',
        'Industrial',
        'Ag & Pumping',
        'Fishing',
        'TCU') AND 
    cw."ceus_subsector" IS NOT NULL
)
SELECT  DISTINCT ceus."premiseid",
        ceus."ceus_subsector",
        circuits."circuit_name",
        ("geom" <-> ceus."centroid") AS circuit_distance,
        ceus."centroid"
INTO    commercial_scope.subsector_megaparcels_to_circuits
FROM    megaparcels
CROSS JOIN LATERAL 
    (SELECT  "circuit_name", "geom"
        FROM commercial_scope.ious_all_circuits
        ORDER BY "geom" <-> ceus."centroid"
        LIMIT 1) AS circuits;
    
-- TODO: TEST THE CODE BLOCKS ABOVE!!!
    
-- NULL out negative outage hours
UPDATE cpuc.psps_outages_2013_2023_simplified
SET outage_hours = NULL
WHERE outage_hours < 0;

-- Map Circuits with Outages
WITH
outages AS (
    SELECT  circuit_name,
            SUM(outage_hours) AS cumulative_outage_hours 
    FROM cpuc.psps_outages_2013_2023_simplified
    GROUP BY circuit_name
    ),
circuits AS (
    SELECT  circuit_name, 
            geom
    FROM commercial_scope.ious_all_circuits)
SELECT  circuits.circuit_name,
        circuits.geom,
        product.cumulative_outage_hours
INTO commercial_scope.all_circuits_outages_geo
FROM circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY circuits.circuit_name <-> outages.circuit_name ASC
        LIMIT 1) AS product;

-- Join parcel level data to circuit level PSPS Data
WITH 
circuits AS (
    SELECT  circuit_name,
            ceus_subsector,
            COUNT(DISTINCT megaparcelid) AS cumulative_facilities
    FROM    commercial_scope.subsector_megaparcels_to_circuits
    GROUP BY circuit_name, ceus_subsector
    ),
outages AS (
    SELECT  circuit_name,
            SUM(outage_hours) AS cumulative_outage_hours 
    FROM cpuc.psps_outages_2013_2023_simplified
    GROUP BY circuit_name
    )
SELECT  DISTINCT circuits.circuit_name AS target_circuit_name,
        product.circuit_name  AS match_circuit_name,
        circuits.ceus_subsector AS ceus_subsector,
        (REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(product.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '')) AS match_similarity_score,
        product.cumulative_outage_hours,
        circuits.cumulative_facilities
INTO commercial_scope.circuit_psps_join_v2
FROM circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuits.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') <-> REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(outages.circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') ASC
        LIMIT 1) AS product;

-- Filter records based upon match similarity
UPDATE commercial_scope.circuit_psps_join_v2
SET cumulative_outage_hours = NULL
WHERE match_similarity_score > 0.5;

UPDATE commercial_scope.circuit_psps_join_v2
SET cumulative_facilities = NULL
WHERE match_similarity_score > 0.5;

-- Add cumulative score field
ALTER TABLE commercial_scope.circuit_psps_join_v2
ADD COLUMN cumulative_outage_score NUMERIC;

UPDATE commercial_scope.circuit_psps_join_v2
SET cumulative_outage_score = cumulative_outage_hours * cumulative_facilities;

SELECT  ceus_subsector,
        SUM(cumulative_outage_score)
FROM    commercial_scope.circuit_psps_join_v2
GROUP BY ceus_subsector
ORDER BY ceus_subsector ASC;

-- Report documentation queries

SELECT COUNT( DISTINCT circuit_name)
FROM cpuc.psps_outages_2013_2023_simplified;

SELECT COUNT( DISTINCT match_circuit_name)
FROM commercial_scope.circuit_psps_join_v2;

