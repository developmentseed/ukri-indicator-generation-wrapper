#!/bin/bash

VALUE="$2"
SRC_BUCKET="ukri-eodh-hazard-tiles-test"
SRC_PATH="indicator-generation/$VALUE"
DEST_DIR="output"

# Create output directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Sync data from S3
aws s3 cp "s3://$SRC_BUCKET/$SRC_PATH/" "$DEST_DIR/" --recursive --exclude "*" \
    --include "cubified/*" \
    --include "days_tas_above_*.json" \
    --include "degree_days_*.json" \
    --include "collection.json"

echo "Files have been organized into '$DEST_DIR'."
