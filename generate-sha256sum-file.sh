#!/usr/bin/env bash

for file in "$@"
do
    echo "$file"
    sha256sum "$file" > "$file.sha256sum"
done
