import json
import shutil

with open("output/plot_data.json") as f:
    arr = json.load(f)["centroids"]
    for obj in arr:
        img = obj["img"]
        org_path = "output/thumbs/64px/"+img
        dest_path = "../docs/"+org_path
        shutil.copyfile(org_path,dest_path)

