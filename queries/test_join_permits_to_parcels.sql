CREATE INDEX panel_upgrade_parcel_number_idx ON permits.panel_upgrades (parcel_number);
CREATE INDEX ca_boundaries_parcel_number_idx ON sgc.ca_parcel_boundaries_2014 (parno);

SELECT  A.*,
        B.geom
INTO    permits.test_boundary_join_apn_key
FROM    permits.panel_upgrades AS A,
        sgc.ca_parcel_boundaries_2014 AS B
WHERE   A.parcel_number = B.parno;
        