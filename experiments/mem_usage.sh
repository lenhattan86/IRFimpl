# JOB_NAMES="vgg16 lenet"
# BATCH_SIZES="32 64"
JOB_NAMES="vgg16 lenet googlenet alexnet  resnet50 inception3 overfeat"
BATCH_SIZES="32 64 128"
BENCH_FOLDER="../../benchmarks/scripts/tf_benchmarks"
MEM_LOG="mem_usage"


mkdir $MEM_LOG
rm -rf $MEM_LOG/*
STOP_TIME=10000
for job in $JOB_NAMES;
do
    for batchSize in $BATCH_SIZES;
    do
        echo "============ $job $batchSize ============"
        # start measuring usage in 5 seconds
        device="gpu"
        rm -rf "$MEM_LOG/$job.$batchSize.$device.csv"
        ./measure_res_usage.sh "$MEM_LOG/$job.$batchSize.$device.csv" $STOP_TIME & logScript=$! 
        sleep 5
        # then start the jobs
        python $BENCH_FOLDER/tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0  --model=$job --batch_size=$batchSize --num_batches=50
        kill $logScript
        echo 'wait for OS to clean the memory'
        sleep 10

        # start measuring usage in 5 seconds
        device="cpu"
        rm -rf "$MEM_LOG/$job.$batchSize.$device.csv"
        ./measure_res_usage.sh "$MEM_LOG/$job.$batchSize.$device.csv" $STOP_TIME & logScript=$! 
        sleep 5
        # then start the jobs
        python $BENCH_FOLDER/tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0  --model=$job --batch_size=$batchSize --num_intra_threads=19 --num_batches=50
        kill $logScript        
        echo 'wait for OS to clean the memory'
        sleep 10        
        echo =======================================
    done
done
