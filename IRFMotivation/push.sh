
if [ -z "$1" ]
then
	message="quick update"
else
	message="$1"
fi

git add --all
git commit -m "$message"
git push
