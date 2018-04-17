if [ -z "$1" ]
then
	folder="beta_motivation"
else
	folder="$1"
fi
if [ -z "$2" ]
then
	EVAL_FOLDER="."
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
	user="cc"
else
	user="$4"
fi

if [ -z "$5" ]
then
	server="chameleon"
else
	server="$5"
fi
# echo $user@$server
# echo "rm -rf ~/$folder.tar.gz;
# tar -czf ~/$folder.tar.gz /dev/projects/IRFimpl/experiments/$folder"
ssh $user@$server "rm -rf ~/$folder.tar.gz;
cd /dev/projects/IRFimpl/experiments/
tar -czf ~/$folder.tar.gz $folder"
mkdir $EVAL_FOLDER
scp $user@$server:~/$folder.tar.gz $EVAL_FOLDER/$folder$extraStr.tar.gz
