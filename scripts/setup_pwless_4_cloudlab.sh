
servers="hp196.utah.cloudlab.us
hp176.utah.cloudlab.us
hp175.utah.cloudlab.us
hp173.utah.cloudlab.us
hp161.utah.cloudlab.us"

for server in $servers; do
	scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
	ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		chmod 0600 ~/.ssh/id_rsa*; 
		chmod 0600 ~/.ssh/authorized_keys; 
		rm -rf ~/.ssh/known_hosts; 	
		echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
done	
