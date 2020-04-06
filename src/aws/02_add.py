import elasticsearch
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth
import json
import glob
import os

INDEX = "toyo_images"

host = 'search-nakamura196-rgvfh3jsqpal3gntof6o7f3ch4.us-east-1.es.amazonaws.com'

profile_name = "default"
region = "us-east-1"

session = boto3.Session(profile_name=profile_name)
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, 'es', session_token=credentials.token)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

all_body = []

files = glob.glob("/Users/nakamura/git/json/toyo/similar_images/*.json")
files = sorted(files)

for i in range(len(files)):
    file = files[i]

    # メイン
    if i % 1000 == 0:
        print(str(i+1)+"/"+str(len(files))+"\t"+file)

    id = file.split("/")[-1].replace(".json", "")

    try:
        with open(file) as f:
            df = json.load(f)
            body = {}
            body["_type"] = "_doc"
            body["_index"] = INDEX
            body["_id"] = id
            body["similar_images"] = df
            all_body.append(body)
    except Exception as e:
        os.remove(file)
        print(e)

def create_documents():
  for body in all_body:
      yield body
  
res = elasticsearch.helpers.streaming_bulk(client=es, actions=all_body, chunk_size=100, max_retries=5,
                                               initial_backoff=2, max_backoff=600, request_timeout=3600)
for ok, response in res:
    print(ok, response)



