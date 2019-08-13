#!/usr/bin/env python3
import requests
import os
import subprocess
from kubernetes import client, config

# Returns a 2D list containing Flannel IPs [i] of all worker nodes as well as the available storage [j] for the nodes.
def populateList():
	# 2D list
	list = [[]]
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_pod_for_all_namespaces(watch=False)
	# Parse through all kube pods.
	for i in ret.items:
		# We are only interested in the http-available-storage pods.
		if "http-available-storage" in i.metadata.name:
			# This returns the available storage of the node that the pod is on.
			r = requests.get("http://" + i.status.pod_ip + ":8080")
			# This returns the Flannel IP of the node converted from the Flannel IP of the pod.
			s = ".".join(i.status.pod_ip.split(".")[:3]) + "0"
			# Add the Flannel IP of the node followed by the available storage of the node in KiB.
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
	# Set the "IP" environment variable to the Flannel IP of the node with the highest available storage.
	os.environ["IP"] = list[n][0]
	subprocess.call("/nginx.sh")
