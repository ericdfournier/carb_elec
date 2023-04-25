-- Drop Extraneous Unicorporated Area Geometry Layer Fields
ALTER TABLE carb.ca_air_districts
DROP COLUMN statefp_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN geoid_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN name_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN namelsad_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN lsad_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN classfp_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN mtfcc_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN funcstat_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN aland_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN awater_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN intptlat_2;

ALTER TABLE carb.ca_air_districts
DROP COLUMN intptlon_2;
