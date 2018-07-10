import os
import socket
import sys
import time
import yaml
from kubernetes import client, config

local_ip = sys.argv[1]
start_time = time.time()
config.load_kube_config()
print("loaded config %s" % str(time.time() - start_time))

with open(os.path.join(os.path.dirname(__file__), "bench.yaml")) as f:
   dep = yaml.load(f)
   dep['spec']['template']['spec']['containers'][0]['args'][0] = local_ip
   k8s_beta = client.ExtensionsV1beta1Api()
   resp = k8s_beta.create_namespaced_deployment(
       body=dep, namespace="default")
   print("deployment created %s" % str(time.time() - start_time))

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 15000))
resp = s.listen(2)
s.accept()
print("call received %s" % str(time.time() - start_time))
s.shutdown(socket.SHUT_RDWR)
s.close()
