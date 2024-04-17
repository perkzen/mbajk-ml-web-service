#!/bin/bash


# Default values
rev="HEAD"
prefix="current_"

# Parse command-line arguments
while getopts "r:p:" opt; do
  case ${opt} in
    r )
      rev="${OPTARG}"
      ;;
    p )
      prefix="${OPTARG}"
      ;;
    \? )
      echo "Usage: $0 [-r <revision>] [-p <prefix>]"
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))


# Get all the files matching the pattern
files=(data/processed/mbajk_station_*.csv)

# Loop through the files and download them one by one
for file in "${files[@]}"; do
    name=$(basename "$file")
    echo "Downloading $prefix$name from revision $rev"
    dvc get . "$file" --rev "$rev" --out "$prefix$name"
done