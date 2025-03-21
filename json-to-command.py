import json
import sys

def main(input_path):
    with open(input_path, "r") as f:
        jase = json.load(f)
    print('"' + json.dumps(jase).replace('"', '\\"') + '"')

if __name__ == '__main__':
    main(sys.argv[1])
