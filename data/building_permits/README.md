# Import Building Permit Data

These scripts import building permit data prepared by Nicole Matteson for a CARB project.

Data for many cities and counties, standardized to CSV format with a common set of fields, is currently located in `V:\PIER_Data\Nicole_Matteson\Building_Permit_Data\3_permit-processing`.

The files should first be copied to the database server (e.g. using WinSCP) for import.

## Columns

* permit_number
* project_description
* permit_class
* permit_type
* estimated_cost [money]
* applied_date [date]
* issued_date [date]
* finaled_date [date]
* address
* parcel_number
* latitude [float8] -- Used to construct centroid then dropped.
* longitude [float8] -- Used to construct centroid then dropped.
* file_name
* centroid_4326 [geometry(POINT, 4326)] -- Constructed from latitude and longitude columns.
* centroid [geometry(POINT, 3310)] -- Transformed from latitude and longitude columns.

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
