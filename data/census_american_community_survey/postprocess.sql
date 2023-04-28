-- Drop Extraneous Unicorporated Area Geometry Layer Fields
ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN statefp_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN geoid_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN name_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN namelsad_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN lsad_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN classfp_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN mtfcc_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN funcstat_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN aland_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN awater_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN intptlat_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN intptlon_2;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN ogc_fid;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN placefp;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN placens;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN pcicbsa;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
DROP COLUMN pcinecta;

-- Rename remaining valid fields
ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN statefp TO STATEFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN countyfp TO COUNTYFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN countyns TO COUNTYNS;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN geoid TO GEOID;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN name TO NAME;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN namelsad TO NAMELSAD;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN lsad TO LSAD;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN classfp TO CLASSFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN mtfcc TO MTFCC;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN csafp TO CSAFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN cbsafp TO CBSAFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN metdivfp TO METDIVFP;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN funcstat TO FUNCSTAT;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN aland TO ALAND;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN awater TO AWATER;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN intptlat TO INTPTLAT;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN intptlon TO INTPTLON;

ALTER TABLE census.acs_ca_2019_tr_unincorporated_geom
RENAME COLUMN geom TO geometry;
