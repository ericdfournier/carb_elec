# Data Source

Various, See below.

# Data Overview

This building permit dataset was prepared by Nicole Matteson for a CARB project. The methods by which these records where acquired will documented in detail in a separate reporting deliverable. The data acquisition process involved manually visiting city and county permitting department websites and data hosting platforms. Detailed records were assembled for each available geography and then later programmatically filtered and assembled into a unified dataset.

# Data Dictionary

Table: permits.combined_raw

| Data Field | Definition |
|------------|------------|
| permit_number | Permit identification number (unique within the scope of each reporting entity) |
| project_description | Free form, applicant generated, description of the permitted work project |
| permit_class | Permit classification |
| permit_type | Permit type |
| estimated_cost | Estimated total project cost |
| applied_date | Permit application date |
| issued_date | Permit issue date |
| finaled_date | Permit final date |
| address | Address string |
| parcel_number | Assessor parcel identification number (unique within the scope of each reporting entity) |
| file_name | Source file name for import |
| centroid_4326 [geometry(POINT, 4326)] | Geographic coordinate system point location (Constructed from latitude and longitude columns) |
| centroid [geometry(POINT, 3310)] | Projected coordinate system point location (Transformed from latitude and longitude columns) |

## Import Notes

Default autodetection (`-oo AUTODETECT_TYPE=YES`) generates the following warnings:

```
# county-nevada-clean.csv
Warning 1: Invalid value type found in record 8117 for field permit_number. This warning will no longer be emitted.
# Caused by text (e.g. "-") in an otherwise numeric field.
```

and

```
# county-sacramento-clean.csv
# Warning 1: Invalid value type found in record 23148 for field parcel_number. This warning will no longer be emitted.
# Caused by text (e.g. "TEST") in an otherwise numeric field.
```

Adding `-oo AUTODETECT_SIZE_LIMIT=2147483647` will sufficiently increase the the number of bytes to inspect so the correct data type is properly inferred for each file. However, some columns (notably permit_number and parcel_number) are numeric in some municipalities but contain additional characters in others.

To assure consistency between tables, instead of using autodetection it is better to specify the column types of the output tables using `-lco COLUMN_TYPES='estimated_cost=money,applied_date=date,issued_date=date,finaled_date=date'`. The other columns default to text (`varchar`).

At least one file contains invalid coordinates that prevent transformation to NAD83 / California Albers on `ogr2ogr` import using the `-t_srs` option:

```
# city-san_diego-final-clean.csv
ERROR 1: latitude or longitude exceeded limits
ERROR 1: Failed to reproject feature 9008 (geometry probably out of source or destination SRS).
# Caused because some latitude and longitudes are swapped and some are wildly out of range (possibly another CRS).
```

This is handled by importing centroid as EPSG:4326 (WGS84) and then transforming only valid coordinates to EPSG:3310 (NAD83 / California Albers) in postprocessing.
