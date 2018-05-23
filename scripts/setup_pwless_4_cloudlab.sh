
servers="c220g2-011303.wisc.cloudlab.us
c220g2-011322.wisc.cloudlab.us"
for server in $servers; do
	scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
	ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		chmod 0600 ~/.ssh/id_rsa*; 
		chmod 0600 ~/.ssh/authorized_keys; 
		rm -rf ~/.ssh/known_hosts; 	
		echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
done	
