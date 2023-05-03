# CARB Electrification Analysis Database

This repository contains workflows for injesting a collection of public and private data layers into a PostGres database for use in downstream analytics. Within this database various data layers are organized into schema on the basis of the source data provider. The following table of contents provides links to individual README documentation for each data source.

## Table of Contents

* Publicly Accessible Data Layers
    * [California Building Permit Sample](./data/building_permits/)
    * [California Air Resources Board (CARB) Air Basin and District Boundaries](./data/carb_boundaries/)
    * [California Air Resources Board (CARB) Priority Populations](./data/carb_priority_populations/)
    * [California Department of Public Heatlh (CDPH) Climate Hazard Vulnerability Index](./data/cdph_climate_hazard_vulnerability_index/)
    * [California Energy Commission (CEC) Building Energy Climate Zones](./data/cec_climate_zones/)
    * [US Census Bureau American Community Survey (ACS) Attributes](./data/census_american_community_survey/)
    * [Community Choice Aggregation (CCA) Boundaries](./data/community_choice_aggregations/)
    * [California Public Utility Commission (CPUC) Utility Affordability Ratios](./data/cpuc_utility_affordability_ratios/)
    * [California Office of Environmental Health Hazard Assessemnt (OEHHA) CalEnviroScreen 4.0](./data/oehha_cal_enviro_screen_4/)
    * [Pacific Gas and Electric (PGE) Grid Infrastructure Integrated Capacity Assessment (ICA) Results](./data/pge_grid/)
    * [Regional Energy Network (REN) Boundaries](./data/regional_energy_networks/)
    * [Southern California Edison (SCE) Grid Infrastructure Integrated Capacity Assessment (ICA) Results](./data/sce_grid/)
    * [San Diego Gas and Electric (SDGE) Grid Infrastructure Integrated Capacity Assessment (ICA) Results](./data/sdge_grid/)
    * [US Environmental Protection Agency (USEPA) eGRID Database](./data/usepa_egrid/)
* Privately Accessible Data Layers
    * TBA

## Important Notes

* Metadata files are automatically generated for each imported layer using the "ogrinfo" command line utility. These files are located within each data provider sub-directory and have the filename suffix "_ogrinfo.txt"
* All geospatial attributes have been projected into the same reference coordinate system: [EPSG:3310 - NAD83 / California Albers](https://epsg.io/3310). This coordinate system allows for accurate area and distance calculations for layers whose spatial boundaries are confied within the bounds of California, but not beyond.
* The raw data files that are used for the import workflows are not stored in the repository as this is not considered best practice. These files are available upon request - although, in most cases they should be unchanged from the resources that are directly available from the provided data source resource links, unless otherwise noted.
