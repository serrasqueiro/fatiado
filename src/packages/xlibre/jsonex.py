# (c)2023  Henrique Moreira

""" json useful functions
"""

# pylint: disable=missing-function-docstring

import json

def json_dump(obj):
    astr = json.dumps(obj, indent=2, sort_keys=True)
    return astr + "\n"

if __name__ == "__main__":
    print("Import me!")
