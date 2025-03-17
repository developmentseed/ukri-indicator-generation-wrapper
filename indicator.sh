#!/bin/bash

python indicator.py generate-indicators "$1"

store=$(echo "$1" | jq -r '.store')
indicator=$(echo "$1" | jq -r '.indicator' | sed 's/_indicator$//')

python indicator.py cubify-indicator $store "$store/cubified" $indicator

python indicator.py create-collection "$store/cubified/*.zarr" "$store/collection.json"

for dir in "$store/cubified"/*; do
    if [ -d "$dir" ]; then
        echo "Processing directory: $dir"
        output_filename=$(basename "$dir" .zarr).json
        python indicator.py create-item $dir "$store/$output_filename"
    fi
done
