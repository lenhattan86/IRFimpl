
JOB_NAMES="vgg16 lenet googlenet alexnet  resnet50 inception3 overfeat"
BATCH_SIZES="32 64 128 256 512 1024"
BENCH_FOLDER="../../benchmarks/scripts/tf_benchmarks"
MEM_LOG="mem_usage_simple"


mkdir $MEM_LOG
rm -rf $MEM_LOG/*
STOP_TIME=10000
NUM_BATCHES=5
for job in $JOB_NAMES;
do
    for batchSize in $BATCH_SIZES;
    do
        echo "============ $job $batchSize ============"
        rm -rf "$MEM_LOG/$job.$batchSize.$device.csv"
        ./measure_res_usage.sh "$MEM_LOG/$job.$batchSize.$device.csv" $STOP_TIME & logScript=$! 
        sleep 5
        # then start the jobs
        python $BENCH_FOLDER/linear_regression.py --batch_size=$batchSize
        kill $logScript
        echo 'wait for OS to clean the memory'
        sleep 10        
        echo =======================================
    done
done
