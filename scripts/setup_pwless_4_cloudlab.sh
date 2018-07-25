
servers="ms1119.utah.cloudlab.us
ms1130.utah.cloudlab.us
ms1138.utah.cloudlab.us
ms1121.utah.cloudlab.us"

for server in $servers; do
	scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
	ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		chmod 0600 ~/.ssh/id_rsa*; 
		chmod 0600 ~/.ssh/authorized_keys; 
		rm -rf ~/.ssh/known_hosts; 	
		echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
done	
