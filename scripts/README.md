# Manually install apache2 and ganglia web UI on the master node

Log in the master node and install ganglia web UI

   * ssh $masterNode
   * sudo apt-get install -y rrdtool  ganglia-webfrontend

# Set the important parameters on the cluster

   * hostnames of master node and worker nodes
   * number of cpus per nodes
   * directory for yarn-logs
   * scheduler & scheduler file path
   * yarn, flink, spark versions and download links

# Install the necessary software and tools by enable 

At the first time of installation, please enable the following 
   * IS_INIT=true

If you want to modify, or install one of them, you only need to set IS_INIT=false and enable one of them. For example, I want to download and install Hadoop
   * IS_INIT=false
   * isDownload=true
   * isExtract=true
   * installHadoop=true
# ssh-add
eval `ssh-agent -s`
