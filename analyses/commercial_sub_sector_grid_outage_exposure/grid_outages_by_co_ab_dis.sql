-- Index circuit name field
CREATE INDEX idx_ious_all_circuits_circuit_name
ON project.ious_all_circuits("circuit_name")

-- Compute Circuit Intersection Counts per CoAbDis
WITH
c AS (
    SELECT  co_ab_dis."coabdis_id" AS coabdis_id,
            ARRAY_AGG(DISTINCT (circuits."circuit_name")) AS circuit_names
    FROM boundary.ca_co_ab_dis AS co_ab_dis
    JOIN project.ious_all_circuits AS circuits
        ON ST_INTERSECTS(co_ab_dis."geom", circuits."geom")
    GROUP BY co_ab_dis."coabdis_id"
    ),
t AS (
    SELECT  co_ab_dis."coabdis_id" AS coabdis_id,
            co_ab_dis."geom" AS geom
    FROM boundary.ca_co_ab_dis AS co_ab_dis
    )
SELECT  c."coabdis_id",
        c."circuit_names",
        CARDINALITY(c."circuit_names") AS "circuit_counts",
        t."geom"
INTO project.co_ab_dis_circuit_counts
FROM c
JOIN t 
    ON c."coabdis_id" = t."coabdis_id";

-- Compute Intersecting Circuit Line Length Proportions per CoAbDis        
WITH 
dist AS (
    SELECT  co_ab_dis."coabdis_id" AS "coabdis_id",
            circuits."utility",
            circuits."circuit_name", 
            SUM(ST_LENGTH(ST_Intersection(co_ab_dis."geom", circuits."geom"))) AS "line_distance"
    FROM boundary.ca_co_ab_dis AS co_ab_dis, project.ious_all_circuits AS circuits
    WHERE ST_Intersects(co_ab_dis."geom", circuits."geom")
    GROUP BY circuits."utility", circuits."circuit_name", co_ab_dis."coabdis_id"
    ),
tot_dist AS (
    SELECT "coabdis_id",
            SUM("line_distance") AS "total_line_distance"
    FROM dist
    GROUP BY "coabdis_id"
    )
SELECT dist."coabdis_id",
       dist."utility",
       dist."circuit_name",
       dist."line_distance"/tot_dist."total_line_distance" AS "line_distance_proportion"
INTO project.co_ab_dis_circuit_line_distance_proportions
FROM dist
JOIN tot_dist
    ON dist."coabdis_id" = tot_dist."coabdis_id"
ORDER BY dist."coabdis_id", dist."utility", tot_dist."coabdis_id";

-- Test Join Against CPUC PSPS Shutoff Table on Circuit Name
WITH
outages AS (
    SELECT  circuit_name,
            SUM(outage_hours) AS cumulative_outage_hours,
            SUM(commercial_customers) AS cumulative_commercial_customers
    FROM project.psps_outages_2013_2023_simplified
    GROUP BY circuit_name)
SELECT  circuits.coabdis_id,
        circuits.utility AS target_utility,
        circuits.utility AS match_utility,
        circuits.circuit_name AS target_circuit_name,
        product.circuit_name  AS match_circuit_name,
        (circuits.circuit_name <-> product.circuit_name) AS match_similarity_score,
        circuits.line_distance_proportion,
        product.cumulative_outage_hours,
        product.cumulative_commercial_customers
INTO project.circuit_psps_join
FROM project.co_ab_dis_circuit_line_distance_proportions AS circuits
CROSS JOIN LATERAL 
    (SELECT * 
        FROM outages
        ORDER BY circuits.circuit_name <-> outages.circuit_name ASC
        LIMIT 1) AS product;

-- Filter records based upon match similarity
UPDATE project.circuit_psps_join
SET cumulative_outage_hours = NULL
WHERE match_similarity_score > 0.5;

UPDATE project.circuit_psps_join
SET cumulative_commercial_customers = NULL
WHERE match_similarity_score > 0.5;

-- Add cumulative score field
ALTER TABLE project.circuit_psps_join
ADD COLUMN cumulative_outage_score NUMERIC;

UPDATE project.circuit_psps_join
SET cumulative_outage_score = cumulative_outage_hours * line_distance_proportion;

-- Generate result output with geospatial field for debugging
WITH 
product AS (
    SELECT  res.coabdis_id,
            SUM(res.cumulative_outage_score) AS cumulative_outage_score
    FROM project.circuit_psps_join AS res
    GROUP BY res.coabdis_id)
SELECT  product.*,
        co_ab_dis.geom
INTO project.circuit_psps_result
FROM product
RIGHT JOIN boundary.ca_co_ab_dis AS co_ab_dis
    ON product.coabdis_id = co_ab_dis."coabdis_id";

-- NULL Negative values
UPDATE project.circuit_psps_result
SET cumulative_outage_score = NULL
WHERE cumulative_outage_score < 0;