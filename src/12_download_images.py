import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import csv
import os
import time
import sys
import argparse

import requests
import shutil

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

# list_path = '/Users/nakamura/git/d_jps/cj/src/europeana/data/list.json'
list_path = '/Users/nakamura/git/d_toyo/toyo_iiif/src/aws/data/list.json'

with open(list_path) as f:
    df = json.load(f)

for i in range(len(df)):
    obj = df[i]

    url = obj["image"]

    name = obj["_id"] #.split("/")[-1].split("#")[0]
    print(str(i+1)+"/"+str(len(df))+"\t"+name)

    opath = "../images/"+name+".jpg"

    if os.path.exists(opath):
        continue

    download_img(url, opath)
