#!/bin/bash

#
# adf_fix.sh
#
# Some scanners with ADF (Automatic Document Feeder) only scan one side of the
# page. In order to easily scan a double sided document, this script combines
# two scanned pdfs where it assumes that the first one is with the first page
# up, and the second scan is made by flipping the whole document (not individual
# pages).
# 
# The pages are then in the following order (assuming a 10-side 5-page document):
# Scan 1: 1, 3, 5, 7, 9
# Scan 2: 10, 8, 6, 4, 2
#
# The script creates an output pdf with all the pages in the correct order.
#
# Dependencies: pdfunite (in the poppler-utils package on Debian/Ubuntu).
#
# Copyright 2020 Martijn
# martijn@mrtijn.nl
#
# Available under the terms of the MIT license.
#

set -e
set -u
set -f
set -o pipefail

function fail {
    echo "$1"
    exit 1
}

# Expect exactly 3 arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 [scan1.pdf] [scan2.pdf] [output.pdf]"
    exit
fi

CURRENT_DIR=$(pwd)
TEMP_DIR=$(mktemp -d)

cp "$1" "$TEMP_DIR"
cp "$2" "$TEMP_DIR"

cd "$TEMP_DIR" || fail "Could not move to temporary directory $TEMP_DIR"

# Assume that both pdf's have the same length, since a page always has 2 sides.
PAGE_COUNT=$(pdfinfo "$1" | grep 'Pages:' | grep --only-matching --perl-regexp '[0-9]+')

pdfseparate "$1" "SCAN1_%d.pdf"
pdfseparate "$2" "SCAN2_%d.pdf"

rm "$1"
rm "$2"

# Initialize command string
UNITE_COMMAND="pdfunite "

ITERATE_COUNT=1
while [ $ITERATE_COUNT -le "$PAGE_COUNT" ]
do
    let INVERTED_PAGE_COUNT=$PAGE_COUNT-$ITERATE_COUNT+1
    UNITE_COMMAND="${UNITE_COMMAND} SCAN1_$ITERATE_COUNT.pdf SCAN2_$INVERTED_PAGE_COUNT.pdf"

    ITERATE_COUNT=$(( ITERATE_COUNT + 1 ))
done

# Append output name to pdfunite command
UNITE_COMMAND="${UNITE_COMMAND} $3"

$UNITE_COMMAND

# Go back to where the command was executed
cd "$CURRENT_DIR" || fail "Could not move back to $CURRENT_DIR"

# Copy output file to where we were
cp "$TEMP_DIR"/"$3" ./

# Delete temporary directory
rm -rf "$TEMP_DIR"
