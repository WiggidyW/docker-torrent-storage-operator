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
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException

config.load_incluster_config()
v1 = client.CoreV1Api()
NAMESPACE = os.environ["NAMESPACE"]
STORAGE_LABELS = os.environ["STORAGE_LABELS"]
STORAGE_PORT = os.environ["STORAGE_PORT"]
ENDPOINTS_TARGET_LABELS = os.environ["ENDPOINTS_TARGET_LABELS"]
ENDPOINTS_NAME = os.environ["ENDPOINTS_NAME"]
NFS_TARGET_LABELS = os.environ["NFS_TARGET_LABELS"]
NFS_NAME = os.environ["NFS_NAME"]
ARR_NAME = os.environ["ARR_NAME"]
ARR_PORT = os.environ["ARR_PORT"]

# in: NAMESPACE, STORAGE_LABELS, STORAGE_PORT
# out: nodeIP
def getNodeWithMostStorage():
	podIP, nodeIP = ""
	curMax = 0
	try:
		podList = v1.list_namespaced_pod(NAMESPACE, label_selector=STORAGE_LABELS, watch=False)
	except ApiException as e:
		print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
		sys.exit(1)
	else:
		for i in podList.items:
			try:
				r = requests.get("http://" + i.status.pod_ip + ":" + STORAGE_PORT)
			except requests.exceptions.RequestException as e:
				print("Exception when calling requests->get: %s\n" % e)
				sys.exit(1)
			else:
				if r.json() > curMax:
					nodeIP = i.status.host_ip
					curMax = r.json()
	if nodeIP == "":
		print("ScriptError: IP invalid in getNodeWithMostStorage()\n")
		sys.exit(1)
	return nodeIP

# in: NAMESPACE, labels, nodeIP
# out: podIP
def getDestination(nodeIP, labels):
	podIP = ""
	try:
		podList = v1.list_namespaced_pod(NAMESPACE, label_selector=labels, watch=False)
	except ApiException as e:
		print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
		sys.exit(1)
	else:
		for i in podList.items:
			if i.status.host_ip == nodeIP:
				podIP = i.status.pod_ip
	if podIP == "";
		print("ScriptError: IP invalid in getDestination(nodeIP, labels)\n")
		sys.exit(1)
	return podIP

# in: NAMESPACE, ENDPOINTS_NAME, podIP
# out:
def patchEndpoint(podIP):
	patch = client.V1Endpoints({"addresses": {"ip": podIP}})
	try:
		ApiResponse = v1.patch_namespaced_endpoints(ENDPOINTS_NAME, NAMESPACE, patch)
		print("Endpoints patched. Status: %s\n" % str(ApiResponse.status))
	except ApiException as e:
		print("Exception when calling CoreV1Api->patch_namespaced_endpoints: %s\n" % e)
		sys.exit(1)

# in: NAMESPACE, NFS_NAME, podIP
# out:
def patchNFS(podIP):
	patchSubset = client.V1PodSpec({"env": {"SERVER": podIP}})
	patchSubset2 = client.V1PodTemplateSpec(patchSubset)
	patchSubset3 = client.V1DeploymentSpec(patchSubset2)
	patch = client.V1Deployment(patchSubset3)
	try:
		ApiResponse = v1.patch_namespaced_deployment(NFS_NAME, NAMESPACE, patch)
		print("Deployment patched. Status: %s\n" % str(ApiResponse.status))
	except ApiException as e:
		print("Exception when calling CoreV1Api->patch_namespaced_deployment: %s\n" % e)
		sys.exit(1)

# in: ENDPOINTS_TARGET_LABELS, NFS_TARGET_LABELS
def main():
	nodeIP = getNodeWithMostStorage()
	endpointIP = getEndpoint(nodeIP, ENDPOINTS_TARGET_LABELS)
	nfsIP = getDestination(nodeIP, NFS_TARGET_LABELS)
	if arr == gucci:
		patchEndpoint(endpointIP)
		patchNFS(nfsIP)

if __name__ == '__main__':
	main()
