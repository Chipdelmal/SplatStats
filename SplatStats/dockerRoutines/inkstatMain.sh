#!/bin/bash

###############################################################################
# Args breakdown
#   --season:
#   --titles:
#   --gmode:
#   --overwrite: 
#   --dpi:
###############################################################################
season=${player:-All}
titles=${titles:-True}
gmode=${gmode:-All}
overwrite=${overwrite:-True}
dpi=${dpi:500}
###############################################################################
# Get args
###############################################################################
while [ $# -gt 0 ]; do
    if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
    fi
    shift
done
###############################################################################
# Constants and Welcome
###############################################################################
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
RED='\033[0;31m'
printf "${RED}*****************************************************************************************************\n"
printf "${RED}* Welcome to SplatStats!!!!!!!!!!!!${CLEAR}\n"
printf "${RED}\t Please visit our github repo for more info: https://github.com/Chipdelmal/SplatStats${CLEAR}\n"
printf "${RED}*****************************************************************************************************\n"
###############################################################################
# Run SplatStats scripts
###############################################################################
printf "${BLUE}* Processing https://stat.ink/downloads data with SplatStats...${CLEAR}\n"
printf "${BLUE}\t Season: ${season}${CLEAR}\n"
printf "${BLUE}\t Game Mode: ${gmode}${CLEAR}\n"
printf "${BLUE}\t Titles: ${titles}${CLEAR}\n"
printf "${BLUE}\t Overwrite: ${overwrite}${CLEAR}\n"
printf "${BLUE}\t DPI: ${dpi}${CLEAR}\n"
# Analyze the data --------------------------------------------------------
mkdir -p /data/battle-results-csv
mkdir -p /data/statInk
cd ~
python /SplatStats/SplatStats/dockerRoutines/inkstatMain.py "$season" "$gmode" "$titles" "$overwrite" "$dpi"
