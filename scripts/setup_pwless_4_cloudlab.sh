
servers="ms1026.utah.cloudlab.us ms1032.utah.cloudlab.us ms1007.utah.cloudlab.us ms1011.utah.cloudlab.us ms1019.utah.cloudlab.us ms1043.utah.cloudlab.us"
for server in $servers; do
	scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
	ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		chmod 0600 ~/.ssh/id_rsa*; 
		chmod 0600 ~/.ssh/authorized_keys; 
		rm -rf ~/.ssh/known_hosts; 	
		echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
done	
