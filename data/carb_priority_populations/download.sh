# Set working directory

chdir /Users/edf/repos/carb_elec/data/

# CARB Priority Population Geodatabase

url='https://ww2.arb.ca.gov/sites/default/files/auction-proceeds/map/PriorityPopulations2022CES4.gdb.zip';
curl -o carb_priority_populations.gdb.zip $url;
mkdir ./carb_priority_populations;
unzip carb_priority_populations.gdb.zip -d ./carb_priority_populations;
rm carb_priority_populations.gdb.zip;
