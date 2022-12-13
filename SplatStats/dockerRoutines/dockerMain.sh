#!/bin/bash

pyName=$1
weapon=$2
btMode=$3
dwnlad=$4

###############################################################################
# Constants and Message
###############################################################################
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
RED='\033[0;31m'
printf "\n${RED}* Welcome to SplatStats!!!!!!!!!!!!${CLEAR}\n"
###############################################################################
# Run s3s scraper
###############################################################################
printf "\n${BLUE}* [1/2] Downloading your data with s3s...${CLEAR}\n"
cd /data
printf "n\n" | python /SplatStats/s3s_source/s3s.py -o
###############################################################################
# Run SplatStats scripts
###############################################################################
printf "\n${BLUE}* [2/2] Processing your data with SplatStats...${CLEAR}\n"
cd ~
python /SplatStats/dockerRoutines/dockerPlots.py "$pyName" "$weapon" "$btMode"