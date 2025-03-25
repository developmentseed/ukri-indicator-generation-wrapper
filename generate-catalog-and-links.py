import json
import os
import argparse


def create_stac_catalog(directory):
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if not os.path.isdir(subdir_path):
            continue

        # Locate collection.json
        collection_file = os.path.join(subdir_path, "collection.json")
        if not os.path.exists(collection_file):
            print(f"Skipping {subdir}, no collection.json found.")
            continue

        # Load collection.json
        with open(collection_file, 'r') as f:
            collection = json.load(f)

        # Create catalog.json structure
        catalog = {
            "stac_version": "1.0.0",
            "id": subdir,
            "type": "Catalog",
            "description": collection.get("description", "STAC Catalog"),
            "links": []
        }

        catalog["links"].append({
            "rel": "child",
            "href": "collection.json",
            "type": "application/json",
            "title": collection.get("title", "Collection")
        })

        # Process item files in the directory
        item_files = [f for f in os.listdir(subdir_path) if
                      f.endswith(".json") and f != "collection.json" and f != "catalog.json"]

        for item_file in item_files:
            item_path = os.path.join(subdir_path, item_file)
            with open(item_path, 'r') as f:
                item = json.load(f)

            # Add item link to collection
            collection.setdefault("links", []).append({
                "rel": "item",
                "href": item_file,
                "type": "application/json",
                "title": item.get("id", "Item")
            })

        # Write updated collection.json
        with open(collection_file, 'w') as f:
            json.dump(collection, f, indent=2)

        # Write catalog.json
        catalog_output_path = os.path.join(subdir_path, "catalog.json")
        with open(catalog_output_path, 'w') as f:
            json.dump(catalog, f, indent=2)

        print(f"STAC catalog updated in {subdir_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate STAC catalogs for multiple directories.")
    parser.add_argument("directory",
                        help="Root directory containing subdirectories with collection.json and item JSON files")

    args = parser.parse_args()

    create_stac_catalog(args.directory)
