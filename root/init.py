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
import subprocess
import requests
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException

config.load_incluster_config()
v1 = client.CoreV1Api()
# STORAGE_LABELS Must be labels unique to the storage pods
LABELS = os.environ["LABELS"]
MESSENGER_PORT = os.environ["MESSENGER_PORT"]
NAMESPACE = os.environ["NAMESPACE"]

SSH_PORT = os.environ["SSH_PORT"]
KEY = os.environ["KEY"]

def getNodeWithMostStorage():
	IP = ""
	curMax = 0
	try:
		podList = v1.list_namespaced_pod(NAMESPACE, label_selector=LABELS, watch=False)
	except ApiException as e:
		print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
		sys.exit(1)
	else:
		for i in podList.items:
			try:
				r = requests.get("http://" + i.status.pod_ip + ":" + MESSENGER_PORT)
			except requests.exceptions.RequestException as e:
				print("Exception when calling requests->get: %s\n" % e)
				sys.exit(1)
			else:
				if r.json() > curMax:
					IP = i.status.host_ip
					curMax = r.json()
	if IP == "":
		print("ScriptError: IP invalid in getNodeWithMostStorage()\n")
		sys.exit(1)
	return IP

if __name__ == '__main__':
	IP = getNodeWithMostStorage()
	os.environ["IP"] = IP
	subprocess.call("/scp.sh")
