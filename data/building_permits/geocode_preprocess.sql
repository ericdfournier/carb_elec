-- Update missing or invalid centroids with parcel centroids where available
UPDATE permits.panel_upgrades
SET centroid = ST_CENTROID(B.geom)
FROM sgc.ca_parcel_boundaries_2014 AS B
WHERE parcel_number = B.parno AND
    (valid_centroid = FALSE OR
    ST_ISEMPTY(centroid));

-- Add clean receiver field
ALTER TABLE permits.panel_upgrades
ADD COLUMN address_clean TEXT;

-- Set initial values
UPDATE permits.panel_upgrades
SET address_clean = address;

-- Replace 'None' with 'San Francisco County'
UPDATE permits.panel_upgrades
SET address_clean = REPLACE(address, 'None', ' ')
WHERE file_name = 'city_county-san_fran-final.geojson';

-- Append 'Elk Grove, CA' to the end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Elk Grove, CA'
WHERE file_name = 'city-elk_grove-final.csv';

-- Append 'Fairfield, CA' to the end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Fairfield, CA'
WHERE file_name = 'city-fairfield-final.csv';

-- Remove '.0' from string and Append 'Garden Grove, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = REPLACE(address, '.0', '') || ' Garden Grove, CA'
WHERE file_name = 'city-garden_grove-final.csv';

-- Append 'Hanford, CA' to the end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Hanford, CA'
WHERE file_name = 'city-hanford-final.csv';

-- Remove '.0' from string and append 'Los Angeles, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = REPLACE(address, '.0', '') || ' Los Angeles, CA'
WHERE file_name = 'city-los_angeles-final.csv';

-- Replace 'MORV' in string with 'Moreno Valley, CA'
UPDATE permits.panel_upgrades
SET address_clean = REPLACE(address, 'MORV', 'Moreno Valley')
WHERE file_name = 'city-moreno_valley-final.csv';

-- Append 'Oceanside, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Oceanside, CA'
WHERE file_name = 'city-oceanside-final.csv';

-- Remove 'SFR' and 'ADU' from string and append 'Pasadena, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = REPLACE(REPLACE(address, 'SFR', ''), 'ADU', '') || ' Pasadena, CA'
WHERE file_name = 'city-pasadena-final.geojson';

-- Append 'Richmond, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Richmond, CA'
WHERE file_name = 'city-richmond-final.csv';

-- Append 'Riverside, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Riverside, CA'
WHERE file_name = 'city-riverside-final.csv';

-- Append 'San Rafael, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' San Rafael, CA'
WHERE file_name = 'city-san_rafael-final.csv';

-- Replace escape carriage character with an empty space in string and remove text between parenthesis
UPDATE permits.panel_upgrades
SET address_clean = REGEXP_REPLACE(REGEXP_REPLACE(address, '[\n\r]+', ' '), '\([^)]*\)', '')
WHERE file_name = 'city-santa_monica-final.csv';

-- Append 'El Dorado, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' El Dorado, CA'
WHERE file_name = 'county-el_dorado-final.csv';

-- Append 'Placer County, CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' Placer County, CA'
WHERE file_name = 'county-placer-final.geojson';

-- Append 'CA' to end of string
UPDATE permits.panel_upgrades
SET address_clean = address || ' CA'
WHERE file_name = 'county-riverside-final.csv';

-- Append 'Yolo County, CA'
UPDATE permits.panel_upgrades
SET address_clean = address || ' Yolo County, CA'
WHERE file_name = 'county-yolo-final.csv';

-- Add generated column for stdaddr.
-- This form of standardize_address uses micro and macro parameters.
-- The tables from address_standardizer_data_us ('us_lex', 'us_gaz', 'us_rules') could also be used.
alter table permits.panel_upgrades
    add sa stdaddr generated always as (
        standardize_address(
            'tiger.pagc_lex', 'tiger.pagc_gaz', 'tiger.pagc_rules',
            address_clean
        )
    ) stored;

-- Create function to convert staddr to norm_addy type.
create or replace function norm_addy(sa stdaddr) returns norm_addy as
$$
declare
    result norm_addy;
begin
    result.parsed := false;
    result.zip4 := null;
    -- For address number only put numbers and stop if reach a non-number e.g. 123-456 will return 123.
    result.address := to_number(substring(sa.house_num, '[0-9]+'), '99999999');
    result.address_alphanumeric := sa.house_num;
    -- Get rid of extraneous spaces before we return.
    result.zip := sa.postcode;
    result.streetname := trim(sa.name);
    result.location := trim(sa.city);
    result.stateabbrev := trim(sa.state);
    -- This should be broken out separately like pagc, but normalizer doesn't have a slot for it
    result.streettypeabbrev := trim(coalesce(sa.suftype, sa.pretype));
    result.predirabbrev := trim(sa.predir);
    result.postdirabbrev := trim(sa.sufdir);
    result.internal := trim(regexp_replace(replace(sa.unit, '#',''), '([0-9]+)\s+([a-za-z]){0,1}', E'\\1\\2'));
    result.parsed := true;
    return result;
end
$$ language plpgsql stable strict;

-- Create a cast using the new function, so that cast() or :: may be used.
create cast (stdaddr as norm_addy)
    with function norm_addy(stdaddr);

--------------------------------------------------------------------------------
-- Add na norm_addy column with normalized address derived from sa stdaddr
--
-- Custom permits.sa_to_na funtion used.
-- Ignore internal/unit field since it is not important for geocoding.
--------------------------------------------------------------------------------

-- Add column for norm_addy.
alter table permits.panel_upgrades
    add na norm_addy;

-- Set values in na column.
-- Drop internal field by setting to null. The unit number is not important for geocoding.
update permits.panel_upgrades
    set na = sa::norm_addy;

--------------------------------------------------------------------------------
-- Create column to store output of pprint_addy
--------------------------------------------------------------------------------

-- Add column for pprint_addy.
alter table permits.panel_upgrades
    add query_address varchar;

-- Set pretty values where address standardization did not obviously fail.
-- This is still no guarantee that they were parsed correctly.
-- Sometimes standardize_address returns a stdaddr with all null fields (even with the method
-- of concatenating address1 + postal and adding city + state, since they are absent from the data set).
-- These can be detected by "where not sa is null" (note this is not the same as "where sa not is null").
-- Sometimes pprint_addy returns the emptry string (never null), and tests showed that these
-- are exactly those with all null stdaddr (at least for this data set).
-- The nullif is not strictly necessary.
update permits.panel_upgrades
    set query_address = nullif(pprint_addy(na), '')
    where not sa is null;
