-- Generate a Unified View of all the Circuits in the State's IOUs
WITH 
sce AS (
    SELECT  'sce' AS "utility",
            "circuit_name",
            ST_UNION("geom") AS "geom"
    FROM sce.ica_circuit_segments_3phase
        GROUP BY "circuit_name"
        ),
sdge AS (
    SELECT  'sdge' AS "utility",
            "circuit_na" AS "circuit_name",
            ST_UNION("geom") AS "geom"
    FROM sdge.ica_circuit_segments_3phase_generation_capacity
        GROUP BY "circuit_na"
        ),
pge AS (
    SELECT  'pge' AS "utility",
            "feeder_name" AS "circuit_name",
            ST_UNION("geom") AS "geom"
    FROM pge.ica_feeder_detail
        GROUP BY "feeder_name"
        )
SELECT ious_union.* 
INTO commercial_scope.ious_all_circuits
FROM
    (SELECT * FROM sce
        UNION 
    SELECT * FROM sdge  
        UNION
    SELECT * FROM pge) AS ious_union;

-- Index geometry field for spatial joins
CREATE INDEX idx_ious_all_circuits_geom
ON commercial_scope.ious_all_circuits USING GIST("geom");

-- Index circuit name field
CREATE INDEX idx_ious_all_circuits_circuit_name
ON commercial_scope.ious_all_circuits("circuit_name")

-- Compute Circuit Intersection Counts per Tract
WITH
c AS (
    SELECT  tracts."GEOID" AS geoid,
            ARRAY_AGG(DISTINCT (circuits."circuit_name")) AS circuit_names
    FROM census.acs_ca_2019_tr_geom AS tracts
    JOIN commercial_scope.ious_all_circuits AS circuits
        ON ST_INTERSECTS(tracts."geometry", circuits."geom")
    GROUP BY tracts."GEOID"
    ),
t AS (
    SELECT  tracts."GEOID" AS geoid,
            tracts."geometry" AS geom
    FROM census.acs_ca_2019_tr_geom AS tracts
    )
SELECT  c."geoid",
        c."circuit_names",
        CARDINALITY(c."circuit_names") AS "circuit_counts",
        t."geom"
INTO commercial_scope.tracts_circuit_counts
FROM c
JOIN t 
    ON c."geoid" = t."geoid";

-- Compute Intersecting Circuit Line Length Proportions per Tract        
WITH 
dist AS (
    SELECT  tracts."GEOID" AS "geoid",
            circuits."utility",
            circuits."circuit_name", 
            SUM(ST_LENGTH(ST_Intersection(tracts."geometry", circuits."geom"))) AS "line_distance"
    FROM census.acs_ca_2019_tr_geom AS tracts, commercial_scope.ious_all_circuits AS circuits
    WHERE ST_Intersects(tracts."geometry", circuits."geom")
    GROUP BY circuits."utility", circuits."circuit_name", tracts."GEOID"
    ),
tot_dist AS (
    SELECT "geoid",
            SUM("line_distance") AS "total_line_distance"
    FROM dist
    GROUP BY "geoid"
    )
SELECT dist."geoid",
       dist."utility",
       dist."circuit_name",
       dist."line_distance"/tot_dist."total_line_distance" AS "line_distance_proportion"
INTO commercial_scope.tracts_circuit_line_distance_proportions
FROM dist
JOIN tot_dist
    ON dist."geoid" = tot_dist."geoid"
ORDER BY dist."geoid", dist."utility", tot_dist."geoid";

-- Generate Derived Field that Aggregates PSPS Outage by Simplified Circuit Name - Minus Section ID Numerical Identifiers
SELECT  REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '') AS circuit_name,
        SUM(outage_hours) AS outage_hours,
        SUM("commercial.industrial_customers") AS commercial_customers
INTO cpuc.psps_outages_2013_2023_simplified
FROM cpuc.psps_outages_2013_2023
GROUP BY REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(circuit_name, '[+-]?\d+(?:\.\d+)?', ''), '*', ''), '-', ''), 'kV', '');

-- Test Join Against CPUC PSPS Shutoff Table on Circuit Name
WITH
outages AS (
    SELECT  circuit_name,
            SUM(outage_hours) AS cumulative_outage_hours,
            SUM(commercial_customers) AS cumulative_commercial_customers
    FROM cpuc.psps_outages_2013_2023_simplified
    GROUP BY circuit_name)
