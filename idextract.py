import json

with open("results.json") as f:
    data = json.load(f)

ids = [item["identifier"] for item in data["result_set"]]

with open("ids.txt", "w") as out:
    out.write(",".join(ids))
print(f"Extracted {len(ids)} identifiers to ids.txt")