# Data Sources

Building permit data pertaining to electrical service panel upgrades and other related work were manually collected from 56 different municipalities throughout the state. These data were accessed by visiting publicly available online permit data web-portals. It was not known prior to this data collection effort how many and which municipalities throughout the state would have such information available. Consequently, the spreadsheet linked below summarizes the list of municipalities which were searched, provides links to associated permit data web-portals (where available), and gives useful metadata about the scope of the permit information that was obtained.

[Permit Data Collection Effort Tracking Spreadsheet](https://docs.google.com/spreadsheets/d/1nkXlNXpIOpRlNw8PWiE40KRpJvN2Hdx-fROsmdRQd5Q/edit#gid=485054375)

Each row of this spreadsheet is highlighted with a specific color based on two components: 1. Building permit data availability, and 2. Which method (open data portal, permit tracking portal system, PDF) the permit data is available. The key is below:

- SB 535 Disadvantaged Community (County)
- Municipality has Permit Data in PDF Format
- Municipality has Permit Data in Open Data Portal
- Municipality has Permit Data in Permit Tracking Portal System
- SB 535 Priority Community with no available data on permits

# Data Overview

This building permit dataset was prepared by Nicole Matteson, a staff research analyst at CCSC.

## Detailed Methods

### Search Prioritization

Our objective was to develop a database of panel upgrade and electrification building permits for as representative a sample of California's geographies and demographics as possible. This data set would later be used to train a machine learning model capable of predicting installed electrical service panel sizes (amps) for the state's residential building stock.

To structure our permit data search process, we began by ranking the list of the state's counties and cities by their population size. Our experience has shown that population sizes correlate strongly with the volume tax revenues collected by municipalities and thus, the available financial resources for developing and maintaining sophisticated digital data collection and hosting infrastructure.

To ensure sufficient representation for historically underserved populations, we also incorporated SB 535 data from CalEnviroscreen 4.0 into our search ranking criteria. Counties that had SB 535 DAC census tracts within their boundaries were prioritized in finding building permit data.

### Permit Record Types

Different municipalities collect different types of attribute information as part of their permitting processes. Additionally, there can be important differences in the way that these attributes have been assembled into published data products as well as in the ways in which these data products can be selected/filtered in data download web-portals between municipalities. In order to find building permits that were related to electric panel upgrades, we used a combination of thematical filtering and keyword searches, where approrpriate, depending upon the combination of these factors.

For permit record type keyword searches, the following terms were used:

- Electrical, Residential Electrical (Res elec), Commercial Electrical (Com elec), Residential Alteration (res alt), Commercial Alteration (com alt), OTC (over the counter), No plan permits (permits that do not require detailed plans), Simple permits, Express permits, PV permit, EV permit, Panel upgrade, MPU (main panel upgrade), Service upgrade, Utility permit, Residential, Building, Commercial.
- If the building permit portal did not provide a query to specify permit type, we used the Record ID query and searched: B (for building permit- some Record ID’s start with B), R (for residential), C (for commercial)
- Dates: Dates ranged from 1950 to present

### Access Patterns

Permit data were access according to one of the following three mechanisms: open data portals, building permit websites, and publicly accessible APIs.  Some municipalities have online permit tracking systems where records can be queried. An in depth process and description of these portals is addressed in the following section.

There are commercial software solution providers which specialize in building permit data tracking and management systems. The two biggest of which are Accela and eTRAKit. The standard products offerred by these companies provided a degree of consistency across municipalities which used them. For example, many permit data download sites provided a query section that allowed the user to search by 1. Record ID, 2. Start Date/End Date, 3. Parcel Number, 4. Street Number, 5. Street Name, 6. City. Differences most commonly ocurred with respect to the options for: 1. Permit Record Type, 2. Record Subtype, 3. Record Status, 4. Project Name, 6. License Type and State License Number, 7. The ability to download the datasets. This last point was very important because while many municipalities had the data we were looking for, they did not provide an option to download the data.

Below describes the general process for searching for and downloading building permit data from a building permit tracking system:

- Accela
  - Starting at home page -> Advanced search -> Search records/applications-> Building-> Record type (if given option)-> From (date) -> Download results
- eTRAKit
  - Starting at home page -> Search By -> Permit Type/Permit Subtype/Record ID -> “contains” -> *fill in* -> check for address, project description -> Download Results
- Other
  - The first step is to look at the query options. Sometimes there was also a button that said “advanced search” and this would provide more specific queries. In other cases, the same steps as above were adapted on the basis of what functionality was available.

If no open data or online building permit tracking system existed, then an unstructured web search was conducted on "building permit data" or "building permit report" for the municipality in question. Some were found to have pdf's or csv's of the data, while others did not appear to make anything publicly available in any format. These municipalities have been highlighted in light yellow in the tracking spreadsheet.

### Summary Results

Our sample consists of the cities and counties in California whose building permit data met the following criteria:
   - Was able to be downloaded as .csv, .json, or .geojson
   - Permit data included a project description
   - Permit data included an address, APN, or coordinates

Overall, 162 municipalities were checked for publicly available building permit data. 56 municipalities met all of the aforementioned requirements (see table 1.). Nintey-four municipalities had building permit data but did not meet our requirements. Their data was either not possible to download (there was no “download” button), the query system required specific entries (only searchable by address, APN, complete permit number), the query system required an account, or there was an error downloading the records.  Lastly, twenty-five out of the nintey-four municipalities only had their building permit data available in PDF format. These municipalities are not included in our sample. Twelve municipalities did not have any type of permit data available on line.

There are multiple raw data files that were collected for some municipalities because there may have been different permit record types that had information on panel upgrades (ex. electrical permits and PV permits). Each raw CSV source file represents a permit record type for that municipality. Any given permit can only be one permit record type. This means that a Residential Solar permit cannot also be a Residential Electricity permit. It may happen that a particular project has multiple related permits, but the scope of work for each permit will be different. All of the raw datafiles have been named with either the “City_” or “County_” prefix following by the name of the municipality, and then a way to denote what type of permits are in that file. The following abbreviations were utilized to codify data files:

- EV: Electric Vehicle
- PV: Photovoltaic
- ESU: Electrical Service Upgrade
- MPU: Main Panel Upgrade
- EPM: Electrical, Plumbing, Mechanical permit type
- Finaled: The project has had all its inspections and is complete
- Issued: Permit was issued but still needs inspections
- Com: Commercial
- Res: Residential

## Data Post-Processing

Individual raw data files were collated into a single combined csv file for each municipality using customized python scripts. During this process, field names were standardized and records with corrupted or missing attributes were dropped as necessary. The database import workflow documented in this portion of the repository operates over these post-processed CSV files to generate a single unified permit record table in the database. The structure of this table is documented in the data-dictionary for the "permits.combined_raw" table below.

### Class Definition Standardization

Within the scope of each municipality, permit "class" designation fields were deemed of interest. However, upon inspection it became obvious that there were a wide range of class values used between the different data providers. An effort to standardize these disparate class fields into a single, property usetype based, classification scheme was undertaken. This involved generating a list of all of the unique class values that appeared across all of the data sets and manually deriving a dictionary mapping them to a simplified and standardized set.

### Panel Upgrade Filtering

While efforts were made during the initial raw data collection effort to constrain the scope of the permits being collected to just those which pertained to panel upgrades and other associated electrification measures - a significant number of unrelated permits were included in the raw data. Thus, an effort was undertaken to flag relevant permits on the basis of keywords within their work description fields. This process resulted in individual permits being assigned a boolean flag (True/False) for each of the following measure type categories:

- Main Panel Upgrade
- Sub-panel Upgrade
- Solar PV System
- Heat Pump HVAC System
- EV Charger
- Battery Energy Storage System (BESS)

Note: While heat pump hot water heaters represent an important electrification measure, their power demand is not typically such that we would expect them to necessarily result in the need for a main service panel upgrade, in most cases. Consequently, the decision was made to exclude them here from this list - which is focused on measures that nearly always require an upgraded service panel to be installed.

### Address Geocoding

While a number of municipalities did provide latitude longitude coordinates of the parcels associated with their permit records, most did not. For these, latitude longitude coordinate pairs had to be derived by either geocoding provided address information fields or joining to a separate parcel boundary dataset via the provided Assessor Parcel Number (APN). Additionally, for a number of municipalities, the provided address fields in the raw data were found to be incomplete (i.e. missing the county designation as it was implied within the scope of the original dataset). This meant that some preprocessing was required before geocoding could proceeed. Overall, 300,000+ of the filtered panel upgrade permit records had to be geocoded using a python script that called the ArcGIS geocoder API. This geocoder provides a geocoding qaulity score (0-100) that was used, in combination with a state boundary mask, to filter out permits with obviously incorrect geocoding results.

# Data Dictionary

## Table: permits.combined

This table contains the raw collated permit data assembled from all the sampled municipalities - prior to any subsequent filtering or post-processing operations.

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
| solar_pv_system | Boolean field indicating solar PV system reference in work description |
| battery_storage_system | Boolean field indicating battery energy storage system reference in work description |
| ev_charger | Boolean field indicating EV charger reference in work description |
| heat_pump | Boolean field indicating heat pump system reference in work description |
| main_panel_upgrade | Boolean field indicating main electrical service panel upgrade reference in work description |
| sub_panel_upgrade | Boolean field indicating electrical sub-panel upgrade reference in work description |
| upgraded_panel_size | Size of destination main/sub panel following upgrade (where mentioned in work description) |

## Table: permits.class_definitions

This table contains a manually defined dictionary which is used for translating raw permit class designations into a more limited and standardized set.

| Data Field | Definition |
|------------|------------|
| ogc_fid | Serial ID (Automatically generated on import |)
| permit_class | Permit classification field value in raw dataset |
| permit_class_std | Mapping to standardized permit classification value |

## Table: permits.panel_upgrades

This table contains a filtered subset of permits that were deemed to be associated with panel upgrades as based upon the content of their work description field. The table includes, as a set of boolean fields, indicators of what relevant measures were identified in the work description field. The table also contains the output of various address string pre-processing operations designed to improve geocoding performance.

| Data Field | Definition |
|------------|------------|
| permit_number | Permit number provided from each original data provider (no guarantee of uniqueness) |
| project_description | Project work description |
| permit_class | Original permit class designation |
| permit_type | Original permit type designation |
| estimated_cost | Estimated total project cost |
| applied_date | Permit application date |
| issued_date | Permit issuance date |
| finaled_date | Permit finaled date |
| address | Street address |
| parcel_number | Assessor Parcel number (APN) |
| place | Census place/city name designation (Derived) |
| county_name | Census county name designation (Derived) |
| zipcode | 5-digit zipcode |
| file_name | Source filename of associated referenced from database import routine |
| centroid_4326 | ESPG: 4326 formatted latitude longitude centroid point |
| centroid | EPSG: 3310 formatted X/Y centroid point |
| id | Globally unique UUID for permit record (Derived) |
| solar_pv_system | Solar PV System measure boolean flag |
| battery_storage_system | Battery Energy Storage System (BESS) measure boolean flag |
| ev_charger | EV Charger boolean flag |
| heat_pump | Heat-Pump HVAC system boolean flag |
| main_panel_upgrade | Main electrical service panel upgrade boolean flag |
| sub_panel_upgrade | Electrical service sub-panel upgrade boolean flag |
| upgraded_panel_size | Destination panel size (where available) |
| valid_centroid | Valid centroid determination boolean flag |
| address_clean | Concatenated address string fields for address standarization/normalization |
| sa | Standardized address type formatted address information |
| na | Normalized address type formatted address information |
| query_address | Final formatted address string to be submitted to the geocoder |

## Table: permits.panel_ugprades_geocode_arcgis

This table contains response information obtained from the ArcGIS geocding service. The scope of the permit records covered in this table only includes those for which a valid centroid was missing in the original data.

| Data Field | Definition |
|------------|------------|
| id | Globally unique UUID for permit record (Derived) |
| query_address | Final formatted address string to be submitted to the geocoder |
| centroid | EPSG: 3310 formatted X/Y coordinate pair for the query_address returned from geocoder |
| address | Geocoder match address |
| raw | Raw geocoder JSON response payload |
| score | Geocder match quality score (0-100) |

## Table: permits.panel_upgrades_geocoded

This table reflects a consolidation of the records in the filtered panel upgrade permit table with the geocoding results table. It also contains a foreign key linkage to ZTRAX parcel record derived megaparcel table.

| Data Field | Definition |
|------------|------------|
| id | Globally unique UUID for permit record (Derived) |
| permit_number | Permit identification number (unique within the scope of each reporting entity) |
| permit_class | Permit classification |
| permit_type | Permit type |
| estimated_cost | Estimated total project cost |
| applied_date | Permit application date |
| issued_date | Permit issuance date |
| finaled_date | Permit finaled date |
| solar_pv_system | Solar PV System measure boolean flag |
| battery_storage_system | Battery Energy Storage System (BESS) measure boolean flag |
| ev_charger | EV Charger boolean flag |
| heat_pump | Heat-Pump HVAC system boolean flag |
| main_panel_upgrade | Main electrical service panel upgrade boolean flag |
| sub_panel_upgrade | Electrical service sub-panel upgrade boolean flag |
| upgraded_panel_size | Destination panel size (where available) |
| parcel_number | Assessor Parcel Number |
| address | Street Address |
| query_address | Final formatted address string to be submitted to the geocoder |
| match_address | Geocoder match address |
| centroid | EPSG: 3310 formatted X/Y centroid point with Null values in original data filled from Geocoding results |
| megaparcelid | ZTRAX derived megaparcel table serial ID (foreign key) |

## Table: permits.panel_upgrades_geocoded_geographies

This table contains a set of contextual attributes for each permit record that have been derived from spatial joins against its centroid location.

| Data Field | Definition |
|------------|------------|
| id | Globally unique UUID for permit record (Derived) |
| place_name | Place Name with translated Legal/Statistical Area Description
| county_name | County Name with translated Legal/Statistical Area Description
| dac | CES-4.0 Disadvantaged Community boolean flag |
| low_income | CARB Priority Population low income community boolean flag |
| non_designated | CARB Priority Population non-designated community boolean flag |
| buffer_low_income | CARB Priority Population buffer low-income community boolean flag |
| bufferlih | CARB Priority Populations buffer low-income household eligible boolean flag |
| tract_geoid_2019 | 2019 Census Tract Geometry Geogrpahic Identification Code |
| megaparcelid | ZTRAX megaparcel serial ID |

## Table: permits.sampled_counties

This table contains a list of the counties for which permit data was accessed.

| Data Field | Definition |
|------------|------------|
| STATEFP | State FIPS Code |
| COUNTYFP | County FIPS Code |
| COUNTYNS | ANSI County Code |
| GEOID | Geographic Identification Code |
| NAME | County Name |
| NAMELSAD | County Name with translated Legal/Statistical Area Description |
| LSAD | Legal/Statistical Area Description Code |
| CLASSFP | Class FIPS Code |
| MTFCC | MAF/Tiger Feature Class Code |
| CSAFP | Geographic Entity Class Code |
| CBSAFP | Core Based Statistical Area |
| METDIVFP | Metropolitan division code |
| FUNCSTAT | Functional Status Code |
| ALAND | Land Area |
| AWATER | Water Area |
| INTPTLAT | Latitude of the Internal Point |
| INTPTLON | Longitude of the Internal Point |
| geometry | Geometry |
| union_code | Boolean value used for spatial union operation |

## Table: permits.sampled_places

This table contains a list of the census designated place

| Data Field | Definition |
|------------|------------|
| STATEFP | State FIPS Code |
| PLACEFP | Place FIPS Code |
| PLACENS | Place ANSI Code |
| GEOID | Geographic Identification Code |
| NAME | Place Name |
| NAMELSAD | Place Name with translated Legal/Statistical Area Description |
| LSAD | Legal/Statistical Area Description Code |
| CLASSFP | Class FIPS Code |
| PCICBSA | Current metropolitan or micropolitan statistical area principal city indicator |
| PCINECTA | Current Census Designated Place Principal City Indicator |
| MTFCC | MAF/Tiger Feature Class Code |
| FUNCSTAT | Functional Status Code |
| ALAND | Land Area |
| AWATER | Water Area |
| INTPTLAT | Latitude of the Internal Point |
| INTPTLON | Longitude of the Internal Point |
| geometry | Geometry |
| union_code | Boolean value used for spatial union operation |

## Table: permits.sampled_territories

This table contains a unified polygon geometry which represents all of the combined sampled places and counties.

| Data Field | Definition |
|------------|------------|
| geometry | Geometry |
| union_code| Boolean value used for spatial union operation |

## Database Import Notes

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
