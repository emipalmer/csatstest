#!/bin/bash

# Script to download JSON files from RCSB PDB API.
# Downloads entry data in JSON format for each PDB id.

if ! command -v curl &> /dev/null
then
    echo "'curl' could not be found. You need to install 'curl' for this script to work."
    exit 1
fi

PROGNAME=$0
BASE_URL="https://data.rcsb.org/rest/v1/core/entry"

usage() {
  cat << EOF >&2
Usage: $PROGNAME -f <file> [-o <dir>]

 -f <file>: the input file containing a comma-separated list of PDB ids
 -o  <dir>: the output dir, default: current dir
EOF
  exit 1
}

download() {
  id=$1
  outdir=$2
  url="$BASE_URL/$id"
  out=$outdir/${id}.json
  echo "Downloading $url to $out"
  curl -s -f $url -o $out 
  if [ $? -eq 0 ]; then
    echo "  ✓ Success"
  else
    echo "  ✗ Failed to download $url"
  fi
  # Add a small delay between requests to avoid overwhelming the server
  sleep 0.2
}

listfile=""
outdir="."
while getopts f:o: o
do
  case $o in
    (f) listfile=$OPTARG;;
    (o) outdir=$OPTARG;;
    (*) usage
  esac
done
shift "$((OPTIND - 1))"

if [ "$listfile" == "" ]
then
  echo "Parameter -f must be provided"
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p $outdir

contents=$(cat $listfile)

# Handle both comma-separated and newline-separated formats
if grep -q ',' <<< "$contents"; then
  # Comma-separated format
  IFS=',' read -ra tokens <<< "$contents"
else
  # Newline-separated format
  IFS=$'\n' read -ra tokens <<< "$contents"
fi

for token in "${tokens[@]}"
do
  # Trim whitespace from token
  token=$(echo "$token" | xargs)
  if [ ! -z "$token" ]
  then
    download $token $outdir
  fi
done

echo "Download complete!"
