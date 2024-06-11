-- Execute the following code on the Database Server in the IOUs database

SELECT  dict."ceus_subsector" AS "ceus_subsector",
    ST_UNION(ST_BUFFER(mp."geom", 200)) AS geom,
    COUNT( DISTINCT mp."geohash19") AS megaparcels_count
INTO temp.landuse_buffer
FROM corelogic.corelogic_20240126_varchar_megaparcels AS mp
JOIN crosswalk.corelogic_landuse_code_to_ceus_sector_dictionary AS dict
    ON mp."land use code _ piq" = dict."corelogic_universal_landuse_code"::TEXT
WHERE   dict."ceus_subsector" NOT IN (
	'Forestry',
	'Residential',
	'National Security',
	'Mining & Extraction',
	'Industrial',
	'Ag & Pumping',
	'Fishing',
	'TCU') AND
	dict."ceus_subsector" IS NOT NULL
GROUP BY dict."ceus_subsector";

CREATE INDEX landuse_buffer_geom_id
    ON temp.landuse_buffer
    USING GIST (geom);

SELECT ST_CENTROID(mp.geom) AS centroid,
   mp."universal building square feet",
   CASE WHEN ces."ciscorep" >= 75.0 THEN TRUE ELSE FALSE END AS dac
INTO temp.residential_parcels
FROM corelogic.corelogic_20240126_varchar_megaparcels AS mp
JOIN geo.calenviroscreen40_gdb AS ces
    ON ST_INTERSECTS(ST_CENTROID(mp."geom"), ces."geom")
WHERE mp."land use code _ piq" IN ('100',
                                    '102',
                                    '109',
                                    '135',
                                    '137',
                                    '138',
                                    '148',
                                    '160',
                                    '163',
                                    '111',
                                    '112',
                                    '116',
                                    '117',
                                    '199',
                                    '115',
                                    '151',
                                    '165',
                                    '103',
                                    '106',
                                    '131',
                                    '132',
                                    '133',
                                    '167');

CREATE INDEX residential_parcels_centroid_idx
    ON temp.residential_parcels
    USING GIST(centroid);

SELECT  lb."ceus_subsector",
        res_parcels."dac",
        ST_UNION(res_parcels.centroid) AS "geom",
        COUNT(DISTINCT res_parcels.*) AS "nearby_residential_property_count",
        SUM(res_parcels."universal building square feet") AS "nearby_residential_property_square_footage"
INTO project.carb_ceus_sector_residential_exposure_dac_status
FROM temp.landuse_buffer AS lb
CROSS JOIN LATERAL
    (SELECT * FROM temp.residential_parcels AS rp WHERE ST_INTERSECTS(lb."geom", rp."centroid")) AS res_parcels
GROUP BY lb."ceus_subsector", res_parcels."dac";
