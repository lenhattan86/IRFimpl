#!/bin/bash
# usage:
# ./auto_setup_cluster.sh [hostname] [method] [parameters]
## constants
IRF="IRF"
DEFAULT="DEFAULT"

METHOD=$IRF

if [ -z "$2" ]
then
	METHOD=$IRF
else
	METHOD="$2"
fi

if [ -z "$3" ]
then
	parameters=0
else
	parameters=$3
fi

## author: Tan N. Le ~ CS department Stony Brook University

### DO this command first at master node #####

# $sudo apt-get install -y rrdtool  ganglia-webfrontend

######################### enviromental variables ##############

set|grep AUTOSSH
AUTOSSH_GATETIME=0
AUTOSSH_PORT=20000

######################### System Variables #####################

isCloudLab=true
isAmazonEC=false
isLocalhost=false
IS_INIT=false
isTestNetwork=false
isOfficial=true
TEST=false
SSH_CMD="autossh"
#SSH_CMD="ssh -v "
yarnFramework="yarn"
enableSim="true"
enablePreemption="false"
enableContainerLog="false"

if $isOfficial
then
	scaleDown=1.0 # DEFAULT 1.0
else
	scaleDown=4.0 # use 4.0 to increase the number of tasks -> 4 times.
fi

if $isLocalhost
then
	isCloudLab=false
	isAmazonEC=false
	IS_INIT=false
	scaleDown=1.0
fi
username="tanle"

java_home='/usr/lib/jvm/java-8-oracle'

## tensorflow 

tensorflow_ver="1.1"

PARALLEL=2

if $isLocalhost
then
	hostname="localhost"; 
else

	if [ -z "$1" ]
	then
		hostname="ctl.tensor.yarnrm-pg0.utah.clemson.us"; cp ~/.ssh/config.tensor ~/.ssh/config; 
	else
		hostname="ctl.$1.yarnrm-pg0.utah.clemson.us"; cp ~/.ssh/config.tensor.$1 ~/.ssh/config;
	fi
fi

echo "[INFO] =====set up $hostname====="

REBOOT=false

isUploadKey=false
isGenerateKey=false	
isPasswordlessSSH=false
isAddToGroup=false

isInstallBasePackages=false
isInstallGanglia=false
startGanglia=false
if $isInstallGanglia
then
	startGanglia=true
fi


isInitPath=false
if $isDownload
then
	isInitPath=true
fi

if $IS_INIT
then
	isDownload=false
	isExtract=true

	isUploadKey=true
	isGenerateKey=false
	isPasswordlessSSH=true

	isInstallBasePackages=true

	isInstallGanglia=true
	startGanglia=false

fi

if $isLocalhost
then
	echo "[INFO] Setup Yarn on localhost"
	masterNode="localhost"
	serverList="localhost"
	slaveNodes="localhost"
	isUploadKey=false
#	isUploadKey=true
#	isGenerateKey=true
	isInstallBasePackages=false
	isInstallGanglia=false

elif $isCloudLab
then
	echo "[INFO]  at CLOUDLAB "
	masterNode="ctl"
	if $isOfficial
	then
		numOfworkers=1
		serverList="$masterNode cp-1"		
		slaveNodes="cp-1"
	fi
elif $isAmazonEC
then
	echo "[INFO] Amazon EC"
fi

if $REBOOT
then
echo ############### REBOOT all servers #############################	
	while true; do
	    read -p "Do you wish to reboot the whole cluster?" yn
	    case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	    esac
	done

	for server in $serverList; do		
		echo reboot server $server
		$SSH_CMD $username@$server "ssh $server 'sudo reboot'" &
	done
	wait
	echo "[INFO] Waiting for 15 mins for the cluster to be ready."
	sleep 900
fi

echo ####################### TEST CLUSTER NETWORK ##########################
if $isTestNetwork
then
	for server in $serverList; do
	$SSH_CMD $username@$server " echo Hello $server "
	done
	wait
fi


