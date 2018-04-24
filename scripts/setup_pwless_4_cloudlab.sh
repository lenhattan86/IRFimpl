
servers="c220g2-011113.wisc.cloudlab.us
c220g2-011308.wisc.cloudlab.us		
c220g2-011316.wisc.cloudlab.us		
c220g2-011330.wisc.cloudlab.us		
c220g2-011310.wisc.cloudlab.us		
c220g2-011303.wisc.cloudlab.us		
c220g2-011317.wisc.cloudlab.us		
c220g2-011322.wisc.cloudlab.us		
c220g2-011319.wisc.cloudlab.us		
c220g2-011105.wisc.cloudlab.us		
c220g2-011110.wisc.cloudlab.us		
c220g2-011314.wisc.cloudlab.us		
c220g2-011018.wisc.cloudlab.us
c220g2-011129.wisc.cloudlab.us		
c220g2-011324.wisc.cloudlab.us		
c220g2-011332.wisc.cloudlab.us		
c220g2-031132.wisc.cloudlab.us		
c220g2-011122.wisc.cloudlab.us		
c220g2-011021.wisc.cloudlab.us"
for server in $servers; do
	scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
	ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		chmod 0600 ~/.ssh/id_rsa*; 
		chmod 0600 ~/.ssh/authorized_keys; 
		rm -rf ~/.ssh/known_hosts; 	
		echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
done	
