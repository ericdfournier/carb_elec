#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Orchestrate Import Sub-Routines
################################################################################

# Import Census American Community Survey
echo "Importing Census American Community Survey Data"
./census_american_community_survey/import.sh

# Import CARB Priority Populations Data
echo "Importing CARB Priority Populations Data..."
./carb_priority_populations/import.sh

# Import CARB Boundaries Data
echo "Importing CARB Boundaries Data..."
./carb_boundaries/import.sh

# Import CDPH Climate Hazard and Vulnerability Index Data
echo "Importing CDPH Hazard Vulnerability Index Data..."
./cdph_climate_hazard_vulnerability_index/import.sh

# Import CEC Building Climate Zone Data
echo "Importing CEC Climate Zone Data..."
./cec_climate_zones/import.sh

# Import CEDARS Fuel Substitution Program Claims Data
echo "Importing CEDARS Fuel Substitution Program Claims Data..."
./cedars_fuel_substitution_program_claims/import.sh

# Import Community Choice Aggregations Data
echo "Importing Community Choice Aggregations Data..."
./community_choice_aggregations/import.sh

# Import CPUC Utility Affordability Ratio Data
echo "Importing CPUC Utility Affordability Ratio Data..."
./cpuc_utility_affordability_ratios/import.sh

# Import DOE Lead Tool Data
echo "Importing DOE Lead Tool Data..."
./cpuc_utility_affordability_ratios/import.sh

# Import HUD Income Limit Data
echo "Importing HUD Income Limit Data..."
./hud_income_limits/import.sh

# Import OEHHA CalEnviroScreen-4.0 Data
echo "Importing OEHHA CalEnviroScreen-4.0 Data..."
./oehha_cal_enviro_screen_4/import.sh

# Import Regional Energy Network Data
echo "Importing Regional Energy Network Data"
./regional_energy_networks/import.sh

# Import PGE Grid Data
echo "Importing PGE Grid Data..."
./pge_grid/import.sh

# Import SCE Grid Data
echo "Importing SCE Grid Data..."
./sce_grid/import.sh

# Import SDGE Grid Data
echo "Importing SDGE Grid Data..."
./sdge_grid/import.sh

# Import USEPA eGRID Data
echo "Importing USEPA eGRID Data..."
./usepa_egrid/import.sh

#%% Create Master Dump File
pg_dump carb > ./dump/sql/carb_dump.sql;
zip ./dump/sql/carb_dump.zip ./dump/sql/carb_dump.sql;
rm ./dump/sql/carb_dump.sql;
