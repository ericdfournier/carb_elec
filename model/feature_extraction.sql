-- Add centroid geometry field
ALTER TABLE ztrax.main 
ADD COLUMN centroid GEOMETRY(point, 3310);

-- Generate Centroid from Existing Latitude Longitude Coordinates
UPDATE ztrax.main 
SET centroid = ST_TRANSFORM(ST_SETSRID(ST_MAKEPOINT(
    "PropertyAddressLongitude", "PropertyAddressLatitude"), 4326), 3310); 

-- Index the Ztrax centroid geometry field
CREATE INDEX IF NOT EXISTS idx_us_main_centroid_idx
ON ztrax.main
USING gist (centroid);

-- Index the shoreline geometry linestring prior to runnning calculation
CREATE INDEX IF NOT EXISTS idx_us_medium_shoreline_geom_idx
ON noaa.us_medium_shoreline
USING gist (geom);

-- Compute the distance to shore from each parcel centroid
SELECT DISTINCT parcels."RowID",
    (SELECT FLOOR(ST_Distance(parcels.centroid, shoreline.geom))::INTEGER
        FROM   noaa.us_medium_shoreline AS shoreline
        ORDER BY
            parcels.centroid <-> shoreline.geom
        LIMIT  1) AS shorelinedistm
INTO ztrax.distance
FROM ztrax.main AS parcels;

-- Compute the elevation of each parcel centroid using a cross lateral join
SELECT DISTINCT parcels."RowID",
       elevation.elevationm
INTO    ztrax.elevation
FROM    ztrax.main AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS elevationm
        FROM srtm.ca_elevation
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS elevation;

-- Compute the slope at each parcel centroid using a cross lateral join
SELECT DISTINCT parcels."RowID",
       slope.slopepct
INTO    ztrax.slope
FROM    ztrax.main AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_Value(rast, parcels.centroid))::INTEGER AS slopepct
        FROM srtm.ca_slope
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS slope;

-- Compute the aspect at each parcel centroid using a cross lateral join
SELECT DISTINCT parcels."RowID",
        aspect.aspectdeg
INTO ztrax.aspect
FROM ztrax.main AS parcels
CROSS JOIN LATERAL
    (SELECT FLOOR(ST_VALUE(rast, parcels.centroid))::INTEGER AS aspectdeg
        FROM srtm.ca_aspect
        WHERE ST_INTERSECTS(parcels.centroid, rast)) AS aspect;
    
-- Index Join Tables on RowID
CREATE INDEX IF NOT EXISTS idx_training_rowid_idx
ON la100.sf_training (rowid);

CREATE INDEX IF NOT EXISTS idx_main_rowid_idx
ON ztrax.main ("RowID");

CREATE INDEX IF NOT EXISTS idx_building_rowid_idx
ON ztrax.building ("RowID")

CREATE INDEX IF NOT EXISTS idx_building_areas_rowid_idx
ON ztrax.building_areas ("RowID");

CREATE INDEX IF NOT EXISTS idx_value_rowid_idx
ON ztrax.value ("RowID");

CREATE INDEX IF NOT EXISTS idx_distance_rowid_idx
ON ztrax.distance ("RowID");

CREATE INDEX IF NOT EXISTS idx_elevation_rowid_idx
ON ztrax.elevation ("RowID");

CREATE INDEX IF NOT EXISTS idx_slope_rowid_idx
ON ztrax.slope ("RowID");

CREATE INDEX IF NOT EXISTS idx_aspect_rowid_idx
ON ztrax.aspect ("RowID");

-- Extract Relevant Parcel Attributes for LA Training Data
SELECT  training.rowid,
        training.panel_size_existing::TEXT,
        main."LotSizeSquareFeet",
        main."NoOfBuildings",
        building."NoOfUnits",
        building."PropertyLandUseStndCode",
        building."YearBuilt",
        building."TotalBedrooms",
        building."HeatingTypeorSystemStndCode",
        building."AirConditioningTypeorSystemStndCode",
        areas."BuildingAreaSqFt",
        val."LandAssessedValue"::NUMERIC,
        val."ImprovementAssessedValue"::NUMERIC,
        dist."shorelinedistm",
        elevation."elevationm",
        slope."slopepct",
        aspect."aspectdeg",
        place."NAMELSAD" AS "placename",
        county."NAMELSAD" AS "countyname",
        pp."dac",
        pp."lowincome",
        pp."nondesignated",
        pp."bufferlowincome",
        pp."bufferlih",
        ejscreen."peopcolorpct",
        ejscreen."lowincpct",
        ejscreen."unemppct",
        ejscreen."lingisopct",
        ejscreen."lesshspct",
        ejscreen."under5pct",
        ejscreen."over64pct",
        ejscreen."lifeexppct" 
INTO    la100."sf_training_full"
FROM    la100.sf_training AS training
INNER JOIN ztrax.main AS main
    ON training.rowid = main."RowID"
INNER JOIN ztrax.building AS building
    ON training.rowid = building."RowID"
INNER JOIN ztrax.building_areas AS areas
    ON training.rowid = areas."RowID"
INNER JOIN ztrax.value AS val
    ON training.rowid = val."RowID"
INNER JOIN ztrax.distance AS dist
    ON training.rowid = dist."RowID"
INNER JOIN ztrax.elevation AS elevation
    ON training.rowid = elevation."RowID"
INNER JOIN ztrax.slope AS slope
    ON training.rowid = slope."RowID"
INNER JOIN ztrax.aspect AS aspect
    ON training.rowid = aspect."RowID"
INNER JOIN census.acs_ca_2019_place_geom AS place
    ON ST_INTERSECTS(training."geom", place."geometry")
INNER JOIN census.acs_ca_2019_county_geom AS county
    ON ST_INTERSECTS(training."geom", county."geometry")
INNER JOIN carb.priority_populations_ces4 AS pp
    ON ST_INTERSECTS(training."geom", pp."geom")
INNER JOIN usepa.ej_screen_ca_2023_tr AS ejscreen
    ON ST_INTERSECTS(training."geom", ejscreen."geom");
