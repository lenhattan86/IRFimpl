if [ -z "$1" ]
then
	folder="beta_motivation"
else
	folder="$1"
fi

if [ -z "$2" ]
then
	extraStr=""
else
	extraStr="$2"
fi

if [ -z "$3" ]
then
	user="cc"
else
	server="$3"
fi

if [ -z "$4" ]
then
	server="chameleon"
else
	server="$4"
fi
# echo $user@$server
# echo "rm -rf ~/$folder.tar.gz;
# tar -czf ~/$folder.tar.gz /dev/projects/IRFimpl/experiments/$folder"
ssh $user@$server "rm -rf ~/$folder.tar.gz;
cd /dev/projects/IRFimpl/experiments/
tar -czf ~/$folder.tar.gz $folder"
scp $user@$server:~/$folder.tar.gz $folder/$folder$extraStr.tar.gz