#!/bin/bash

###############################################################################
# Args breakdown
#   --player: Username string (Defaults to "None" and skips SplatStats)[eg. --player 'chip ウナギ']
#   --weapon: Weapon's string (Defaults to "All") [eg. --weapon 'Hero Shot Replica']
#   --matchMode: Match mode string (Defaults to "All") [eg. --matchMode 'Turf War']
#   --download: Determines if s3s should be used to download the data (Defaults to "False") [eg. --download True]
#   --upload: Determines if s3s should be used to upload the missing data to stat.ink (Defaults to "False") [eg. --upload True]
#   --overwrite: 
###############################################################################
player=${player:-None}
weapon=${weapon:-All}
matchMode=${matchMode:-All}
download=${download:-False}
upload=${upload:-False}
overwrite=${overwrite:-True}
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
printf "${RED}* Welcome to SplatStats!!!!!!!!!!!!${CLEAR}\n"
printf "${RED}\t Please visit our github repo for more info: https://github.com/Chipdelmal/SplatStats${CLEAR}"
###############################################################################
# Run s3s scraper
###############################################################################
if [[ "$download" == "False" ]]; then
    printf "\n${BLUE}* [1/3] Skipping data download...${CLEAR}\n"
else
    printf "\n${BLUE}* [1/3] Downloading config.txt's data with s3s...${CLEAR}\n"
    printf "${BLUE}\t s3s is a third-party software not designed by the SplatStats team, please visit https://github.com/frozenpandaman/s3s for more info and to support the devs! ${CLEAR}\n"
    # Scrape data -------------------------------------------------------------
    mkdir -p /data/jsons
    cd /data/jsons
    printf "n\n" | python /other/s3s/s3s.py -o
fi
###############################################################################
# Run SplatStats scripts
###############################################################################
if [[ "$player" == "None" ]]; then
    printf "\n${BLUE}* [2/3] No player name was provided, skipping...${CLEAR}\n"
else
    printf "\n${BLUE}* [2/3] Processing data with SplatStats...${CLEAR}\n"
    printf "${BLUE}\t Player: ${player}${CLEAR}\n"
    printf "${BLUE}\t Weapon: ${weapon}${CLEAR}\n"
    printf "${BLUE}\t Match Modes: ${matchMode}${CLEAR}\n"
    printf "${BLUE}\t Overwrite Battles: ${overwrite}${CLEAR}\n\n"
    # Analyze the data --------------------------------------------------------
    mkdir -p /data/battles
    cd ~
    python /SplatStats/dockerRoutines/dockerPlots.py "$player" "$weapon" "$matchMode" "$overwrite"
fi
###############################################################################
# Upload s3s to stat.ink
###############################################################################
if [[ "$upload" == "False" ]]; then
    printf "\n${BLUE}* [3/3] Skipping data upload to stat.ink ...${CLEAR}\n"
else
    printf "\n${BLUE}* [3/3] Uploading required data to stat.ink ...${CLEAR}\n"
    printf "${BLUE}\t s3s is a third-party software not designed by the SplatStats team, please visit https://github.com/frozenpandaman/s3s for more info and to support the devs! ${CLEAR}\n"
    # Upload data -------------------------------------------------------------
    mkdir -p /data/jsons
    cd /data/jsons
    printf "n\n" | python /other/s3s/s3s.py -r
fi