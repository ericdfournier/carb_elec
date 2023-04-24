-- Drop Extraneous Air District Layer Fields
ALTER TABLE carb.ca_air_districts
DROP COLUMN objectid;

ALTER TABLE carb.ca_air_districts
DROP COLUMN area;

ALTER TABLE carb.ca_air_districts
DROP COLUMN perimeter;

ALTER TABLE carb.ca_air_districts
DROP COLUMN caaba_;

-- Drop Extraneous Air Basins Layer Fields
ALTER TABLE carb.ca_air_basins
DROP COLUMN objectid;

ALTER TABLE carb.ca_air_basins
DROP COLUMN area;

ALTER TABLE carb.ca_air_basins
DROP COLUMN perimeter;

ALTER TABLE carb.ca_air_basins
DROP COLUMN caaba_;