if $isUploadKey
then		
echo ################################# passwordless SSH ####################################
	if $isGenerateKey 
	then
            while true; do
            	read -p "Do you wish to generate new public keys ?" yn
            case $yn in
                [Yy]* ) 
			sudo rm -rf $HOME/.ssh/id_rsa*
			sudo rm -rf $HOME/.ssh/authorized_keys*
			yes Y | ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa	
			cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
			sudo chmod 0600 $HOME/.ssh/id_rsa*
			sudo chmod 0600 ~/.ssh/authorized_keys
			echo 'StrictHostKeyChecking no' >> ~/.ssh/config
			if $isLocalhost
			then
				ssh-add
			fi
			break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
	    done 	
		
	fi
	uploadKeys () { 
		echo upload keys to $1
		$SSH_CMD $username@$1 'sudo rm -rf $HOME/.ssh/id_rsa*'
		scp ~/.ssh/id_rsa* $username@$1:~/.ssh/
		$SSH_CMD $username@$1 "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
		 chmod 0600 ~/.ssh/id_rsa*; 
		 chmod 0600 ~/.ssh/authorized_keys; 
		 rm -rf ~/.ssh/known_hosts; 	
		 echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
	}
	rm -rf ~/.ssh/known_hosts

	echo "[INFO] uploading keys"
	for server in $serverList; do
		uploadKeys $server &
	done	
	wait
fi

if $isInstallBasePackages
then
	echo "################################# install JAVA ######################################"
	installPackages () {
		$SSH_CMD $username@$1 "sudo apt-get -y install $SSH_CMD
			sudo apt-get purge -y openjdk*
			sudo apt-get purge -y oracle-java*
			sudo apt-get install -y software-properties-common			
			yes='' | sudo add-apt-repository ppa:webupd8team/java
			sudo apt-get update
			sudo echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections	
			sudo apt-get install -y oracle-java8-installer"
		$SSH_CMD $username@$1 "sudo apt-get install -y cgroup-tools; sudo apt-get install -y scala; sudo apt-get install -y vim"	
	}
	counter=0;
	for server in $serverList; do
		counter=$((counter+1))
		installPackages $server &		
		if [[ "$counter" -gt $PARALLEL ]]; then
	       		counter=0;
			wait
	       	fi		
	done
	wait
	echo ################################ install screen #####################################
	$SSH_CMD $username@$masterNode "sudo apt-get install -y screen"
	
fi


if $isInstallGanglia
then
echo ################################# install Ganglia ###################################
	echo "[INFO] Configure Ganglia master node $masterNode"
	$SSH_CMD $username@$masterNode 'yes Y | sudo apt-get purge ganglia-monitor gmetad'
	### PLZ manually install Ganglia as we need to respond to some pop-ups
	# we may restart the Apache2 twice
	#$SSH_CMD $username@$masterNode 'sudo apt-get install -y rrdtool  ganglia-webfrontend'
	$SSH_CMD $username@$masterNode 'sudo apt-get install -y ganglia-monitor gmetad'
	
	# 
	$SSH_CMD $username@$masterNode "sudo cp /etc/ganglia-webfrontend/apache.conf /etc/apache2/sites-enabled/ganglia.conf ;
	sudo sed -i -e 's/data_source \"my cluster\" localhost/data_source \"sbu flink\" 1 localhost/g' /etc/ganglia/gmetad.conf;
	sudo sed -i -e 's/name = \"unspecified\"/name = \"sbu flink\"/g' /etc/ganglia/gmond.conf ;
	sudo sed -i -e 's/mcast_join = 239.2.11.71/#mcast_join = 239.2.11.71/g' /etc/ganglia/gmond.conf;
	sudo sed -i -e 's/bind = 239.2.11.71/#bind = 239.2.11.71/g' /etc/ganglia/gmond.conf"
	$SSH_CMD $username@$masterNode "sudo sed -i -e 's/udp_send_channel {/udp_send_channel { host=$masterNode/g' /etc/ganglia/gmond.conf"
	
	installGangliaFunc(){
		$SSH_CMD $username@$1 "yes Y | sudo apt-get purge ganglia-monitor;
		sudo apt-get install -y ganglia-monitor;
		sudo sed -i -e 's/name = \"unspecified\"/name = \"sbu flink\"/g' /etc/ganglia/gmond.conf;
		sudo sed -i -e 's/mcast_join = 239.2.11.71/#mcast_join = 239.2.11.71/g' /etc/ganglia/gmond.conf;
		sudo sed -i -e 's/udp_send_channel {/udp_send_channel { host=$masterNode/g' /etc/ganglia/gmond.conf"
	}

	for server in $slaveNodes; do
		installGangliaFunc $server &
	done	
	wait

fi

if $startGanglia
then
	echo restart Ganglia
	# restart all related services
	$SSH_CMD $username@$masterNode 'sudo service ganglia-monitor restart & sudo service gmetad restart & sudo service apache2 restart'
	for server in $slaveNodes; do
		$SSH_CMD $username@$server 'sudo service ganglia-monitor restart' &
	done
	wait	
fi

########################################### TENSOR-FLOW ##########################################


############################################# END #################################################

echo ""
echo "[INFO] $hostname "
echo "[INFO] Finished at: $(date) "
