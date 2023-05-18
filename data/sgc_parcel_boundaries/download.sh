#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Download California Statewide Parcel Boundaries
#
# Source: https://hub.arcgis.com/documents/lacounty::california-statewide-parcel-boundaries/about
#
# Rename files to *.gdp.zip to read directly without unzipping.
#
# The lacounty server has bad certificates so use http. To use https requires
# -k, --insecure (curl) or --no-check-certificate (wget).
#
# # Curl Options
#
# -R
#   Retain file times from server.
#   Wget does this automatically.
#
# -C, --continue-at -
#   Resume transfer, also prevent overwrite/redownload if file exists.
#   For Wget use the -c, --continue option to resume partial downloads. By
#   default Wget will back up existing file as *.1 and redownload.
################################################################################

curl -R -C - -o ./raw/Parcels_CA_2014.gdb.zip http://egis4.gis.lacounty.gov/HubData/Parcels_CA_2014.zip

# Unzip file. Use -n option to never overwrite existing files.
unzip -n ./raw/Parcels_CA_2014.gdb.zip
