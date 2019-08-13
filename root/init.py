#!/usr/bin/env python3

import requests
import os
import subprocess
from kubernetes import client, config

# Returns a 2D list containing flannel IPs [i] of all worker nodes as well as the available storage [j] for the nodes.
def populateList():
	list = [[]]
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_pod_for_all_namespaces(watch=False)
	for i in ret.items:
		if "http-available-storage" in i.metadata.name:
			r = requests.get("http://" + i.status.pod_ip + ":8080")
			s = ".".join(i.status.pod_ip.split(".")[:3]) + "0"
			list.append((s,r.json()))
	return list

# Sets Nginx to proxy to the flannel IP of the kube node with the highest available storage.
def setIP():
	list = populateList()
	highestCapacity = 0
	n = 0
	for i in list:
		if list[i][1] > highestCapacity:
			highestCapacity = list[i][1]
			n = i
	os.environ["IP"] = list[n][0]
	subprocess.call("/nginx.sh")