SELECT  circuits.geoid,
        circuits.utility AS target_utility,
        circuits.utility AS match_utility,
        circuits.circuit_name AS target_circuit_name,
        product.circuit_name  AS match_circuit_name,
        (circuits.circuit_name <-> product.circuit_name) AS match_similarity_score,
        circuits.line_distance_proportion,
        product.cumulative_outage_hours,
        product.cumulative_commercial_customers
INTO commercial_scope.circuit_psps_join
FROM commercial_scope.tracts_circuit_line_distance_proportions AS circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY circuits.circuit_name <-> outages.circuit_name ASC
        LIMIT 1) AS product;
    
-- Filter records based upon match similarity
UPDATE commercial_scope.circuit_psps_join
SET cumulative_outage_hours = NULL
WHERE match_similarity_score > 0.5;

UPDATE commercial_scope.circuit_psps_join
SET cumulative_commercial_customers = NULL
WHERE match_similarity_score > 0.5;

-- Add cumulative score field
ALTER TABLE commercial_scope.circuit_psps_join
ADD COLUMN cumulative_outage_score NUMERIC;

UPDATE commercial_scope.circuit_psps_join
SET cumulative_outage_score = cumulative_outage_hours * line_distance_proportion;

-- Generate result output with geospatial field for debugging
WITH 
product AS (
    SELECT  res.geoid,
            SUM(res.cumulative_outage_score) AS cumulative_outage_score
    FROM commercial_scope.circuit_psps_join AS res
    GROUP BY res.geoid)
SELECT  product.*,
        tracts.geometry
INTO commercial_scope.circuit_psps_result
FROM product
RIGHT JOIN census.acs_ca_2019_tr_geom AS tracts
    ON product.geoid = tracts."GEOID";

-- NULL Negative values
UPDATE commercial_scope.circuit_psps_result
SET cumulative_outage_score = NULL
WHERE cumulative_outage_score < 0;

-- Generate Property Counts for Each Ceus Sector by Tract
SELECT  mpgg.tract_geoid_2019,
        cw.ceus_subsector,
        COUNT(DISTINCT mp.megaparcelid)
INTO commercial_scope.tracts_ceus_property_counts
FROM corelogic.corelogic_20240126_varchar_megaparcels AS mp 
JOIN corelogic.corelogic_20240126_varchar_megaparcels_geocoded_geographies AS mpgg
    ON mp."megaparcelid" = mpgg."megaparcelid"
JOIN crosswalk.corelogic_landuse_code_to_ceus_sector_dictionary AS cw
    ON mp."property indicator code _ piq" = cw."property_indicator"::TEXT
GROUP BY mpgg.tract_geoid_2019, cw.ceus_subsector;

-- Multiply Outage Scores for Each Tract by the corresponding Ceus Subsector Property Counts and Aggregate
WITH 
tract_counts AS (
    SELECT  tcpc.tract_geoid_2019,
            tcpc.ceus_subsector,
            tcpc.count AS property_count,
            psps.cumulative_outage_score
    FROM commercial_scope.tracts_ceus_property_counts AS tcpc
    JOIN commercial_scope.circuit_psps_result AS psps
        ON tcpc.tract_geoid_2019 = psps.geoid)
SELECT  tract_counts.ceus_subsector,
        SUM(tract_counts.property_count * cumulative_outage_score) AS weighted_cumulative_outage_score
FROM tract_counts
GROUP BY tract_counts.ceus_subsector
ORDER BY tract_counts.ceus_subsector ASC;

-- Count Distinct Values for Reporting
SELECT COUNT (DISTINCT circuit_name) FROM cpuc.psps_outages_2013_2023;

SELECT COUNT (DISTINCT circuit_name) FROM cpuc.psps_outages_2013_2023_simplified;

SELECT COUNT (DISTINCT circuit_name) FROM commercial_scope.ious_all_circuits;

SELECT DISTINCT ceus_subsector FROM commercial_scope.tracts_ceus_property_counts ORDER BY ceus_subsector ASC;

SELECT COUNT(DISTINCT geometry) FROM census.acs_ca_2019_tr_geom;

