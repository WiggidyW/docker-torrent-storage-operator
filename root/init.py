#!/usr/bin/env python3
import time
import sys
import os
import subprocess
import requests
from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_incluster_config()
v1 = client.CoreV1Api()
# STORAGE_LABELS Must be labels unique to the storage pods
STORAGE_LABELS = os.environ["STORAGE_LABELS"]
STORAGE_MESSENGER_PORT = os.environ["STORAGE_MESSENGER_PORT"]
STORAGE_NAMESPACE = os.environ["STORAGE_NAMESPACE"]

def getNodeWithMostStorage():
	IP = ""
	curMax = 0
	try:
		podList = v1.list_namespaced_pod(STORAGE_NAMESPACE, label_selector=STORAGE_LABELS, watch=False)
	except ApiException as e:
		print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
		sys.exit(1)
	else:
		for i in podList.items:
			try:
				r = requests.get("http://" + i.status.pod_ip + ":" + STORAGE_MESSENGER_PORT)
			except requests.exceptions.RequestException as e:
				print("Exception when calling requests->get: %s\n" % e)
				sys.exit(1)
			else:
				if r.json() > curMax:
					IP = i.status.pod_ip
					curMax = r.json()
	if IP == "":
		print("ScriptError: IP invalid in getNodeWithMostStorage()\n")
		sys.exit(1)
	return IP

while True:
	IP = getNodeWithMostStorage()
	subprocess.call(["/rsync.sh", IP])
	time.sleep(14400)
