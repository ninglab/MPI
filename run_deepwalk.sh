
graph=$1
rep_size=$2
window_size=$3
out_prefix=$4

deepwalk --format edgelist --input ${graph} --max-memory-data-size 0 --number-walks 256  --representation-size $rep_size --walk-length 128 --window-size $window_size --workers 1 --output ${out_prefix}_${window_size}_${rep_size}.embeddings
