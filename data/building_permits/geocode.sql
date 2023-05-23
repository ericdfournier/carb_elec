-- Update missing or invalid centroids with parcel centroids where available
UPDATE permits.panel_upgrades
SET centroid = ST_CENTROID(B.geom)
FROM sgc.ca_parcel_boundaries_2014 AS B
WHERE parcel_number = B.parno AND
    (valid_centroid = FALSE OR
    centroid IS NULL);

-- Add generated column for stdaddr.
-- This form of standardize_address uses micro and macro parameters.
-- The tables from address_standardizer_data_us ('us_lex', 'us_gaz', 'us_rules') could also be used.
alter table permits.panel_upgrades
    add sa stdaddr generated always as (
        standardize_address(
            'tiger.pagc_lex', 'tiger.pagc_gaz', 'tiger.pagc_rules',
            address
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
