from annoy import AnnoyIndex
import glob
from os.path import join
import numpy
import os
import json

# 初期設定

# 次元
dims = 2048

# 検索対象数
n_nearest_neighbors = 200
n_nearest_neighbors = n_nearest_neighbors + 1

t = AnnoyIndex(dims, metric='angular')
t.load('index.ann')

# インデックスマップの読み込み（Annoyのインデックス内のIDと特徴ベクトルの対応）

map_path = "file_index_map.json"
file_index_map = {}
max = 0
with open(map_path) as f:
    data = json.load(f)
    index_id_map = {}
    id_index_map = {}
    for index in data:
        index_id_map[int(index)] = data[index]
        id_index_map[data[index]] = int(index)
        max += 1

# 予測

count = 0
for id in sorted(id_index_map):

    count += 1
    print(str(count)+"/" + str(max) + "\t" + id)

    opath = "/Users/nakamura/git/json/toyo/similar_images/"+id+".json"
    if os.path.exists(opath):
        continue

    query_index = id_index_map[id]
    nearest_neighbors = t.get_nns_by_item(query_index, n_nearest_neighbors, include_distances=False) #True)

    indexes = nearest_neighbors #[0]

    # scores = nearest_neighbors[1]

    similar_images = []

    for i in range(1, len(indexes)):

        target_index = indexes[i]

        target_id = index_id_map[target_index]
        '''

        similarity = scores[i]

        rounded_similarity = int((similarity * 10000)) / 10000.0

        
        data.append({
            "id" : target_id,
            "score" : rounded_similarity
        })
        '''
        similar_images.append(target_id)

    fw = open(opath, 'w')
    json.dump(similar_images, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

        
