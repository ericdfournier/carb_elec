-- Select cca Cities
SELECT A.city_name AS geog_name,
       A.cca_name AS cca_name,
       'city' AS geo_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO cca.places_geom
FROM cca.places AS A
LEFT JOIN census.acs_ca_2019_place_geom AS B
ON A."city_name" = B."NAME";

-- Select cca Unincorporated Areas
SELECT A.unincorporated_name AS geog_name,
       A.cca_name AS cca_name,
       'unincorporated_area' AS geo_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO cca.unincorporated_areas_geom
FROM cca.unincorporated_areas AS A
LEFT JOIN census.acs_ca_2019_unincorporated_geom AS B
ON A."unincorporated_name" = B."NAME";

-- Select cca Unincorporated Areas and Cities within Counties
SELECT A.county_name AS geog_name,
       A.cca_name AS cca_name,
       'county' AS geom_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO cca.counties_geom
FROM cca.counties AS A
LEFT JOIN census.acs_ca_2019_county_geom AS B
ON A."county_name" = B."NAME";

-- Union Subselected Areas
CREATE TABLE cca.all_merged AS (
SELECT * FROM cca.places_geom
UNION
SELECT * FROM cca.counties_geom
UNION
SELECT * FROM cca.unincorporated_areas_geom);

-- Add table description
COMMENT ON TABLE cca.all_merged IS 'all geometries merged';

-- Drop intermediate tables
DROP TABLE cca.places,
       cca.places_geom,
       cca.counties,
       cca.counties_geom,
       cca.unincorporated_areas,
       cca.unincorporated_areas_geom;
