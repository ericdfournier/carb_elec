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

Our objective was to develop a database of panel upgrade and electrification building permits for as representative sample of California's geographies and demographics as possible. This data set would later be used to train a machine learning model capable of predicting installed electrical service panel sizes (Amps) for the state's residential housing stock.

To structure our permit data search process, we began by ranking the list of the state's counties and cities by their population size. Our experience has shown that population sizes correlate strongly with the volume tax revenues collected by municipalities and thus, the available financial resources for developing and maintaining sophisticated digital data collection and hosting infrastructure.

To ensure sufficient representation for historically underserved populations, we also incorporated SB 535 data from CalEnviroscreen 4.0 into our search ranking criteria. Counties that had SB 535 DAC census tracts within their boundaries were prioritized in finding building permit data.

### Permit Record Types

Different municipalities collect different types of attribute information as part of their permitting processes. Additionally, there can be important differences in the way that these attributes have been assembled into published data products as well as in the ways in which these data products can be selected/filtered in data download web-portals between municicpalities. In order to find building permits that were related to electric panel upgrades, we used a combination of thematical filtering and keyword searches, where approrpriate, depending upon the combination of these factors.

For permit record type keyword searches, the following terms were used:

-	Electrical, Residential Electrical (Res elec), Commercial Electrical (Com elec), Residential Alteration (res alt), Commercial Alteration (com alt), OTC (over the counter), No plan permits (permits that do not require detailed plans), Simple permits, Express permits, PV permit, EV permit, Panel upgrade, MPU (main panel upgrade), Service upgrade, Utility permit, Residential, Building, Commercial.

-	If the building permit portal did not provide a query to specify permit type, we used the Record ID query and searched: B (for building permit- some Record ID’s start with B), R (for residential), C (for commercial)
-	Dates: Dates ranged from 1950 to present


### Access Patterns

There are three basic mechanisms by which we found permit data to be accessible: open data portals, building permit websites, and publicly accessible APIs.  Some municipalities have online permit tracking systems where you can search for all records that match a certain query. An in depth process and description of these portals is addressed in the following section. There are commercial software solution providers which specialize in building permit data tracking and management systems. The two biggest of which are Accela and eTRAKit. The standard products offerred by these companies provided a degree of consistency across municipalities which used them. For example, many permit data download sites provided a query section that allowed the user to search by 1. Record ID, 2. Start Date/End Date, 3. Parcel Number, 4. Street Number, 5. Street Name, 6. City. Differences most commonly ocurred with respect to the options for: 1. Permit Record Type, 2. Record Subtype, 3. Record Status, 4. Project Name, 6. License Type and State License Number, 7. The ability to download the datasets. This last point was very important because while many municipalities had the data we were looking for, they did not provide an option to download the data.

Below describes the general process for searching for and downloading building permit data from a building permit tracking system:

-	Accela
Starting at home page -> Advanced search -> Search records/applications-> Building-> Record type (if given option)-> From (date) -> Download results
-	eTRAKit
Starting at home page -> Search By -> Permit Type/Permit Subtype/Record ID -> “contains” -> *fill in* -> check for address, project description -> Download Results
-	Other
The first step is to look at the query options. Sometimes there was also a button that said “advanced search” and this would provide more specific queries. In other cases, the same steps as above were adapted on the basis of what functionality was available.

If no open data or online building permit tracking system existed, then a google search was conducted on "building permit data" or "building permit report" for the municipality in question. Some were found to have pdf's or csv's of the data, while others did not appear to make anything publicly available in any format. These municipalities have been highlighted in light yellow in the tracking spreadsheet.

### Summary Results

Our sample consists of the cities and counties in California whose building permit data met the following criteria:
1.	Was able to be downloaded as .csv, .json, or .geojson
2.	Permit data included a project description
3.	Permit data included an address, APN, or coordinates

Overall, 162 municipalities were checked for publicly available building permit data. Fifty-six municipalities met all of the aforementioned requirements (see table 1.). Nintey-four municipalities had building permit data but did not meet our requirements. Their data was either not possible to download (there was no “download” button), the query system required specific entries (only searchable by address, APN, complete permit number), the query system required an account, or there was an error downloading the records.  Lastly, twenty-five out of the nintey-four municipalities only had their building permit data available in PDF format. These municipalities are not included in our sample. Twelve municipalities did not have any type of permit data available on line.

There are multiple raw data files that were collected for some municipalities because there may have been different permit record types that had information on panel upgrades (ex. electrical permits and PV permits). Each raw CSV source file represents a permit record type for that municipality. Any given permit can only be one permit record type. This means that a Residential Solar permit cannot also be a Residential Electricity permit. It may happen that a particular project has multiple related permits, but the scope of work for each permit will be different. All of the raw datafiles have been named with either the “City_” or “County_” prefix following by the name of the municipality, and then a way to denote what type of permits are in that file. The following abbreviations were utilized to codify data files:

EV: Electric Vehicle
PV: Photovoltaic
ESU: Electrical Service Upgrade
MPU: Main Panel Upgrade
EPM: Electrical, Plumbing, Mechanical permit type
Finaled: The project has had all its inspections and is complete
Issued: Permit was issued but still needs inspections
Com: Commercial
Res: Residential

### Collation and Post-Processing

Individual raw data files were collated into a single combined csv table for each municipality using customized python scripts. During this process, field names were standardized and records with corrupted or missing attributes were dropped as necessary. The database import workflow documented in this portion of the repository operates over these post-processed CSV files to generate a single unified permit record table in the database. The structure of this table is documented in the data-dictionary below.

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
| solar_pv_system | Boolean field indicating solar PV system reference in work description |
| battery_storage_system | Boolean field indicating battery energy storage system reference in work description |
| ev_charger | Boolean field indicating EV charger reference in work description |
| heat_pump | Boolean field indicating heat pump system reference in work description |
| main_panel_upgrade | Boolean field indicating main electrical service panel upgrade reference in work description |
| sub_panel_upgrade | Boolean field indicating electrical sub-panel upgrade reference in work description |
| upgraded_panel_size | Size of destination main/sub panel following upgrade (where mentioned in work description) |



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
