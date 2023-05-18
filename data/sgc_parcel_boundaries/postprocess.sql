-- Convert geometries to 2D linear features
alter table sgc.ca_parcel_boundaries_2014
    alter geom type geometry(multipolygon, 3310) using ST_Force2D(ST_CurveToLine(geom));
