if [ -z "$1" ]
then
    filename="job_usage.csv"
else
    filename=$1
fi

if [ -z "$2" ]
then
    stopTime=10
else
    stopTime=$2
fi

startTime=1
for i in $(seq $startTime $stopTime);
do    
    MEMORY=$(free -m | awk 'NR==2{printf "%f", $3 }')
    # DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    # CPU=$(top -bn1 | grep load | awk '{printf "%f\n", $(NF-2)}')
    # echo "$MEMORY,$DISK,$CPU" >> resource_usage.csv
    echo "$i,$MEMORY" >> $filename
    sleep 1
done


    