# Set working directory

chdir /Users/edf/repos/carb_elec/data/carb_priority_populations/

# Download CARB Priority Population Geodatabase

url='https://ww2.arb.ca.gov/sites/default/files/auction-proceeds/map/PriorityPopulations2022CES4.gdb.zip';
curl -o carb_priority_populations.gdb.zip $url;
mkdir raw;
unzip carb_priority_populations.gdb.zip -d ./raw;
rm carb_priority_populations.gdb.zip;
