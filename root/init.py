#!/usr/bin/env python3
# Documentation:
#   https://2.python-requests.org/en/master/
#   https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#patch_namespaced_endpoints
#   https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_namespaced_pod
#   https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#patch_namespaced_pod
#   https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py
#   https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1PodStatus.md
import sys
import os
import requests
import subprocess
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException

config.load_incluster_config()
v1 = client.CoreV1Api()
NAMESPACE = os.environ["NAMESPACE"]
STORAGE_LABELS = os.environ["STORAGE_LABELS"]
STORAGE_PORT = os.environ["STORAGE_PORT"]
ENDPOINTS_NAME = os.environ["ENDPOINTS_NAME"]
ENDPOINTS_PORT = os.environ["ENDPOINTS_PORT"]
POD_NAME = os.environ["POD_NAME"]
SONARR_NAME = os.environ["SONARR_NAME"]
SONARR_PORT = os.environ["SONARR_PORT"]
RADARR_NAME = os.environ["RADARR_NAME"]
RADARR_PORT = os.environ["RADARR_PORT"]

def getNodeWithMostStorage():
	podIP, hostIP = ""
	curMax = 0
	try:
		podList = v1.list_namespaced_pod(NAMESPACE, label_selector=STORAGE_LABELS, watch=False)
	except ApiException as e:
		print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
		sys.exit(1)
	for i in podList.items:
		try:
			r = requests.get("http://" + i.status.pod_ip + ":" + STORAGE_PORT)
		except requests.exceptions.RequestException as e:
			print("Exception when calling requests->get: %s\n" % e)
			sys.exit(1)
		if r.json() > curMax:
			podIP = i.status.pod_ip
			hostIP = i.status.host_ip
			curMax = r.json()
	if podIP == "":
		print("ScriptError: IP invalid in getNodeWithMostStorage()\n")
		sys.exit(1)
	return podIP, hostIP

def patchEndpoints(podIP):
	patch = client.V1EndpointSubset(
		addresses=["
	try:
		v1.patch_namespaced_endpoints(ENDPOINTS_NAME, NAMESPACE, 

def main():
	podIP, hostIP = getNodeWithMostStorage()
	patchService(podIP)
	
if __name__ == '__main__':
	main()
