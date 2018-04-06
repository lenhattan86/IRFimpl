# /usr/bin/python2.7
# written by Tomas (www.lisenet.com) on 05/11/2012
# copyleft free software

import boto.ec2
import sys

# specify AWS keys
auth = {"aws_access_key_id": "AKIAIIV3UCOQGYWYRR5A", "aws_secret_access_key": "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"}
aws_region = "us-east-2"
#instance_ids= {"", ""}

def main():
    # read arguments from the command line and 
    # check whether at least two elements were entered
    if len(sys.argv) < 2:
        print "Usage: python aws.py {start|stop}\n"
        sys.exit(0)
    else:
	    action = sys.argv[1] 

    if action == "start":
	    startInstance()
    elif action == "stop":
    	stopInstance()
    else:
    	print "Usage: python aws.py {start|stop}\n"    
    

def startInstance():
    print "Starting the instance..."

    # change "us-east-2" region if different
    try:
        ec2 = boto.ec2.connect_to_region("us-east-2", **auth)

    except Exception, e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    # change instance ID appropriately  
    try:
         ec2.start_instances(instance_ids="i-052f1bc78d0c24a20")

    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def stopInstance():
    print "Stopping the instance..."

    try:
        ec2 = boto.ec2.connect_to_region("us-east-2", **auth)

    except Exception, e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    try:
        ec2.stop_instances(instance_ids="i-052f1bc78d0c24a20")

    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

if __name__ == '__main__':
    main()