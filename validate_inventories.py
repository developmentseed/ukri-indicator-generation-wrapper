import os
import json


def validate_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    for file in json_files:
        file_path = os.path.join(directory, file)

        with open(file_path, "r") as f:
            data = json.load(f)

            central_years = data.get("central_year_list", [])
            scenarios = data.get("scenario_list", [])
            store_relative_path = data.get("store", "").replace("indicator/", "").lstrip("./")
            store_path = os.path.join("generated-indicators", store_relative_path, "inventory.json")

            if not os.path.exists(store_path):
                print(f"Missing inventory file: {store_path}")
                continue

            with open(store_path, "r") as inv_f:
                inventory_data = json.load(inv_f)
                resources = inventory_data.get("resources", [])

                if not resources:
                    print(f"No resources found in {store_path}")
                    continue

                inventory_scenarios = resources[0].get("scenarios", [])

                for scenario in scenarios:
                    matching_scenario = next((s for s in inventory_scenarios if s.get("id") == scenario), None)

                    if not matching_scenario:
                        print(f"Missing scenario {scenario} in {store_path}")
                        continue

                    scenario_years = matching_scenario.get("years", [])
                    missing_years = [year for year in central_years if year not in scenario_years]

                    if missing_years:
                        print(f"Scenario {scenario} in {store_path} is missing years: {missing_years}")


if __name__ == "__main__":
    directory = "./inputs"
    validate_json_files(directory)
