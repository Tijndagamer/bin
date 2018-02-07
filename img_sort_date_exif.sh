#!/bin/bash

# Move images to a folder based on their exif CreateDate tag.
# One folder per year.

function get_file_year {
    file=$1
    exiftool -CreateDate $file | grep -oP "\d{4}"
}

for file in "$@"
do
    echo $file
    year=$(get_file_year $file)
    mv -v $file "$year/$file"
done
