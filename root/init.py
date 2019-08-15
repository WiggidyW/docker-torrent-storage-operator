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
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import config

config.load_incluster_config()
v1 = client.CoreV1Api()
NAMESPACE = os.environ["NAMESPACE"]
STORAGE_PORT = os.environ["STORAGE_PORT"]
DESTINATION_PORT = os.environ["DESTINATION_PORT"]
STORAGE_LABELS = os.environ["STORAGE_LABELS"]
DESTINATION_LABELS = os.environ["DESINATION_LABELS"]

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
		if r.json() > i:
			podIP = i.status.pod_ip
			hostIP = i.status.host_ip
			n = r.json()
	if podIP == "":
		print("ScriptError: IP invalid in getNodeWithMostStorage()\n")
		sys.exit(1)
	return podIP, hostIP

def 

def main():
	podIP, hostIP = getNodeWithMostStorage()
	
if __name__ == '__main__':
	main()
