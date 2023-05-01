-- Select REN Cities
SELECT A.city_name AS geog_name,
       A.ren_name AS ren_name,
       'city' AS geo_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO ren.places_geom
FROM ren.places AS A
LEFT JOIN census.acs_ca_2019_place_geom AS B
ON A."city_name" = B."NAME";

-- Select REN Unincorporated Areas
SELECT A.unincorporated_name AS geog_name,
       A.ren_name AS ren_name,
       'unincorporated_area' AS geo_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO ren.unincorporated_areas_geom
FROM ren.unincorporated_areas AS A
LEFT JOIN census.acs_ca_2019_unincorporated_geom AS B
ON A."unincorporated_name" = B."NAME";

-- Select REN Unincorporated Areas and Cities within Counties
SELECT A.county_name AS geog_name,
       A.ren_name AS ren_name,
       'county' AS geo_type,
       B."GEOID" AS geoid,
       B.geometry AS geometry
INTO ren.counties_geom
FROM ren.counties AS A
LEFT JOIN census.acs_ca_2019_county_geom AS B
ON A."county_name" = B."NAME";

-- Union Subselected Areas
CREATE TABLE ren.all_merged AS (
SELECT * FROM ren.places_geom
UNION
SELECT * FROM ren.counties_geom
UNION
SELECT * FROM ren.unincorporated_areas_geom);

-- Add table description
COMMENT ON TABLE ren.all_merged IS 'all geometries merged';

-- Drop intermediate tables
DROP TABLE ren.places,
       ren.places_geom,
       ren.counties,
       ren.counties_geom,
       ren.unincorporated_areas,
       ren.unincorporated_areas_geom;
