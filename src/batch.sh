cd /Users/nakamura/git/d_jps/cj/src/sim
python process_images.py
# aws s3 sync ../europeana/data/images s3://cultural-jp
# aws s3 cp ../data s3://cultural-jp/json/ --recursive
python build.py
python predicate.py
python sim.py

# find arc_nishikie/data/images/ -name "*.jpg" -print0 | xargs -0 -I {} cp {} images/
