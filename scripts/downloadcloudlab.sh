if [ -z "$1" ]
then
	folder="beta_motivation"
else
	folder="$1"
fi
if [ -z "$2" ]
then
	EVAL_FOLDER="random"
else
	EVAL_FOLDER="$2"
fi

if [ -z "$3" ]
then
	extraStr=""
else
	extraStr="$3"
fi

if [ -z "$4" ]
then
	user="tanle"
else
	user="$4"
fi

if [ -z "$5" ]
then
	server="ctl"
else
	server="$5"
fi
# echo $user@$server
# echo "rm -rf ~/$folder.tar.gz;
# tar -czf ~/$folder.tar.gz /dev/projects/IRFimpl/experiments/$folder"
ROOT_FOLDER="/ssd/projects/IRFevaluation/awscloudlab"
ssh $user@$server "rm -rf ~/$folder.tar.gz;
cd ~/IRFimpl/experiments/
tar --exclude='*.yaml' --exclude='*user*.log' --exclude='*.sh' -czf ~/$folder.tar.gz $folder"
mkdir $ROOT_FOLDER/$EVAL_FOLDER
scp $user@$server:~/$folder.tar.gz $ROOT_FOLDER/$EVAL_FOLDER/$folder$extraStr.tar.gz