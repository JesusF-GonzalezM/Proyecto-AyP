import json


def write_to_file(obj, filename):
    json_string = json.dumps(obj, default=lambda o: o.__dict__, indent=4)
    with open(f"Database/{filename}.json", "w") as json_file:
        json_file.write(json_string)

