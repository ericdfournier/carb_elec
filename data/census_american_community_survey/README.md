# README.md

# Data Source

American Community Survey (ACS) data are accessed programmatically via the Census Developer API using methods documented in the associated "download.py" script located within this same directory. ACS tables are constructed on the basis of keyword search matches. These data are provided for the 2019 census year to retain geographic consistency with the boundaries used for the CalEnviroScreen and CARB Priority Population designations.

# Data Dictionary

| Table | Data Field | Definition |
|-------|------------|------------|
| acs_ca_2019_county_geom | ALAND | Land Area |
| acs_ca_2019_county_geom | AWATER | Water Area |
| acs_ca_2019_county_geom | CBSAFP | Core Based Statistical Area |
| acs_ca_2019_county_geom | CLASSFP | Class FIPS Code |
| acs_ca_2019_county_geom | COUNTYFP | County FIPS Code |
| acs_ca_2019_county_geom | COUNTYNS | ANSI County Code |
| acs_ca_2019_county_geom | CSAFP | Geographic Entity Class Code |
| acs_ca_2019_county_geom | FUNCSTAT | Functional Status Code |
| acs_ca_2019_county_geom | GEOID | Geographic Identification Code |
| acs_ca_2019_county_geom | INTPTLAT | Latitude of the Internal Point |
| acs_ca_2019_county_geom | INTPTLON | Longitude of the Internal Point |
| acs_ca_2019_county_geom | LSAD | Legal/Statistical Area Description Code |
| acs_ca_2019_county_geom | METDIVFP | Metropolitan division code |
| acs_ca_2019_county_geom | MTFCC | MAF/Tiger Feature Class Code |
| acs_ca_2019_county_geom | NAME | County Name |
| acs_ca_2019_county_geom | NAMELSAD | County Name with translated Legal/Statistical Area Description |
| acs_ca_2019_county_geom | STATEFP | State FIPS Code |
| acs_ca_2019_county_geom | geometry | Geometry |
| acs_ca_2019_place_geom | ALAND | Land Area |
| acs_ca_2019_place_geom | AWATER | Water Area |
| acs_ca_2019_place_geom | CLASSFP | Class FIPS Code |
| acs_ca_2019_place_geom | FUNCSTAT | Functional Status Code |
| acs_ca_2019_place_geom | GEOID | Geographic Identification Code |
| acs_ca_2019_place_geom | INTPTLAT | Latitude of the Internal Point |
| acs_ca_2019_place_geom | INTPTLON | Longitude of the Internal Point |
| acs_ca_2019_place_geom | LSAD | Legal/Statistical Area Description Code |
| acs_ca_2019_place_geom | MTFCC | MAF/Tiger Feature Class Code |
| acs_ca_2019_place_geom | NAME | Place Name  |
| acs_ca_2019_place_geom | NAMELSAD | Place Name with translated Legal/Statistical Area Description |
| acs_ca_2019_place_geom | PCICBSA | Metropolitan or micropolitan statistical area principal city indicator |
| acs_ca_2019_place_geom | PCINECTA | City and town area principal city indicator |
| acs_ca_2019_place_geom | PLACEFP | Place FIPS Code |
| acs_ca_2019_place_geom | PLACENS | Place GNIS Code |
| acs_ca_2019_place_geom | STATEFP | State FIPS Code |
| acs_ca_2019_place_geom | geometry | Geometry |
| acs_ca_2019_puma_geom | ALAND10 | Land Area |
| acs_ca_2019_puma_geom | AWATER10 | Water Area |
| acs_ca_2019_puma_geom | FUNCSTAT10 | Functional Status Code |
| acs_ca_2019_puma_geom | GEOID10 | Geographic Identification Code |
| acs_ca_2019_puma_geom | INTPTLAT10 | Latitude of Internal Point |
| acs_ca_2019_puma_geom | INTPTLON10 | Longitude of Internal Point |
| acs_ca_2019_puma_geom | MTFCC10 | MAF/Tiger Feature Class Code |
| acs_ca_2019_puma_geom | NAMELSAD10 | Place Name with translated Legal/Statistical Area Description  |
| acs_ca_2019_puma_geom | PUMACE10 | Public Use Microdata Area Code |
| acs_ca_2019_puma_geom | STATEFP10 | State FIPS Code |
| acs_ca_2019_puma_geom | geometry | Geometry |
| acs_ca_2019_tr_fuel | DP04_0062E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_fuel | DP04_0062E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_fuel | DP04_0062PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_fuel | DP04_0062PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_fuel | DP04_0063E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_fuel | DP04_0063E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_fuel | DP04_0063PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_fuel | DP04_0063PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_fuel | DP04_0064E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_fuel | DP04_0064E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_fuel | DP04_0064PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_fuel | DP04_0064PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_fuel | DP04_0065E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_fuel | DP04_0065E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_fuel | DP04_0065PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_fuel | DP04_0065PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_fuel | DP04_0066E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_fuel | DP04_0066E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_fuel | DP04_0066PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_fuel | DP04_0066PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_fuel | DP04_0067E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_fuel | DP04_0067E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_fuel | DP04_0067PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_fuel | DP04_0067PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_fuel | DP04_0068E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_fuel | DP04_0068E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_fuel | DP04_0068PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_fuel | DP04_0068PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_fuel | DP04_0069E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_fuel | DP04_0069E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_fuel | DP04_0069PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_fuel | DP04_0069PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_fuel | DP04_0070E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_fuel | DP04_0070E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_fuel | DP04_0070PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_fuel | DP04_0070PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_fuel | DP04_0071E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_fuel | DP04_0071E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_fuel | DP04_0071PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_fuel | DP04_0071PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_fuel | GEOID | Geographic Identification Code |
| acs_ca_2019_tr_fuel | NAME | Tract Name |
| acs_ca_2019_tr_geom | ALAND | Land Area |
| acs_ca_2019_tr_geom | AWATER | Water Area |
| acs_ca_2019_tr_geom | COUNTYFP | County FIPS Code |
| acs_ca_2019_tr_geom | FUNCSTAT | Functional Status Code |
| acs_ca_2019_tr_geom | GEOID | Geographic Identification Code |
| acs_ca_2019_tr_geom | INTPTLAT | Latitude of Internal Point |
| acs_ca_2019_tr_geom | INTPTLON | Longitude of Internal Point |
| acs_ca_2019_tr_geom | MTFCC | MAF/Tiger Feature Class Code |
| acs_ca_2019_tr_geom | NAME | Tract Name |
| acs_ca_2019_tr_geom | NAMELSAD | Tract Name with translated Legal/Statistical Area Description |
| acs_ca_2019_tr_geom | STATEFP | State FIPS Code |
| acs_ca_2019_tr_geom | TRACTCE | Census Tract Code |
| acs_ca_2019_tr_geom | geometry | Geometry |
| acs_ca_2019_tr_housing | DP03_0038E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_housing | DP03_0038E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_housing | DP03_0038PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_housing | DP03_0038PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_housing | DP04_0001E | Estimate!!HOUSING OCCUPANCY!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0001PE | Percent!!HOUSING OCCUPANCY!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0002E | Estimate!!HOUSING OCCUPANCY!!Total housing units!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0002PE | Percent!!HOUSING OCCUPANCY!!Total housing units!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0003E | Estimate!!HOUSING OCCUPANCY!!Total housing units!!Vacant housing units |
| acs_ca_2019_tr_housing | DP04_0003PE | Percent!!HOUSING OCCUPANCY!!Total housing units!!Vacant housing units |
| acs_ca_2019_tr_housing | DP04_0004E | Estimate!!HOUSING OCCUPANCY!!Total housing units!!Homeowner vacancy rate |
| acs_ca_2019_tr_housing | DP04_0004PE | Percent!!HOUSING OCCUPANCY!!Total housing units!!Homeowner vacancy rate |
| acs_ca_2019_tr_housing | DP04_0005E | Estimate!!HOUSING OCCUPANCY!!Total housing units!!Rental vacancy rate |
| acs_ca_2019_tr_housing | DP04_0005PE | Percent!!HOUSING OCCUPANCY!!Total housing units!!Rental vacancy rate |
| acs_ca_2019_tr_housing | DP04_0006E | Estimate!!UNITS IN STRUCTURE!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0006PE | Percent!!UNITS IN STRUCTURE!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0007E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!1-unit, detached |
| acs_ca_2019_tr_housing | DP04_0007PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!1-unit, detached |
| acs_ca_2019_tr_housing | DP04_0008E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!1-unit, attached |
| acs_ca_2019_tr_housing | DP04_0008PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!1-unit, attached |
| acs_ca_2019_tr_housing | DP04_0009E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!2 units |
| acs_ca_2019_tr_housing | DP04_0009PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!2 units |
| acs_ca_2019_tr_housing | DP04_0010E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!3 or 4 units |
| acs_ca_2019_tr_housing | DP04_0010PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!3 or 4 units |
| acs_ca_2019_tr_housing | DP04_0011E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!5 to 9 units |
| acs_ca_2019_tr_housing | DP04_0011PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!5 to 9 units |
| acs_ca_2019_tr_housing | DP04_0012E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!10 to 19 units |
| acs_ca_2019_tr_housing | DP04_0012PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!10 to 19 units |
| acs_ca_2019_tr_housing | DP04_0013E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!20 or more units |
| acs_ca_2019_tr_housing | DP04_0013PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!20 or more units |
| acs_ca_2019_tr_housing | DP04_0014E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!Mobile home |
| acs_ca_2019_tr_housing | DP04_0014PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!Mobile home |
| acs_ca_2019_tr_housing | DP04_0015E | Estimate!!UNITS IN STRUCTURE!!Total housing units!!Boat, RV, van, etc. |
| acs_ca_2019_tr_housing | DP04_0015PE | Percent!!UNITS IN STRUCTURE!!Total housing units!!Boat, RV, van, etc. |
| acs_ca_2019_tr_housing | DP04_0016E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0016PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0017E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2014 or later |
| acs_ca_2019_tr_housing | DP04_0017PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2014 or later |
| acs_ca_2019_tr_housing | DP04_0018E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2010 to 2013 |
| acs_ca_2019_tr_housing | DP04_0018PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2010 to 2013 |
| acs_ca_2019_tr_housing | DP04_0019E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2000 to 2009 |
| acs_ca_2019_tr_housing | DP04_0019PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 2000 to 2009 |
| acs_ca_2019_tr_housing | DP04_0020E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1990 to 1999 |
| acs_ca_2019_tr_housing | DP04_0020PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1990 to 1999 |
| acs_ca_2019_tr_housing | DP04_0021E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1980 to 1989 |
| acs_ca_2019_tr_housing | DP04_0021PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1980 to 1989 |
| acs_ca_2019_tr_housing | DP04_0022E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1970 to 1979 |
| acs_ca_2019_tr_housing | DP04_0022PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1970 to 1979 |
| acs_ca_2019_tr_housing | DP04_0023E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1960 to 1969 |
| acs_ca_2019_tr_housing | DP04_0023PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1960 to 1969 |
| acs_ca_2019_tr_housing | DP04_0024E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1950 to 1959 |
| acs_ca_2019_tr_housing | DP04_0024PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1950 to 1959 |
| acs_ca_2019_tr_housing | DP04_0025E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1940 to 1949 |
| acs_ca_2019_tr_housing | DP04_0025PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1940 to 1949 |
| acs_ca_2019_tr_housing | DP04_0026E | Estimate!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1939 or earlier |
| acs_ca_2019_tr_housing | DP04_0026PE | Percent!!YEAR STRUCTURE BUILT!!Total housing units!!Built 1939 or earlier |
| acs_ca_2019_tr_housing | DP04_0027E | Estimate!!ROOMS!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0027PE | Percent!!ROOMS!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0028E | Estimate!!ROOMS!!Total housing units!!1 room |
| acs_ca_2019_tr_housing | DP04_0028PE | Percent!!ROOMS!!Total housing units!!1 room |
| acs_ca_2019_tr_housing | DP04_0029E | Estimate!!ROOMS!!Total housing units!!2 rooms |
| acs_ca_2019_tr_housing | DP04_0029PE | Percent!!ROOMS!!Total housing units!!2 rooms |
| acs_ca_2019_tr_housing | DP04_0030E | Estimate!!ROOMS!!Total housing units!!3 rooms |
| acs_ca_2019_tr_housing | DP04_0030PE | Percent!!ROOMS!!Total housing units!!3 rooms |
| acs_ca_2019_tr_housing | DP04_0031E | Estimate!!ROOMS!!Total housing units!!4 rooms |
| acs_ca_2019_tr_housing | DP04_0031PE | Percent!!ROOMS!!Total housing units!!4 rooms |
| acs_ca_2019_tr_housing | DP04_0032E | Estimate!!ROOMS!!Total housing units!!5 rooms |
| acs_ca_2019_tr_housing | DP04_0032PE | Percent!!ROOMS!!Total housing units!!5 rooms |
| acs_ca_2019_tr_housing | DP04_0033E | Estimate!!ROOMS!!Total housing units!!6 rooms |
| acs_ca_2019_tr_housing | DP04_0033PE | Percent!!ROOMS!!Total housing units!!6 rooms |
| acs_ca_2019_tr_housing | DP04_0034E | Estimate!!ROOMS!!Total housing units!!7 rooms |
| acs_ca_2019_tr_housing | DP04_0034PE | Percent!!ROOMS!!Total housing units!!7 rooms |
| acs_ca_2019_tr_housing | DP04_0035E | Estimate!!ROOMS!!Total housing units!!8 rooms |
| acs_ca_2019_tr_housing | DP04_0035PE | Percent!!ROOMS!!Total housing units!!8 rooms |
| acs_ca_2019_tr_housing | DP04_0036E | Estimate!!ROOMS!!Total housing units!!9 rooms or more |
| acs_ca_2019_tr_housing | DP04_0036PE | Percent!!ROOMS!!Total housing units!!9 rooms or more |
| acs_ca_2019_tr_housing | DP04_0037E | Estimate!!ROOMS!!Total housing units!!Median rooms |
| acs_ca_2019_tr_housing | DP04_0037PE | Percent!!ROOMS!!Total housing units!!Median rooms |
| acs_ca_2019_tr_housing | DP04_0038E | Estimate!!BEDROOMS!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0038PE | Percent!!BEDROOMS!!Total housing units |
| acs_ca_2019_tr_housing | DP04_0039E | Estimate!!BEDROOMS!!Total housing units!!No bedroom |
| acs_ca_2019_tr_housing | DP04_0039PE | Percent!!BEDROOMS!!Total housing units!!No bedroom |
| acs_ca_2019_tr_housing | DP04_0040E | Estimate!!BEDROOMS!!Total housing units!!1 bedroom |
| acs_ca_2019_tr_housing | DP04_0040PE | Percent!!BEDROOMS!!Total housing units!!1 bedroom |
| acs_ca_2019_tr_housing | DP04_0041E | Estimate!!BEDROOMS!!Total housing units!!2 bedrooms |
| acs_ca_2019_tr_housing | DP04_0041PE | Percent!!BEDROOMS!!Total housing units!!2 bedrooms |
| acs_ca_2019_tr_housing | DP04_0042E | Estimate!!BEDROOMS!!Total housing units!!3 bedrooms |
| acs_ca_2019_tr_housing | DP04_0042PE | Percent!!BEDROOMS!!Total housing units!!3 bedrooms |
| acs_ca_2019_tr_housing | DP04_0043E | Estimate!!BEDROOMS!!Total housing units!!4 bedrooms |
| acs_ca_2019_tr_housing | DP04_0043PE | Percent!!BEDROOMS!!Total housing units!!4 bedrooms |
| acs_ca_2019_tr_housing | DP04_0044E | Estimate!!BEDROOMS!!Total housing units!!5 or more bedrooms |
| acs_ca_2019_tr_housing | DP04_0044PE | Percent!!BEDROOMS!!Total housing units!!5 or more bedrooms |
| acs_ca_2019_tr_housing | DP04_0045E | Estimate!!HOUSING TENURE!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0045PE | Percent!!HOUSING TENURE!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0046E | Estimate!!HOUSING TENURE!!Occupied housing units!!Owner-occupied |
| acs_ca_2019_tr_housing | DP04_0046PE | Percent!!HOUSING TENURE!!Occupied housing units!!Owner-occupied |
| acs_ca_2019_tr_housing | DP04_0047E | Estimate!!HOUSING TENURE!!Occupied housing units!!Renter-occupied |
| acs_ca_2019_tr_housing | DP04_0047PE | Percent!!HOUSING TENURE!!Occupied housing units!!Renter-occupied |
| acs_ca_2019_tr_housing | DP04_0048E | Estimate!!HOUSING TENURE!!Occupied housing units!!Average household size of owner-occupied unit |
| acs_ca_2019_tr_housing | DP04_0048PE | Percent!!HOUSING TENURE!!Occupied housing units!!Average household size of owner-occupied unit |
| acs_ca_2019_tr_housing | DP04_0049E | Estimate!!HOUSING TENURE!!Occupied housing units!!Average household size of renter-occupied unit |
| acs_ca_2019_tr_housing | DP04_0049PE | Percent!!HOUSING TENURE!!Occupied housing units!!Average household size of renter-occupied unit |
| acs_ca_2019_tr_housing | DP04_0050E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0050PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0051E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2017 or later |
| acs_ca_2019_tr_housing | DP04_0051PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2017 or later |
| acs_ca_2019_tr_housing | DP04_0052E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2015 to 2016 |
| acs_ca_2019_tr_housing | DP04_0052PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2015 to 2016 |
| acs_ca_2019_tr_housing | DP04_0053E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2010 to 2014 |
| acs_ca_2019_tr_housing | DP04_0053PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2010 to 2014 |
| acs_ca_2019_tr_housing | DP04_0054E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2000 to 2009 |
| acs_ca_2019_tr_housing | DP04_0054PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 2000 to 2009 |
| acs_ca_2019_tr_housing | DP04_0055E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 1990 to 1999 |
| acs_ca_2019_tr_housing | DP04_0055PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 1990 to 1999 |
| acs_ca_2019_tr_housing | DP04_0056E | Estimate!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 1989 and earlier |
| acs_ca_2019_tr_housing | DP04_0056PE | Percent!!YEAR HOUSEHOLDER MOVED INTO UNIT!!Occupied housing units!!Moved in 1989 and earlier |
| acs_ca_2019_tr_housing | DP04_0057E | Estimate!!VEHICLES AVAILABLE!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0057PE | Percent!!VEHICLES AVAILABLE!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0058E | Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!No vehicles available |
| acs_ca_2019_tr_housing | DP04_0058PE | Percent!!VEHICLES AVAILABLE!!Occupied housing units!!No vehicles available |
| acs_ca_2019_tr_housing | DP04_0059E | Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!1 vehicle available |
| acs_ca_2019_tr_housing | DP04_0059PE | Percent!!VEHICLES AVAILABLE!!Occupied housing units!!1 vehicle available |
| acs_ca_2019_tr_housing | DP04_0060E | Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!2 vehicles available |
| acs_ca_2019_tr_housing | DP04_0060PE | Percent!!VEHICLES AVAILABLE!!Occupied housing units!!2 vehicles available |
| acs_ca_2019_tr_housing | DP04_0061E | Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!3 or more vehicles available |
| acs_ca_2019_tr_housing | DP04_0061PE | Percent!!VEHICLES AVAILABLE!!Occupied housing units!!3 or more vehicles available |
| acs_ca_2019_tr_housing | DP04_0062E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0062E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0062PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0062PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0063E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_housing | DP04_0063E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_housing | DP04_0063PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_housing | DP04_0063PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Utility gas |
| acs_ca_2019_tr_housing | DP04_0064E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_housing | DP04_0064E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_housing | DP04_0064PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_housing | DP04_0064PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Bottled, tank, or LP gas |
| acs_ca_2019_tr_housing | DP04_0065E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_housing | DP04_0065E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_housing | DP04_0065PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_housing | DP04_0065PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Electricity |
| acs_ca_2019_tr_housing | DP04_0066E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_housing | DP04_0066E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_housing | DP04_0066PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_housing | DP04_0066PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc. |
| acs_ca_2019_tr_housing | DP04_0067E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_housing | DP04_0067E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_housing | DP04_0067PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_housing | DP04_0067PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Coal or coke |
| acs_ca_2019_tr_housing | DP04_0068E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_housing | DP04_0068E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_housing | DP04_0068PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_housing | DP04_0068PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Wood |
| acs_ca_2019_tr_housing | DP04_0069E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_housing | DP04_0069E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_housing | DP04_0069PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_housing | DP04_0069PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Solar energy |
| acs_ca_2019_tr_housing | DP04_0070E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_housing | DP04_0070E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_housing | DP04_0070PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_housing | DP04_0070PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!Other fuel |
| acs_ca_2019_tr_housing | DP04_0071E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_housing | DP04_0071E | Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_housing | DP04_0071PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_housing | DP04_0071PE | Percent!!HOUSE HEATING FUEL!!Occupied housing units!!No fuel used |
| acs_ca_2019_tr_housing | DP04_0072E | Estimate!!SELECTED CHARACTERISTICS!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0072PE | Percent!!SELECTED CHARACTERISTICS!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0073E | Estimate!!SELECTED CHARACTERISTICS!!Occupied housing units!!Lacking complete plumbing facilities |
| acs_ca_2019_tr_housing | DP04_0073PE | Percent!!SELECTED CHARACTERISTICS!!Occupied housing units!!Lacking complete plumbing facilities |
| acs_ca_2019_tr_housing | DP04_0074E | Estimate!!SELECTED CHARACTERISTICS!!Occupied housing units!!Lacking complete kitchen facilities |
| acs_ca_2019_tr_housing | DP04_0074PE | Percent!!SELECTED CHARACTERISTICS!!Occupied housing units!!Lacking complete kitchen facilities |
| acs_ca_2019_tr_housing | DP04_0075E | Estimate!!SELECTED CHARACTERISTICS!!Occupied housing units!!No telephone service available |
| acs_ca_2019_tr_housing | DP04_0075PE | Percent!!SELECTED CHARACTERISTICS!!Occupied housing units!!No telephone service available |
| acs_ca_2019_tr_housing | DP04_0076E | Estimate!!OCCUPANTS PER ROOM!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0076PE | Percent!!OCCUPANTS PER ROOM!!Occupied housing units |
| acs_ca_2019_tr_housing | DP04_0077E | Estimate!!OCCUPANTS PER ROOM!!Occupied housing units!!1.00 or less |
| acs_ca_2019_tr_housing | DP04_0077PE | Percent!!OCCUPANTS PER ROOM!!Occupied housing units!!1.00 or less |
| acs_ca_2019_tr_housing | DP04_0078E | Estimate!!OCCUPANTS PER ROOM!!Occupied housing units!!1.01 to 1.50 |
| acs_ca_2019_tr_housing | DP04_0078PE | Percent!!OCCUPANTS PER ROOM!!Occupied housing units!!1.01 to 1.50 |
| acs_ca_2019_tr_housing | DP04_0079E | Estimate!!OCCUPANTS PER ROOM!!Occupied housing units!!1.51 or more |
| acs_ca_2019_tr_housing | DP04_0079PE | Percent!!OCCUPANTS PER ROOM!!Occupied housing units!!1.51 or more |
| acs_ca_2019_tr_housing | DP04_0091E | Estimate!!MORTGAGE STATUS!!Owner-occupied units!!Housing units with a mortgage |
| acs_ca_2019_tr_housing | DP04_0091PE | Percent!!MORTGAGE STATUS!!Owner-occupied units!!Housing units with a mortgage |
| acs_ca_2019_tr_housing | DP04_0092E | Estimate!!MORTGAGE STATUS!!Owner-occupied units!!Housing units without a mortgage |
| acs_ca_2019_tr_housing | DP04_0092PE | Percent!!MORTGAGE STATUS!!Owner-occupied units!!Housing units without a mortgage |
| acs_ca_2019_tr_housing | DP04_0093E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage |
| acs_ca_2019_tr_housing | DP04_0093PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage |
| acs_ca_2019_tr_housing | DP04_0094E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!Less than $500 |
| acs_ca_2019_tr_housing | DP04_0094PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!Less than $500 |
| acs_ca_2019_tr_housing | DP04_0095E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$500 to $999 |
| acs_ca_2019_tr_housing | DP04_0095PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$500 to $999 |
| acs_ca_2019_tr_housing | DP04_0096E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$1,000 to $1,499 |
| acs_ca_2019_tr_housing | DP04_0096PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$1,000 to $1,499 |
| acs_ca_2019_tr_housing | DP04_0097E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$1,500 to $1,999 |
| acs_ca_2019_tr_housing | DP04_0097PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$1,500 to $1,999 |
| acs_ca_2019_tr_housing | DP04_0098E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$2,000 to $2,499 |
| acs_ca_2019_tr_housing | DP04_0098PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$2,000 to $2,499 |
| acs_ca_2019_tr_housing | DP04_0099E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$2,500 to $2,999 |
| acs_ca_2019_tr_housing | DP04_0099PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$2,500 to $2,999 |
| acs_ca_2019_tr_housing | DP04_0100E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$3,000 or more |
| acs_ca_2019_tr_housing | DP04_0100PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!$3,000 or more |
| acs_ca_2019_tr_housing | DP04_0101E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!Median (dollars) |
| acs_ca_2019_tr_housing | DP04_0101PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!Median (dollars) |
| acs_ca_2019_tr_housing | DP04_0102E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage |
| acs_ca_2019_tr_housing | DP04_0102PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage |
| acs_ca_2019_tr_housing | DP04_0103E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!Less than $250 |
| acs_ca_2019_tr_housing | DP04_0103PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!Less than $250 |
| acs_ca_2019_tr_housing | DP04_0104E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$250 to $399 |
| acs_ca_2019_tr_housing | DP04_0104PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$250 to $399 |
| acs_ca_2019_tr_housing | DP04_0105E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$400 to $599 |
| acs_ca_2019_tr_housing | DP04_0105PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$400 to $599 |
| acs_ca_2019_tr_housing | DP04_0106E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$600 to $799 |
| acs_ca_2019_tr_housing | DP04_0106PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$600 to $799 |
| acs_ca_2019_tr_housing | DP04_0107E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$800 to $999 |
| acs_ca_2019_tr_housing | DP04_0107PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$800 to $999 |
| acs_ca_2019_tr_housing | DP04_0108E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$1,000 or more |
| acs_ca_2019_tr_housing | DP04_0108PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!$1,000 or more |
| acs_ca_2019_tr_housing | DP04_0109E | Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!Median (dollars) |
| acs_ca_2019_tr_housing | DP04_0109PE | Percent!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units without a mortgage!!Median (dollars) |
| acs_ca_2019_tr_housing | DP04_0110E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0110E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0110PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0110PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0111E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_housing | DP04_0111E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_housing | DP04_0111PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_housing | DP04_0111PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_housing | DP04_0112E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0112E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0112PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0112PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0113E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0113E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0113PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0113PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0114E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0114E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0114PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0114PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0115E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0115E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0115PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0115PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0116E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0116E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0116PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0116PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0117E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0117E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0117PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0117PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_housing | DP04_0118E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_housing | DP04_0118E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_housing | DP04_0118PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_housing | DP04_0118PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_housing | DP04_0119E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_housing | DP04_0119E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_housing | DP04_0119PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_housing | DP04_0119PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_housing | DP04_0120E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_housing | DP04_0120E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_housing | DP04_0120PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_housing | DP04_0120PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_housing | DP04_0121E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0121E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0121PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0121PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_housing | DP04_0122E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0122E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0122PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0122PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_housing | DP04_0123E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0123E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0123PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0123PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_housing | DP04_0124E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0124E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0124PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0124PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_housing | DP04_0125E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0125E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0125PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP04_0125PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_housing | DP05_0086E | Estimate!!Total housing units |
| acs_ca_2019_tr_housing | DP05_0086PE | Percent!!Total housing units |
| acs_ca_2019_tr_housing | GEOID | Geographic Identification Code |
| acs_ca_2019_tr_housing | NAME | Tract Name |
| acs_ca_2019_tr_income | DP03_0051E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households |
| acs_ca_2019_tr_income | DP03_0051PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households |
| acs_ca_2019_tr_income | DP03_0052E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Less than $10,000 |
| acs_ca_2019_tr_income | DP03_0052PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Less than $10,000 |
| acs_ca_2019_tr_income | DP03_0053E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$10,000 to $14,999 |
| acs_ca_2019_tr_income | DP03_0053PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$10,000 to $14,999 |
| acs_ca_2019_tr_income | DP03_0054E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$15,000 to $24,999 |
| acs_ca_2019_tr_income | DP03_0054PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$15,000 to $24,999 |
| acs_ca_2019_tr_income | DP03_0055E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$25,000 to $34,999 |
| acs_ca_2019_tr_income | DP03_0055PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$25,000 to $34,999 |
| acs_ca_2019_tr_income | DP03_0056E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$35,000 to $49,999 |
| acs_ca_2019_tr_income | DP03_0056PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$35,000 to $49,999 |
| acs_ca_2019_tr_income | DP03_0057E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$50,000 to $74,999 |
| acs_ca_2019_tr_income | DP03_0057PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$50,000 to $74,999 |
| acs_ca_2019_tr_income | DP03_0058E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$75,000 to $99,999 |
| acs_ca_2019_tr_income | DP03_0058PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$75,000 to $99,999 |
| acs_ca_2019_tr_income | DP03_0059E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$100,000 to $149,999 |
| acs_ca_2019_tr_income | DP03_0059PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$100,000 to $149,999 |
| acs_ca_2019_tr_income | DP03_0060E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$150,000 to $199,999 |
| acs_ca_2019_tr_income | DP03_0060PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$150,000 to $199,999 |
| acs_ca_2019_tr_income | DP03_0061E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$200,000 or more |
| acs_ca_2019_tr_income | DP03_0061PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!$200,000 or more |
| acs_ca_2019_tr_income | DP03_0062E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars) |
| acs_ca_2019_tr_income | DP03_0062PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars) |
| acs_ca_2019_tr_income | DP03_0063E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Mean household income (dollars) |
| acs_ca_2019_tr_income | DP03_0063PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Mean household income (dollars) |
| acs_ca_2019_tr_income | DP03_0064E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With earnings |
| acs_ca_2019_tr_income | DP03_0064PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With earnings |
| acs_ca_2019_tr_income | DP03_0065E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With earnings!!Mean earnings (dollars) |
| acs_ca_2019_tr_income | DP03_0065PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With earnings!!Mean earnings (dollars) |
| acs_ca_2019_tr_income | DP03_0066E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Social Security |
| acs_ca_2019_tr_income | DP03_0066PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Social Security |
| acs_ca_2019_tr_income | DP03_0067E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Social Security!!Mean Social Security income (dollars) |
| acs_ca_2019_tr_income | DP03_0067PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Social Security!!Mean Social Security income (dollars) |
| acs_ca_2019_tr_income | DP03_0068E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With retirement income |
| acs_ca_2019_tr_income | DP03_0068PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With retirement income |
| acs_ca_2019_tr_income | DP03_0069E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With retirement income!!Mean retirement income (dollars) |
| acs_ca_2019_tr_income | DP03_0069PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With retirement income!!Mean retirement income (dollars) |
| acs_ca_2019_tr_income | DP03_0070E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Supplemental Security Income |
| acs_ca_2019_tr_income | DP03_0070PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Supplemental Security Income |
| acs_ca_2019_tr_income | DP03_0071E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Supplemental Security Income!!Mean Supplemental Security Income (dollars) |
| acs_ca_2019_tr_income | DP03_0071PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Supplemental Security Income!!Mean Supplemental Security Income (dollars) |
| acs_ca_2019_tr_income | DP03_0072E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With cash public assistance income |
| acs_ca_2019_tr_income | DP03_0072PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With cash public assistance income |
| acs_ca_2019_tr_income | DP03_0073E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With cash public assistance income!!Mean cash public assistance income (dollars) |
| acs_ca_2019_tr_income | DP03_0073PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With cash public assistance income!!Mean cash public assistance income (dollars) |
| acs_ca_2019_tr_income | DP03_0074E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Food Stamp/SNAP benefits in the past 12 months |
| acs_ca_2019_tr_income | DP03_0074PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!With Food Stamp/SNAP benefits in the past 12 months |
| acs_ca_2019_tr_income | DP03_0075E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families |
| acs_ca_2019_tr_income | DP03_0075PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families |
| acs_ca_2019_tr_income | DP03_0076E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Less than $10,000 |
| acs_ca_2019_tr_income | DP03_0076PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Less than $10,000 |
| acs_ca_2019_tr_income | DP03_0077E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$10,000 to $14,999 |
| acs_ca_2019_tr_income | DP03_0077PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$10,000 to $14,999 |
| acs_ca_2019_tr_income | DP03_0078E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$15,000 to $24,999 |
| acs_ca_2019_tr_income | DP03_0078PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$15,000 to $24,999 |
| acs_ca_2019_tr_income | DP03_0079E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$25,000 to $34,999 |
| acs_ca_2019_tr_income | DP03_0079PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$25,000 to $34,999 |
| acs_ca_2019_tr_income | DP03_0080E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$35,000 to $49,999 |
| acs_ca_2019_tr_income | DP03_0080PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$35,000 to $49,999 |
| acs_ca_2019_tr_income | DP03_0081E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$50,000 to $74,999 |
| acs_ca_2019_tr_income | DP03_0081PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$50,000 to $74,999 |
| acs_ca_2019_tr_income | DP03_0082E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$75,000 to $99,999 |
| acs_ca_2019_tr_income | DP03_0082PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$75,000 to $99,999 |
| acs_ca_2019_tr_income | DP03_0083E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$100,000 to $149,999 |
| acs_ca_2019_tr_income | DP03_0083PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$100,000 to $149,999 |
| acs_ca_2019_tr_income | DP03_0084E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$150,000 to $199,999 |
| acs_ca_2019_tr_income | DP03_0084PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$150,000 to $199,999 |
| acs_ca_2019_tr_income | DP03_0085E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$200,000 or more |
| acs_ca_2019_tr_income | DP03_0085PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!$200,000 or more |
| acs_ca_2019_tr_income | DP03_0086E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Median family income (dollars) |
| acs_ca_2019_tr_income | DP03_0086PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Median family income (dollars) |
| acs_ca_2019_tr_income | DP03_0087E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Mean family income (dollars) |
| acs_ca_2019_tr_income | DP03_0087PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Families!!Mean family income (dollars) |
| acs_ca_2019_tr_income | DP03_0088E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Per capita income (dollars) |
| acs_ca_2019_tr_income | DP03_0088PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Per capita income (dollars) |
| acs_ca_2019_tr_income | DP03_0089E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households |
| acs_ca_2019_tr_income | DP03_0089PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households |
| acs_ca_2019_tr_income | DP03_0090E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households!!Median nonfamily income (dollars) |
| acs_ca_2019_tr_income | DP03_0090PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households!!Median nonfamily income (dollars) |
| acs_ca_2019_tr_income | DP03_0091E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households!!Mean nonfamily income (dollars) |
| acs_ca_2019_tr_income | DP03_0091PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Nonfamily households!!Mean nonfamily income (dollars) |
| acs_ca_2019_tr_income | DP03_0092E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for workers (dollars) |
| acs_ca_2019_tr_income | DP03_0092PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for workers (dollars) |
| acs_ca_2019_tr_income | DP03_0093E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for male full-time, year-round workers (dollars) |
| acs_ca_2019_tr_income | DP03_0093PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for male full-time, year-round workers (dollars) |
| acs_ca_2019_tr_income | DP03_0094E | Estimate!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for female full-time, year-round workers (dollars) |
| acs_ca_2019_tr_income | DP03_0094PE | Percent!!INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Median earnings for female full-time, year-round workers (dollars) |
| acs_ca_2019_tr_income | DP03_0119E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families |
| acs_ca_2019_tr_income | DP03_0119PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families |
| acs_ca_2019_tr_income | DP03_0120E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0120PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0121E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0121PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0122E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families |
| acs_ca_2019_tr_income | DP03_0122PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families |
| acs_ca_2019_tr_income | DP03_0123E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0123PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0124E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0124PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Married couple families!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0125E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present |
| acs_ca_2019_tr_income | DP03_0125PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present |
| acs_ca_2019_tr_income | DP03_0126E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0126PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present!!With related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0127E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0127PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families!!Families with female householder, no spouse present!!With related children of the householder under 18 years!!With related children of the householder under 5 years only |
| acs_ca_2019_tr_income | DP03_0128E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people |
| acs_ca_2019_tr_income | DP03_0128PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people |
| acs_ca_2019_tr_income | DP03_0129E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years |
| acs_ca_2019_tr_income | DP03_0129PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years |
| acs_ca_2019_tr_income | DP03_0130E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0130PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years |
| acs_ca_2019_tr_income | DP03_0131E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years!!Related children of the householder under 5 years |
| acs_ca_2019_tr_income | DP03_0131PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years!!Related children of the householder under 5 years |
| acs_ca_2019_tr_income | DP03_0132E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years!!Related children of the householder 5 to 17 years |
| acs_ca_2019_tr_income | DP03_0132PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Under 18 years!!Related children of the householder under 18 years!!Related children of the householder 5 to 17 years |
| acs_ca_2019_tr_income | DP03_0133E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over |
| acs_ca_2019_tr_income | DP03_0133PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over |
| acs_ca_2019_tr_income | DP03_0134E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over!!18 to 64 years |
| acs_ca_2019_tr_income | DP03_0134PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over!!18 to 64 years |
| acs_ca_2019_tr_income | DP03_0135E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over!!65 years and over |
| acs_ca_2019_tr_income | DP03_0135PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!18 years and over!!65 years and over |
| acs_ca_2019_tr_income | DP03_0136E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!People in families |
| acs_ca_2019_tr_income | DP03_0136PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!People in families |
| acs_ca_2019_tr_income | DP03_0137E | Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Unrelated individuals 15 years and over |
| acs_ca_2019_tr_income | DP03_0137PE | Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people!!Unrelated individuals 15 years and over |
| acs_ca_2019_tr_income | DP04_0110E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0110E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0110PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0110PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0111E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_income | DP04_0111E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_income | DP04_0111PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_income | DP04_0111PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 20.0 percent |
| acs_ca_2019_tr_income | DP04_0112E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0112E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0112PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0112PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0113E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0113E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0113PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0113PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0114E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0114E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0114PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0114PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0115E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0115E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0115PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0115PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0116E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0116E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0116PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0116PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0117E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0117E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0117PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0117PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0118E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_income | DP04_0118E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_income | DP04_0118PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_income | DP04_0118PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Less than 10.0 percent |
| acs_ca_2019_tr_income | DP04_0119E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_income | DP04_0119E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_income | DP04_0119PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_income | DP04_0119PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!10.0 to 14.9 percent |
| acs_ca_2019_tr_income | DP04_0120E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0120E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0120PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0120PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0121E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0121E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0121PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0121PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0122E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0122E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0122PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0122PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0123E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0123E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0123PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0123PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0124E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0124E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0124PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0124PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0125E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0125E | Estimate!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0125PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0125PE | Percent!!SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)!!Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0136E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0136PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed) |
| acs_ca_2019_tr_income | DP04_0137E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!Less than 15.0 percent |
| acs_ca_2019_tr_income | DP04_0137PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!Less than 15.0 percent |
| acs_ca_2019_tr_income | DP04_0138E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0138PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!15.0 to 19.9 percent |
| acs_ca_2019_tr_income | DP04_0139E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0139PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!20.0 to 24.9 percent |
| acs_ca_2019_tr_income | DP04_0140E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0140PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!25.0 to 29.9 percent |
| acs_ca_2019_tr_income | DP04_0141E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0141PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!30.0 to 34.9 percent |
| acs_ca_2019_tr_income | DP04_0142E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0142PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!35.0 percent or more |
| acs_ca_2019_tr_income | DP04_0143E | Estimate!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | DP04_0143PE | Percent!!GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)!!Occupied units paying rent (excluding units where GRAPI cannot be computed)!!Not computed |
| acs_ca_2019_tr_income | GEOID |  |
| acs_ca_2019_tr_income | Variable Code |  |
| acs_ca_2019_tr_metadata | label |  |
| acs_ca_2019_tr_metadata | table |  |
| acs_ca_2019_tr_metadata | variable |  |
| acs_ca_2019_tr_population | DP02_0018E | Estimate!!RELATIONSHIP!!Population in households |
| acs_ca_2019_tr_population | DP02_0018PE | Percent!!RELATIONSHIP!!Population in households |
| acs_ca_2019_tr_population | DP02_0019E | Estimate!!RELATIONSHIP!!Population in households!!Householder |
| acs_ca_2019_tr_population | DP02_0019PE | Percent!!RELATIONSHIP!!Population in households!!Householder |
| acs_ca_2019_tr_population | DP02_0020E | Estimate!!RELATIONSHIP!!Population in households!!Spouse |
| acs_ca_2019_tr_population | DP02_0020PE | Percent!!RELATIONSHIP!!Population in households!!Spouse |
| acs_ca_2019_tr_population | DP02_0021E | Estimate!!RELATIONSHIP!!Population in households!!Unmarried partner |
| acs_ca_2019_tr_population | DP02_0021PE | Percent!!RELATIONSHIP!!Population in households!!Unmarried partner |
| acs_ca_2019_tr_population | DP02_0022E | Estimate!!RELATIONSHIP!!Population in households!!Child |
| acs_ca_2019_tr_population | DP02_0022PE | Percent!!RELATIONSHIP!!Population in households!!Child |
| acs_ca_2019_tr_population | DP02_0023E | Estimate!!RELATIONSHIP!!Population in households!!Other relatives |
| acs_ca_2019_tr_population | DP02_0023PE | Percent!!RELATIONSHIP!!Population in households!!Other relatives |
| acs_ca_2019_tr_population | DP02_0024E | Estimate!!RELATIONSHIP!!Population in households!!Other nonrelatives |
| acs_ca_2019_tr_population | DP02_0024PE | Percent!!RELATIONSHIP!!Population in households!!Other nonrelatives |
| acs_ca_2019_tr_population | DP02_0053E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school |
| acs_ca_2019_tr_population | DP02_0053PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school |
| acs_ca_2019_tr_population | DP02_0054E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Nursery school, preschool |
| acs_ca_2019_tr_population | DP02_0054PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Nursery school, preschool |
| acs_ca_2019_tr_population | DP02_0055E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Kindergarten |
| acs_ca_2019_tr_population | DP02_0055PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Kindergarten |
| acs_ca_2019_tr_population | DP02_0056E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Elementary school (grades 1-8) |
| acs_ca_2019_tr_population | DP02_0056PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Elementary school (grades 1-8) |
| acs_ca_2019_tr_population | DP02_0057E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!High school (grades 9-12) |
| acs_ca_2019_tr_population | DP02_0057PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!High school (grades 9-12) |
| acs_ca_2019_tr_population | DP02_0058E | Estimate!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!College or graduate school |
| acs_ca_2019_tr_population | DP02_0058PE | Percent!!SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!College or graduate school |
| acs_ca_2019_tr_population | DP02_0059E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over |
| acs_ca_2019_tr_population | DP02_0059PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over |
| acs_ca_2019_tr_population | DP02_0060E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Less than 9th grade |
| acs_ca_2019_tr_population | DP02_0060PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Less than 9th grade |
| acs_ca_2019_tr_population | DP02_0061E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!9th to 12th grade, no diploma |
| acs_ca_2019_tr_population | DP02_0061PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!9th to 12th grade, no diploma |
| acs_ca_2019_tr_population | DP02_0062E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency) |
| acs_ca_2019_tr_population | DP02_0062PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency) |
| acs_ca_2019_tr_population | DP02_0063E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college, no degree |
| acs_ca_2019_tr_population | DP02_0063PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college, no degree |
| acs_ca_2019_tr_population | DP02_0064E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Associate's degree |
| acs_ca_2019_tr_population | DP02_0064PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Associate's degree |
| acs_ca_2019_tr_population | DP02_0065E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree |
| acs_ca_2019_tr_population | DP02_0065PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree |
| acs_ca_2019_tr_population | DP02_0066E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree |
| acs_ca_2019_tr_population | DP02_0066PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree |
| acs_ca_2019_tr_population | DP02_0067E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher |
| acs_ca_2019_tr_population | DP02_0067PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher |
| acs_ca_2019_tr_population | DP02_0068E | Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher |
| acs_ca_2019_tr_population | DP02_0068PE | Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher |
| acs_ca_2019_tr_population | DP02_0069E | Estimate!!VETERAN STATUS!!Civilian population 18 years and over |
| acs_ca_2019_tr_population | DP02_0069PE | Percent!!VETERAN STATUS!!Civilian population 18 years and over |
| acs_ca_2019_tr_population | DP02_0070E | Estimate!!VETERAN STATUS!!Civilian population 18 years and over!!Civilian veterans |
| acs_ca_2019_tr_population | DP02_0070PE | Percent!!VETERAN STATUS!!Civilian population 18 years and over!!Civilian veterans |
| acs_ca_2019_tr_population | DP02_0071E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population |
| acs_ca_2019_tr_population | DP02_0071PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population |
| acs_ca_2019_tr_population | DP02_0072E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population!!With a disability |
| acs_ca_2019_tr_population | DP02_0072PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population!!With a disability |
| acs_ca_2019_tr_population | DP02_0073E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years |
| acs_ca_2019_tr_population | DP02_0073PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years |
| acs_ca_2019_tr_population | DP02_0074E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years!!With a disability |
| acs_ca_2019_tr_population | DP02_0074PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years!!With a disability |
| acs_ca_2019_tr_population | DP02_0075E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years |
| acs_ca_2019_tr_population | DP02_0075PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years |
| acs_ca_2019_tr_population | DP02_0076E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years!!With a disability |
| acs_ca_2019_tr_population | DP02_0076PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years!!With a disability |
| acs_ca_2019_tr_population | DP02_0077E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over |
| acs_ca_2019_tr_population | DP02_0077PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over |
| acs_ca_2019_tr_population | DP02_0078E | Estimate!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over!!With a disability |
| acs_ca_2019_tr_population | DP02_0078PE | Percent!!DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over!!With a disability |
| acs_ca_2019_tr_population | DP02_0079E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over |
| acs_ca_2019_tr_population | DP02_0079PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over |
| acs_ca_2019_tr_population | DP02_0080E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Same house |
| acs_ca_2019_tr_population | DP02_0080PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Same house |
| acs_ca_2019_tr_population | DP02_0081E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S. |
| acs_ca_2019_tr_population | DP02_0081PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S. |
| acs_ca_2019_tr_population | DP02_0082E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Same county |
| acs_ca_2019_tr_population | DP02_0082PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Same county |
| acs_ca_2019_tr_population | DP02_0083E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county |
| acs_ca_2019_tr_population | DP02_0083PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county |
| acs_ca_2019_tr_population | DP02_0084E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county!!Same state |
| acs_ca_2019_tr_population | DP02_0084PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county!!Same state |
| acs_ca_2019_tr_population | DP02_0085E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county!!Different state |
| acs_ca_2019_tr_population | DP02_0085PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Different house in the U.S.!!Different county!!Different state |
| acs_ca_2019_tr_population | DP02_0086E | Estimate!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Abroad |
| acs_ca_2019_tr_population | DP02_0086PE | Percent!!RESIDENCE 1 YEAR AGO!!Population 1 year and over!!Abroad |
| acs_ca_2019_tr_population | DP02_0087E | Estimate!!PLACE OF BIRTH!!Total population |
| acs_ca_2019_tr_population | DP02_0087PE | Percent!!PLACE OF BIRTH!!Total population |
| acs_ca_2019_tr_population | DP02_0088E | Estimate!!PLACE OF BIRTH!!Total population!!Native |
| acs_ca_2019_tr_population | DP02_0088PE | Percent!!PLACE OF BIRTH!!Total population!!Native |
| acs_ca_2019_tr_population | DP02_0089E | Estimate!!PLACE OF BIRTH!!Total population!!Native!!Born in United States |
| acs_ca_2019_tr_population | DP02_0089PE | Percent!!PLACE OF BIRTH!!Total population!!Native!!Born in United States |
| acs_ca_2019_tr_population | DP02_0090E | Estimate!!PLACE OF BIRTH!!Total population!!Native!!Born in United States!!State of residence |
| acs_ca_2019_tr_population | DP02_0090PE | Percent!!PLACE OF BIRTH!!Total population!!Native!!Born in United States!!State of residence |
| acs_ca_2019_tr_population | DP02_0091E | Estimate!!PLACE OF BIRTH!!Total population!!Native!!Born in United States!!Different state |
| acs_ca_2019_tr_population | DP02_0091PE | Percent!!PLACE OF BIRTH!!Total population!!Native!!Born in United States!!Different state |
| acs_ca_2019_tr_population | DP02_0092E | Estimate!!PLACE OF BIRTH!!Total population!!Native!!Born in Puerto Rico, U.S. Island areas, or born abroad to American parent(s) |
| acs_ca_2019_tr_population | DP02_0092PE | Percent!!PLACE OF BIRTH!!Total population!!Native!!Born in Puerto Rico, U.S. Island areas, or born abroad to American parent(s) |
| acs_ca_2019_tr_population | DP02_0093E | Estimate!!PLACE OF BIRTH!!Total population!!Foreign born |
| acs_ca_2019_tr_population | DP02_0093PE | Percent!!PLACE OF BIRTH!!Total population!!Foreign born |
| acs_ca_2019_tr_population | DP02_0094E | Estimate!!U.S. CITIZENSHIP STATUS!!Foreign-born population |
| acs_ca_2019_tr_population | DP02_0094PE | Percent!!U.S. CITIZENSHIP STATUS!!Foreign-born population |
| acs_ca_2019_tr_population | DP02_0095E | Estimate!!U.S. CITIZENSHIP STATUS!!Foreign-born population!!Naturalized U.S. citizen |
| acs_ca_2019_tr_population | DP02_0095PE | Percent!!U.S. CITIZENSHIP STATUS!!Foreign-born population!!Naturalized U.S. citizen |
| acs_ca_2019_tr_population | DP02_0096E | Estimate!!U.S. CITIZENSHIP STATUS!!Foreign-born population!!Not a U.S. citizen |
| acs_ca_2019_tr_population | DP02_0096PE | Percent!!U.S. CITIZENSHIP STATUS!!Foreign-born population!!Not a U.S. citizen |
| acs_ca_2019_tr_population | DP02_0097E | Estimate!!YEAR OF ENTRY!!Population born outside the United States |
| acs_ca_2019_tr_population | DP02_0097PE | Percent!!YEAR OF ENTRY!!Population born outside the United States |
| acs_ca_2019_tr_population | DP02_0098E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Native |
| acs_ca_2019_tr_population | DP02_0098PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Native |
| acs_ca_2019_tr_population | DP02_0099E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Native!!Entered 2010 or later |
| acs_ca_2019_tr_population | DP02_0099PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Native!!Entered 2010 or later |
| acs_ca_2019_tr_population | DP02_0100E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Native!!Entered before 2010 |
| acs_ca_2019_tr_population | DP02_0100PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Native!!Entered before 2010 |
| acs_ca_2019_tr_population | DP02_0101E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born |
| acs_ca_2019_tr_population | DP02_0101PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born |
| acs_ca_2019_tr_population | DP02_0102E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born!!Entered 2010 or later |
| acs_ca_2019_tr_population | DP02_0102PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born!!Entered 2010 or later |
| acs_ca_2019_tr_population | DP02_0103E | Estimate!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born!!Entered before 2010 |
| acs_ca_2019_tr_population | DP02_0103PE | Percent!!YEAR OF ENTRY!!Population born outside the United States!!Foreign born!!Entered before 2010 |
| acs_ca_2019_tr_population | DP02_0104E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea |
| acs_ca_2019_tr_population | DP02_0104PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea |
| acs_ca_2019_tr_population | DP02_0105E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Europe |
| acs_ca_2019_tr_population | DP02_0105PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Europe |
| acs_ca_2019_tr_population | DP02_0106E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Asia |
| acs_ca_2019_tr_population | DP02_0106PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Asia |
| acs_ca_2019_tr_population | DP02_0107E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Africa |
| acs_ca_2019_tr_population | DP02_0107PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Africa |
| acs_ca_2019_tr_population | DP02_0108E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Oceania |
| acs_ca_2019_tr_population | DP02_0108PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Oceania |
| acs_ca_2019_tr_population | DP02_0109E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Latin America |
| acs_ca_2019_tr_population | DP02_0109PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Latin America |
| acs_ca_2019_tr_population | DP02_0110E | Estimate!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Northern America |
| acs_ca_2019_tr_population | DP02_0110PE | Percent!!WORLD REGION OF BIRTH OF FOREIGN BORN!!Foreign-born population, excluding population born at sea!!Northern America |
| acs_ca_2019_tr_population | DP02_0111E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over |
| acs_ca_2019_tr_population | DP02_0111PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over |
| acs_ca_2019_tr_population | DP02_0112E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!English only |
| acs_ca_2019_tr_population | DP02_0112PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!English only |
| acs_ca_2019_tr_population | DP02_0113E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Language other than English |
| acs_ca_2019_tr_population | DP02_0113PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Language other than English |
| acs_ca_2019_tr_population | DP02_0114E | "Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Language other than English!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0114PE | "Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Language other than English!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0115E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Spanish |
| acs_ca_2019_tr_population | DP02_0115PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Spanish |
| acs_ca_2019_tr_population | DP02_0116E | "Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Spanish!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0116PE | "Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Spanish!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0117E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other Indo-European languages |
| acs_ca_2019_tr_population | DP02_0117PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other Indo-European languages |
| acs_ca_2019_tr_population | DP02_0118E | "Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other Indo-European languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0118PE | "Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other Indo-European languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0119E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Asian and Pacific Islander languages |
| acs_ca_2019_tr_population | DP02_0119PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Asian and Pacific Islander languages |
| acs_ca_2019_tr_population | DP02_0120E | "Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Asian and Pacific Islander languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0120PE | "Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Asian and Pacific Islander languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0121E | Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other languages |
| acs_ca_2019_tr_population | DP02_0121PE | Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other languages |
| acs_ca_2019_tr_population | DP02_0122E | "Estimate!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0122PE | "Percent!!LANGUAGE SPOKEN AT HOME!!Population 5 years and over!!Other languages!!Speak English less than ""very well""" |
| acs_ca_2019_tr_population | DP02_0123E | Estimate!!ANCESTRY!!Total population |
| acs_ca_2019_tr_population | DP02_0123PE | Percent!!ANCESTRY!!Total population |
| acs_ca_2019_tr_population | DP02_0124E | Estimate!!ANCESTRY!!Total population!!American |
| acs_ca_2019_tr_population | DP02_0124PE | Percent!!ANCESTRY!!Total population!!American |
| acs_ca_2019_tr_population | DP02_0125E | Estimate!!ANCESTRY!!Total population!!Arab |
| acs_ca_2019_tr_population | DP02_0125PE | Percent!!ANCESTRY!!Total population!!Arab |
| acs_ca_2019_tr_population | DP02_0126E | Estimate!!ANCESTRY!!Total population!!Czech |
| acs_ca_2019_tr_population | DP02_0126PE | Percent!!ANCESTRY!!Total population!!Czech |
| acs_ca_2019_tr_population | DP02_0127E | Estimate!!ANCESTRY!!Total population!!Danish |
| acs_ca_2019_tr_population | DP02_0127PE | Percent!!ANCESTRY!!Total population!!Danish |
| acs_ca_2019_tr_population | DP02_0128E | Estimate!!ANCESTRY!!Total population!!Dutch |
| acs_ca_2019_tr_population | DP02_0128PE | Percent!!ANCESTRY!!Total population!!Dutch |
| acs_ca_2019_tr_population | DP02_0129E | Estimate!!ANCESTRY!!Total population!!English |
| acs_ca_2019_tr_population | DP02_0129PE | Percent!!ANCESTRY!!Total population!!English |
| acs_ca_2019_tr_population | DP02_0130E | Estimate!!ANCESTRY!!Total population!!French (except Basque) |
| acs_ca_2019_tr_population | DP02_0130PE | Percent!!ANCESTRY!!Total population!!French (except Basque) |
| acs_ca_2019_tr_population | DP02_0131E | Estimate!!ANCESTRY!!Total population!!French Canadian |
| acs_ca_2019_tr_population | DP02_0131PE | Percent!!ANCESTRY!!Total population!!French Canadian |
| acs_ca_2019_tr_population | DP02_0132E | Estimate!!ANCESTRY!!Total population!!German |
| acs_ca_2019_tr_population | DP02_0132PE | Percent!!ANCESTRY!!Total population!!German |
| acs_ca_2019_tr_population | DP02_0133E | Estimate!!ANCESTRY!!Total population!!Greek |
| acs_ca_2019_tr_population | DP02_0133PE | Percent!!ANCESTRY!!Total population!!Greek |
| acs_ca_2019_tr_population | DP02_0134E | Estimate!!ANCESTRY!!Total population!!Hungarian |
| acs_ca_2019_tr_population | DP02_0134PE | Percent!!ANCESTRY!!Total population!!Hungarian |
| acs_ca_2019_tr_population | DP02_0135E | Estimate!!ANCESTRY!!Total population!!Irish |
| acs_ca_2019_tr_population | DP02_0135PE | Percent!!ANCESTRY!!Total population!!Irish |
| acs_ca_2019_tr_population | DP02_0136E | Estimate!!ANCESTRY!!Total population!!Italian |
| acs_ca_2019_tr_population | DP02_0136PE | Percent!!ANCESTRY!!Total population!!Italian |
| acs_ca_2019_tr_population | DP02_0137E | Estimate!!ANCESTRY!!Total population!!Lithuanian |
| acs_ca_2019_tr_population | DP02_0137PE | Percent!!ANCESTRY!!Total population!!Lithuanian |
| acs_ca_2019_tr_population | DP02_0138E | Estimate!!ANCESTRY!!Total population!!Norwegian |
| acs_ca_2019_tr_population | DP02_0138PE | Percent!!ANCESTRY!!Total population!!Norwegian |
| acs_ca_2019_tr_population | DP02_0139E | Estimate!!ANCESTRY!!Total population!!Polish |
| acs_ca_2019_tr_population | DP02_0139PE | Percent!!ANCESTRY!!Total population!!Polish |
| acs_ca_2019_tr_population | DP02_0140E | Estimate!!ANCESTRY!!Total population!!Portuguese |
| acs_ca_2019_tr_population | DP02_0140PE | Percent!!ANCESTRY!!Total population!!Portuguese |
| acs_ca_2019_tr_population | DP02_0141E | Estimate!!ANCESTRY!!Total population!!Russian |
| acs_ca_2019_tr_population | DP02_0141PE | Percent!!ANCESTRY!!Total population!!Russian |
| acs_ca_2019_tr_population | DP02_0142E | Estimate!!ANCESTRY!!Total population!!Scotch-Irish |
| acs_ca_2019_tr_population | DP02_0142PE | Percent!!ANCESTRY!!Total population!!Scotch-Irish |
| acs_ca_2019_tr_population | DP02_0143E | Estimate!!ANCESTRY!!Total population!!Scottish |
| acs_ca_2019_tr_population | DP02_0143PE | Percent!!ANCESTRY!!Total population!!Scottish |
| acs_ca_2019_tr_population | DP02_0144E | Estimate!!ANCESTRY!!Total population!!Slovak |
| acs_ca_2019_tr_population | DP02_0144PE | Percent!!ANCESTRY!!Total population!!Slovak |
| acs_ca_2019_tr_population | DP02_0145E | Estimate!!ANCESTRY!!Total population!!Subsaharan African |
| acs_ca_2019_tr_population | DP02_0145PE | Percent!!ANCESTRY!!Total population!!Subsaharan African |
| acs_ca_2019_tr_population | DP02_0146E | Estimate!!ANCESTRY!!Total population!!Swedish |
| acs_ca_2019_tr_population | DP02_0146PE | Percent!!ANCESTRY!!Total population!!Swedish |
| acs_ca_2019_tr_population | DP02_0147E | Estimate!!ANCESTRY!!Total population!!Swiss |
| acs_ca_2019_tr_population | DP02_0147PE | Percent!!ANCESTRY!!Total population!!Swiss |
| acs_ca_2019_tr_population | DP02_0148E | Estimate!!ANCESTRY!!Total population!!Ukrainian |
| acs_ca_2019_tr_population | DP02_0148PE | Percent!!ANCESTRY!!Total population!!Ukrainian |
| acs_ca_2019_tr_population | DP02_0149E | Estimate!!ANCESTRY!!Total population!!Welsh |
| acs_ca_2019_tr_population | DP02_0149PE | Percent!!ANCESTRY!!Total population!!Welsh |
| acs_ca_2019_tr_population | DP02_0150E | Estimate!!ANCESTRY!!Total population!!West Indian (excluding Hispanic origin groups) |
| acs_ca_2019_tr_population | DP02_0150PE | Percent!!ANCESTRY!!Total population!!West Indian (excluding Hispanic origin groups) |
| acs_ca_2019_tr_population | DP03_0001E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over |
| acs_ca_2019_tr_population | DP03_0001PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over |
| acs_ca_2019_tr_population | DP03_0002E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force |
| acs_ca_2019_tr_population | DP03_0002PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force |
| acs_ca_2019_tr_population | DP03_0003E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force |
| acs_ca_2019_tr_population | DP03_0003PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force |
| acs_ca_2019_tr_population | DP03_0004E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Employed |
| acs_ca_2019_tr_population | DP03_0004PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Employed |
| acs_ca_2019_tr_population | DP03_0005E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed |
| acs_ca_2019_tr_population | DP03_0005PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed |
| acs_ca_2019_tr_population | DP03_0006E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Armed Forces |
| acs_ca_2019_tr_population | DP03_0006PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Armed Forces |
| acs_ca_2019_tr_population | DP03_0007E | Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!Not in labor force |
| acs_ca_2019_tr_population | DP03_0007PE | Percent!!EMPLOYMENT STATUS!!Population 16 years and over!!Not in labor force |
| acs_ca_2019_tr_population | DP03_0026E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0026PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0027E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over!!Management, business, science, and arts occupations |
| acs_ca_2019_tr_population | DP03_0027PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over!!Management, business, science, and arts occupations |
| acs_ca_2019_tr_population | DP03_0028E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over!!Service occupations |
| acs_ca_2019_tr_population | DP03_0028PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over!!Service occupations |
| acs_ca_2019_tr_population | DP03_0029E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over!!Sales and office occupations |
| acs_ca_2019_tr_population | DP03_0029PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over!!Sales and office occupations |
| acs_ca_2019_tr_population | DP03_0030E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over!!Natural resources, construction, and maintenance occupations |
| acs_ca_2019_tr_population | DP03_0030PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over!!Natural resources, construction, and maintenance occupations |
| acs_ca_2019_tr_population | DP03_0031E | Estimate!!OCCUPATION!!Civilian employed population 16 years and over!!Production, transportation, and material moving occupations |
| acs_ca_2019_tr_population | DP03_0031PE | Percent!!OCCUPATION!!Civilian employed population 16 years and over!!Production, transportation, and material moving occupations |
| acs_ca_2019_tr_population | DP03_0032E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0032PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0033E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Agriculture, forestry, fishing and hunting, and mining |
| acs_ca_2019_tr_population | DP03_0033PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Agriculture, forestry, fishing and hunting, and mining |
| acs_ca_2019_tr_population | DP03_0034E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Construction |
| acs_ca_2019_tr_population | DP03_0034PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Construction |
| acs_ca_2019_tr_population | DP03_0035E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Manufacturing |
| acs_ca_2019_tr_population | DP03_0035PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Manufacturing |
| acs_ca_2019_tr_population | DP03_0036E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Wholesale trade |
| acs_ca_2019_tr_population | DP03_0036PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Wholesale trade |
| acs_ca_2019_tr_population | DP03_0037E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Retail trade |
| acs_ca_2019_tr_population | DP03_0037PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Retail trade |
| acs_ca_2019_tr_population | DP03_0038E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_population | DP03_0038E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_population | DP03_0038PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_population | DP03_0038PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Transportation and warehousing, and utilities |
| acs_ca_2019_tr_population | DP03_0039E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Information |
| acs_ca_2019_tr_population | DP03_0039PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Information |
| acs_ca_2019_tr_population | DP03_0040E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Finance and insurance, and real estate and rental and leasing |
| acs_ca_2019_tr_population | DP03_0040PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Finance and insurance, and real estate and rental and leasing |
| acs_ca_2019_tr_population | DP03_0041E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Professional, scientific, and management, and administrative and waste management services |
| acs_ca_2019_tr_population | DP03_0041PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Professional, scientific, and management, and administrative and waste management services |
| acs_ca_2019_tr_population | DP03_0042E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Educational services, and health care and social assistance |
| acs_ca_2019_tr_population | DP03_0042PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Educational services, and health care and social assistance |
| acs_ca_2019_tr_population | DP03_0043E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Arts, entertainment, and recreation, and accommodation and food services |
| acs_ca_2019_tr_population | DP03_0043PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Arts, entertainment, and recreation, and accommodation and food services |
| acs_ca_2019_tr_population | DP03_0044E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Other services, except public administration |
| acs_ca_2019_tr_population | DP03_0044PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Other services, except public administration |
| acs_ca_2019_tr_population | DP03_0045E | Estimate!!INDUSTRY!!Civilian employed population 16 years and over!!Public administration |
| acs_ca_2019_tr_population | DP03_0045PE | Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Public administration |
| acs_ca_2019_tr_population | DP03_0046E | Estimate!!CLASS OF WORKER!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0046PE | Percent!!CLASS OF WORKER!!Civilian employed population 16 years and over |
| acs_ca_2019_tr_population | DP03_0047E | Estimate!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Private wage and salary workers |
| acs_ca_2019_tr_population | DP03_0047PE | Percent!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Private wage and salary workers |
| acs_ca_2019_tr_population | DP03_0048E | Estimate!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Government workers |
| acs_ca_2019_tr_population | DP03_0048PE | Percent!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Government workers |
| acs_ca_2019_tr_population | DP03_0049E | Estimate!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Self-employed in own not incorporated business workers |
| acs_ca_2019_tr_population | DP03_0049PE | Percent!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Self-employed in own not incorporated business workers |
| acs_ca_2019_tr_population | DP03_0050E | Estimate!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Unpaid family workers |
| acs_ca_2019_tr_population | DP03_0050PE | Percent!!CLASS OF WORKER!!Civilian employed population 16 years and over!!Unpaid family workers |
| acs_ca_2019_tr_population | DP03_0095E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population |
| acs_ca_2019_tr_population | DP03_0095PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population |
| acs_ca_2019_tr_population | DP03_0096E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0096PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0097E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0097PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0098E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0098PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0099E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0099PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0100E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population under 19 years |
| acs_ca_2019_tr_population | DP03_0100PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population under 19 years |
| acs_ca_2019_tr_population | DP03_0101E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population under 19 years!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0101PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population under 19 years!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0102E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years |
| acs_ca_2019_tr_population | DP03_0102PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years |
| acs_ca_2019_tr_population | DP03_0103E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force: |
| acs_ca_2019_tr_population | DP03_0103PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force: |
| acs_ca_2019_tr_population | DP03_0104E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed: |
| acs_ca_2019_tr_population | DP03_0104PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed: |
| acs_ca_2019_tr_population | DP03_0105E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0105PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0106E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0106PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0107E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0107PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0108E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0108PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Employed:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0109E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed: |
| acs_ca_2019_tr_population | DP03_0109PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed: |
| acs_ca_2019_tr_population | DP03_0110E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0110PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0111E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0111PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0112E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0112PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0113E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0113PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!In labor force:!!Unemployed:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0114E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force: |
| acs_ca_2019_tr_population | DP03_0114PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force: |
| acs_ca_2019_tr_population | DP03_0115E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0115PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage |
| acs_ca_2019_tr_population | DP03_0116E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0116PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage!!With private health insurance |
| acs_ca_2019_tr_population | DP03_0117E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0117PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!With health insurance coverage!!With public coverage |
| acs_ca_2019_tr_population | DP03_0118E | Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP03_0118PE | Percent!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population 19 to 64 years!!Not in labor force:!!No health insurance coverage |
| acs_ca_2019_tr_population | DP05_0001E | Estimate!!SEX AND AGE!!Total population |
| acs_ca_2019_tr_population | DP05_0001PE | Percent!!SEX AND AGE!!Total population |
| acs_ca_2019_tr_population | DP05_0002E | Estimate!!SEX AND AGE!!Total population!!Male |
| acs_ca_2019_tr_population | DP05_0002PE | Percent!!SEX AND AGE!!Total population!!Male |
| acs_ca_2019_tr_population | DP05_0003E | Estimate!!SEX AND AGE!!Total population!!Female |
| acs_ca_2019_tr_population | DP05_0003PE | Percent!!SEX AND AGE!!Total population!!Female |
| acs_ca_2019_tr_population | DP05_0004E | Estimate!!SEX AND AGE!!Total population!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0004PE | Percent!!SEX AND AGE!!Total population!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0005E | Estimate!!SEX AND AGE!!Total population!!Under 5 years |
| acs_ca_2019_tr_population | DP05_0005PE | Percent!!SEX AND AGE!!Total population!!Under 5 years |
| acs_ca_2019_tr_population | DP05_0006E | Estimate!!SEX AND AGE!!Total population!!5 to 9 years |
| acs_ca_2019_tr_population | DP05_0006PE | Percent!!SEX AND AGE!!Total population!!5 to 9 years |
| acs_ca_2019_tr_population | DP05_0007E | Estimate!!SEX AND AGE!!Total population!!10 to 14 years |
| acs_ca_2019_tr_population | DP05_0007PE | Percent!!SEX AND AGE!!Total population!!10 to 14 years |
| acs_ca_2019_tr_population | DP05_0008E | Estimate!!SEX AND AGE!!Total population!!15 to 19 years |
| acs_ca_2019_tr_population | DP05_0008PE | Percent!!SEX AND AGE!!Total population!!15 to 19 years |
| acs_ca_2019_tr_population | DP05_0009E | Estimate!!SEX AND AGE!!Total population!!20 to 24 years |
| acs_ca_2019_tr_population | DP05_0009PE | Percent!!SEX AND AGE!!Total population!!20 to 24 years |
| acs_ca_2019_tr_population | DP05_0010E | Estimate!!SEX AND AGE!!Total population!!25 to 34 years |
| acs_ca_2019_tr_population | DP05_0010PE | Percent!!SEX AND AGE!!Total population!!25 to 34 years |
| acs_ca_2019_tr_population | DP05_0011E | Estimate!!SEX AND AGE!!Total population!!35 to 44 years |
| acs_ca_2019_tr_population | DP05_0011PE | Percent!!SEX AND AGE!!Total population!!35 to 44 years |
| acs_ca_2019_tr_population | DP05_0012E | Estimate!!SEX AND AGE!!Total population!!45 to 54 years |
| acs_ca_2019_tr_population | DP05_0012PE | Percent!!SEX AND AGE!!Total population!!45 to 54 years |
| acs_ca_2019_tr_population | DP05_0013E | Estimate!!SEX AND AGE!!Total population!!55 to 59 years |
| acs_ca_2019_tr_population | DP05_0013PE | Percent!!SEX AND AGE!!Total population!!55 to 59 years |
| acs_ca_2019_tr_population | DP05_0014E | Estimate!!SEX AND AGE!!Total population!!60 to 64 years |
| acs_ca_2019_tr_population | DP05_0014PE | Percent!!SEX AND AGE!!Total population!!60 to 64 years |
| acs_ca_2019_tr_population | DP05_0015E | Estimate!!SEX AND AGE!!Total population!!65 to 74 years |
| acs_ca_2019_tr_population | DP05_0015PE | Percent!!SEX AND AGE!!Total population!!65 to 74 years |
| acs_ca_2019_tr_population | DP05_0016E | Estimate!!SEX AND AGE!!Total population!!75 to 84 years |
| acs_ca_2019_tr_population | DP05_0016PE | Percent!!SEX AND AGE!!Total population!!75 to 84 years |
| acs_ca_2019_tr_population | DP05_0017E | Estimate!!SEX AND AGE!!Total population!!85 years and over |
| acs_ca_2019_tr_population | DP05_0017PE | Percent!!SEX AND AGE!!Total population!!85 years and over |
| acs_ca_2019_tr_population | DP05_0018E | Estimate!!SEX AND AGE!!Total population!!Median age (years) |
| acs_ca_2019_tr_population | DP05_0018PE | Percent!!SEX AND AGE!!Total population!!Median age (years) |
| acs_ca_2019_tr_population | DP05_0019E | Estimate!!SEX AND AGE!!Total population!!Under 18 years |
| acs_ca_2019_tr_population | DP05_0019PE | Percent!!SEX AND AGE!!Total population!!Under 18 years |
| acs_ca_2019_tr_population | DP05_0020E | Estimate!!SEX AND AGE!!Total population!!16 years and over |
| acs_ca_2019_tr_population | DP05_0020PE | Percent!!SEX AND AGE!!Total population!!16 years and over |
| acs_ca_2019_tr_population | DP05_0021E | Estimate!!SEX AND AGE!!Total population!!18 years and over |
| acs_ca_2019_tr_population | DP05_0021PE | Percent!!SEX AND AGE!!Total population!!18 years and over |
| acs_ca_2019_tr_population | DP05_0022E | Estimate!!SEX AND AGE!!Total population!!21 years and over |
| acs_ca_2019_tr_population | DP05_0022PE | Percent!!SEX AND AGE!!Total population!!21 years and over |
| acs_ca_2019_tr_population | DP05_0023E | Estimate!!SEX AND AGE!!Total population!!62 years and over |
| acs_ca_2019_tr_population | DP05_0023PE | Percent!!SEX AND AGE!!Total population!!62 years and over |
| acs_ca_2019_tr_population | DP05_0024E | Estimate!!SEX AND AGE!!Total population!!65 years and over |
| acs_ca_2019_tr_population | DP05_0024PE | Percent!!SEX AND AGE!!Total population!!65 years and over |
| acs_ca_2019_tr_population | DP05_0025E | Estimate!!SEX AND AGE!!Total population!!18 years and over |
| acs_ca_2019_tr_population | DP05_0025PE | Percent!!SEX AND AGE!!Total population!!18 years and over |
| acs_ca_2019_tr_population | DP05_0026E | Estimate!!SEX AND AGE!!Total population!!18 years and over!!Male |
| acs_ca_2019_tr_population | DP05_0026PE | Percent!!SEX AND AGE!!Total population!!18 years and over!!Male |
| acs_ca_2019_tr_population | DP05_0027E | Estimate!!SEX AND AGE!!Total population!!18 years and over!!Female |
| acs_ca_2019_tr_population | DP05_0027PE | Percent!!SEX AND AGE!!Total population!!18 years and over!!Female |
| acs_ca_2019_tr_population | DP05_0028E | Estimate!!SEX AND AGE!!Total population!!18 years and over!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0028PE | Percent!!SEX AND AGE!!Total population!!18 years and over!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0029E | Estimate!!SEX AND AGE!!Total population!!65 years and over |
| acs_ca_2019_tr_population | DP05_0029PE | Percent!!SEX AND AGE!!Total population!!65 years and over |
| acs_ca_2019_tr_population | DP05_0030E | Estimate!!SEX AND AGE!!Total population!!65 years and over!!Male |
| acs_ca_2019_tr_population | DP05_0030PE | Percent!!SEX AND AGE!!Total population!!65 years and over!!Male |
| acs_ca_2019_tr_population | DP05_0031E | Estimate!!SEX AND AGE!!Total population!!65 years and over!!Female |
| acs_ca_2019_tr_population | DP05_0031PE | Percent!!SEX AND AGE!!Total population!!65 years and over!!Female |
| acs_ca_2019_tr_population | DP05_0032E | Estimate!!SEX AND AGE!!Total population!!65 years and over!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0032PE | Percent!!SEX AND AGE!!Total population!!65 years and over!!Sex ratio (males per 100 females) |
| acs_ca_2019_tr_population | DP05_0033E | Estimate!!RACE!!Total population |
| acs_ca_2019_tr_population | DP05_0033PE | Percent!!RACE!!Total population |
| acs_ca_2019_tr_population | DP05_0034E | Estimate!!RACE!!Total population!!One race |
| acs_ca_2019_tr_population | DP05_0034PE | Percent!!RACE!!Total population!!One race |
| acs_ca_2019_tr_population | DP05_0035E | Estimate!!RACE!!Total population!!Two or more races |
| acs_ca_2019_tr_population | DP05_0035PE | Percent!!RACE!!Total population!!Two or more races |
| acs_ca_2019_tr_population | DP05_0036E | Estimate!!RACE!!Total population!!One race |
| acs_ca_2019_tr_population | DP05_0036PE | Percent!!RACE!!Total population!!One race |
| acs_ca_2019_tr_population | DP05_0037E | Estimate!!RACE!!Total population!!One race!!White |
| acs_ca_2019_tr_population | DP05_0037PE | Percent!!RACE!!Total population!!One race!!White |
| acs_ca_2019_tr_population | DP05_0038E | Estimate!!RACE!!Total population!!One race!!Black or African American |
| acs_ca_2019_tr_population | DP05_0038PE | Percent!!RACE!!Total population!!One race!!Black or African American |
| acs_ca_2019_tr_population | DP05_0039E | Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0039PE | Percent!!RACE!!Total population!!One race!!American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0040E | Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Cherokee tribal grouping |
| acs_ca_2019_tr_population | DP05_0040PE | Percent!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Cherokee tribal grouping |
| acs_ca_2019_tr_population | DP05_0041E | Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Chippewa tribal grouping |
| acs_ca_2019_tr_population | DP05_0041PE | Percent!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Chippewa tribal grouping |
| acs_ca_2019_tr_population | DP05_0042E | Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Navajo tribal grouping |
| acs_ca_2019_tr_population | DP05_0042PE | Percent!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Navajo tribal grouping |
| acs_ca_2019_tr_population | DP05_0043E | Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Sioux tribal grouping |
| acs_ca_2019_tr_population | DP05_0043PE | Percent!!RACE!!Total population!!One race!!American Indian and Alaska Native!!Sioux tribal grouping |
| acs_ca_2019_tr_population | DP05_0044E | Estimate!!RACE!!Total population!!One race!!Asian |
| acs_ca_2019_tr_population | DP05_0044PE | Percent!!RACE!!Total population!!One race!!Asian |
| acs_ca_2019_tr_population | DP05_0045E | Estimate!!RACE!!Total population!!One race!!Asian!!Asian Indian |
| acs_ca_2019_tr_population | DP05_0045PE | Percent!!RACE!!Total population!!One race!!Asian!!Asian Indian |
| acs_ca_2019_tr_population | DP05_0046E | Estimate!!RACE!!Total population!!One race!!Asian!!Chinese |
| acs_ca_2019_tr_population | DP05_0046PE | Percent!!RACE!!Total population!!One race!!Asian!!Chinese |
| acs_ca_2019_tr_population | DP05_0047E | Estimate!!RACE!!Total population!!One race!!Asian!!Filipino |
| acs_ca_2019_tr_population | DP05_0047PE | Percent!!RACE!!Total population!!One race!!Asian!!Filipino |
| acs_ca_2019_tr_population | DP05_0048E | Estimate!!RACE!!Total population!!One race!!Asian!!Japanese |
| acs_ca_2019_tr_population | DP05_0048PE | Percent!!RACE!!Total population!!One race!!Asian!!Japanese |
| acs_ca_2019_tr_population | DP05_0049E | Estimate!!RACE!!Total population!!One race!!Asian!!Korean |
| acs_ca_2019_tr_population | DP05_0049PE | Percent!!RACE!!Total population!!One race!!Asian!!Korean |
| acs_ca_2019_tr_population | DP05_0050E | Estimate!!RACE!!Total population!!One race!!Asian!!Vietnamese |
| acs_ca_2019_tr_population | DP05_0050PE | Percent!!RACE!!Total population!!One race!!Asian!!Vietnamese |
| acs_ca_2019_tr_population | DP05_0051E | Estimate!!RACE!!Total population!!One race!!Asian!!Other Asian |
| acs_ca_2019_tr_population | DP05_0051PE | Percent!!RACE!!Total population!!One race!!Asian!!Other Asian |
| acs_ca_2019_tr_population | DP05_0052E | Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0052PE | Percent!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0053E | Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Native Hawaiian |
| acs_ca_2019_tr_population | DP05_0053PE | Percent!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Native Hawaiian |
| acs_ca_2019_tr_population | DP05_0054E | Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Guamanian or Chamorro |
| acs_ca_2019_tr_population | DP05_0054PE | Percent!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Guamanian or Chamorro |
| acs_ca_2019_tr_population | DP05_0055E | Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Samoan |
| acs_ca_2019_tr_population | DP05_0055PE | Percent!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Samoan |
| acs_ca_2019_tr_population | DP05_0056E | Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0056PE | Percent!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander!!Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0057E | Estimate!!RACE!!Total population!!One race!!Some other race |
| acs_ca_2019_tr_population | DP05_0057PE | Percent!!RACE!!Total population!!One race!!Some other race |
| acs_ca_2019_tr_population | DP05_0058E | Estimate!!RACE!!Total population!!Two or more races |
| acs_ca_2019_tr_population | DP05_0058PE | Percent!!RACE!!Total population!!Two or more races |
| acs_ca_2019_tr_population | DP05_0059E | Estimate!!RACE!!Total population!!Two or more races!!White and Black or African American |
| acs_ca_2019_tr_population | DP05_0059PE | Percent!!RACE!!Total population!!Two or more races!!White and Black or African American |
| acs_ca_2019_tr_population | DP05_0060E | Estimate!!RACE!!Total population!!Two or more races!!White and American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0060PE | Percent!!RACE!!Total population!!Two or more races!!White and American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0061E | Estimate!!RACE!!Total population!!Two or more races!!White and Asian |
| acs_ca_2019_tr_population | DP05_0061PE | Percent!!RACE!!Total population!!Two or more races!!White and Asian |
| acs_ca_2019_tr_population | DP05_0062E | Estimate!!RACE!!Total population!!Two or more races!!Black or African American and American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0062PE | Percent!!RACE!!Total population!!Two or more races!!Black or African American and American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0063E | Estimate!!Race alone or in combination with one or more other races!!Total population |
| acs_ca_2019_tr_population | DP05_0063PE | Percent!!Race alone or in combination with one or more other races!!Total population |
| acs_ca_2019_tr_population | DP05_0064E | Estimate!!Race alone or in combination with one or more other races!!Total population!!White |
| acs_ca_2019_tr_population | DP05_0064PE | Percent!!Race alone or in combination with one or more other races!!Total population!!White |
| acs_ca_2019_tr_population | DP05_0065E | Estimate!!Race alone or in combination with one or more other races!!Total population!!Black or African American |
| acs_ca_2019_tr_population | DP05_0065PE | Percent!!Race alone or in combination with one or more other races!!Total population!!Black or African American |
| acs_ca_2019_tr_population | DP05_0066E | Estimate!!Race alone or in combination with one or more other races!!Total population!!American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0066PE | Percent!!Race alone or in combination with one or more other races!!Total population!!American Indian and Alaska Native |
| acs_ca_2019_tr_population | DP05_0067E | Estimate!!Race alone or in combination with one or more other races!!Total population!!Asian |
| acs_ca_2019_tr_population | DP05_0067PE | Percent!!Race alone or in combination with one or more other races!!Total population!!Asian |
| acs_ca_2019_tr_population | DP05_0068E | Estimate!!Race alone or in combination with one or more other races!!Total population!!Native Hawaiian and Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0068PE | Percent!!Race alone or in combination with one or more other races!!Total population!!Native Hawaiian and Other Pacific Islander |
| acs_ca_2019_tr_population | DP05_0069E | Estimate!!Race alone or in combination with one or more other races!!Total population!!Some other race |
| acs_ca_2019_tr_population | DP05_0069PE | Percent!!Race alone or in combination with one or more other races!!Total population!!Some other race |
| acs_ca_2019_tr_population | DP05_0070E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population |
| acs_ca_2019_tr_population | DP05_0070PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population |
| acs_ca_2019_tr_population | DP05_0071E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race) |
| acs_ca_2019_tr_population | DP05_0071PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race) |
| acs_ca_2019_tr_population | DP05_0072E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Mexican |
| acs_ca_2019_tr_population | DP05_0072PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Mexican |
| acs_ca_2019_tr_population | DP05_0073E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Puerto Rican |
| acs_ca_2019_tr_population | DP05_0073PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Puerto Rican |
| acs_ca_2019_tr_population | DP05_0074E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Cuban |
| acs_ca_2019_tr_population | DP05_0074PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Cuban |
| acs_ca_2019_tr_population | DP05_0075E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Other Hispanic or Latino |
| acs_ca_2019_tr_population | DP05_0075PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)!!Other Hispanic or Latino |
| acs_ca_2019_tr_population | DP05_0076E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino |
| acs_ca_2019_tr_population | DP05_0076PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino |
| acs_ca_2019_tr_population | DP05_0077E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!White alone |
| acs_ca_2019_tr_population | DP05_0077PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!White alone |
| acs_ca_2019_tr_population | DP05_0078E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Black or African American alone |
| acs_ca_2019_tr_population | DP05_0078PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Black or African American alone |
| acs_ca_2019_tr_population | DP05_0079E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!American Indian and Alaska Native alone |
| acs_ca_2019_tr_population | DP05_0079PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!American Indian and Alaska Native alone |
| acs_ca_2019_tr_population | DP05_0080E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Asian alone |
| acs_ca_2019_tr_population | DP05_0080PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Asian alone |
| acs_ca_2019_tr_population | DP05_0081E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Native Hawaiian and Other Pacific Islander alone |
| acs_ca_2019_tr_population | DP05_0081PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Native Hawaiian and Other Pacific Islander alone |
| acs_ca_2019_tr_population | DP05_0082E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Some other race alone |
| acs_ca_2019_tr_population | DP05_0082PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Some other race alone |
| acs_ca_2019_tr_population | DP05_0083E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races |
| acs_ca_2019_tr_population | DP05_0083PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races |
| acs_ca_2019_tr_population | DP05_0084E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races!!Two races including Some other race |
| acs_ca_2019_tr_population | DP05_0084PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races!!Two races including Some other race |
| acs_ca_2019_tr_population | DP05_0085E | Estimate!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races!!Two races excluding Some other race, and Three or more races |
| acs_ca_2019_tr_population | DP05_0085PE | Percent!!HISPANIC OR LATINO AND RACE!!Total population!!Not Hispanic or Latino!!Two or more races!!Two races excluding Some other race, and Three or more races |
| acs_ca_2019_tr_population | DP05_0087E | Estimate!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population |
| acs_ca_2019_tr_population | DP05_0087PE | Percent!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population |
| acs_ca_2019_tr_population | DP05_0088E | Estimate!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population!!Male |
| acs_ca_2019_tr_population | DP05_0088PE | Percent!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population!!Male |
| acs_ca_2019_tr_population | DP05_0089E | Estimate!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population!!Female |
| acs_ca_2019_tr_population | DP05_0089PE | Percent!!CITIZEN, VOTING AGE POPULATION!!Citizen, 18 and over population!!Female |
| acs_ca_2019_tr_population | GEOID | Geographic Idenification Code |
| acs_ca_2019_tr_population | NAME | Tract Name|
| acs_ca_2019_unincorporated_geom | aland | Land Area |
| acs_ca_2019_unincorporated_geom | awater | Water Area |
| acs_ca_2019_unincorporated_geom | cbsafp | Core Based Statistical Area |
| acs_ca_2019_unincorporated_geom | classfp | Class FIPS Code |
| acs_ca_2019_unincorporated_geom | countyfp | County FIPS Code |
| acs_ca_2019_unincorporated_geom | countyns | ANSI County Code |
| acs_ca_2019_unincorporated_geom | csafp | Geographic Entity Class Code  |
| acs_ca_2019_unincorporated_geom | funcstat | Functional Status Code |
| acs_ca_2019_unincorporated_geom | geoid | Geographic Identification Code |
| acs_ca_2019_unincorporated_geom | geom | Geometry |
| acs_ca_2019_unincorporated_geom | intptlat | Latitude of Internal Point |
| acs_ca_2019_unincorporated_geom | intptlon | Longitude of Internal Point |
| acs_ca_2019_unincorporated_geom | lsad | Legal/Statistical Area Description Code |
| acs_ca_2019_unincorporated_geom | metdivfp | Metropolitan division code |
| acs_ca_2019_unincorporated_geom | mtfcc | MAF/Tiger Feature Class Code |
| acs_ca_2019_unincorporated_geom | name | County Name |
| acs_ca_2019_unincorporated_geom | namelsad | County Name with translated Legal/Statistical Area Description |
| acs_ca_2019_unincorporated_geom | ogc_fid | OGC Feature Identifidation Code (Autogenerated) |
| acs_ca_2019_unincorporated_geom | pcicbsa | Metropolitan or micropolitan statistical area principal city indicator |
| acs_ca_2019_unincorporated_geom | pcinecta | City and town area principal city indicator |
| acs_ca_2019_unincorporated_geom | placefp | Place FIPS Code |
| acs_ca_2019_unincorporated_geom | placens | Place ANSI Code |
| acs_ca_2019_unincorporated_geom | statefp | State FIPS Code |
