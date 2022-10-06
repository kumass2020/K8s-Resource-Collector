import subprocess
import os
from os import path
import time

while True:
    try:
        output = subprocess.check_output('kubectl get namespace --all-namespaces -o=name', shell=True)
        print('got namespaces')
        break
    except subprocess.CalledProcessError:
        print('refused')
        time.sleep(0.5)
output_list = str(output).lstrip("b'").rstrip("'").split('\\n')
output_list.pop()

current_path = os.getcwd()

# print(output_list)

namespace_list = []
for i, element in enumerate(output_list):
    element = element.lstrip('namespace/')
    namespace_list.append(element)

resource_type_str = 'pvc,configmap,serviceaccount,secret,service,deployment,statefulset,hpa,job,cronjob,node,namespace,endpoints,pv,rolebindings,roles,netpol,replicasets,pdb,pod'
resource_type_list = resource_type_str.split(',')
for namespace in namespace_list:
    print('init ' + namespace + '...')
    for resource_type in resource_type_list:
        resource_list = []
        while True:
            try:
                output = subprocess.check_output('kubectl get -n ' + namespace + ' -o=name ' + resource_type, shell=True)
                print('got resources: ' + namespace + '/' + resource_type)
                break
            except subprocess.CalledProcessError:
                print('refused')
                time.sleep(0.5)
                pass

        output_list = str(output).lstrip("b'").rstrip("'").split('\\n')
        output_list.pop()

        for i, element in enumerate(output_list):
            # element.lstrip(resource_type + '/')
            resource_list.append(element)
            for resource in resource_list:
                subprocess.check_output('mkdir -p $(dirname ' + resource + ')', shell=True)
                while True:
                    try:
                        output = subprocess.check_output('kubectl get -n ' + namespace + ' -o=yaml ' + resource + ' > ' + resource + '.yaml', shell=True)
                    except subprocess.CalledProcessError:
                        print('refused')
                        time.sleep(0.5)
                        continue
                    if 'refused' in str(output):
                        print('refused')
                        pass
                    else:
                        print('got yaml: ' + resource)
                        break

subprocess.check_output('cd ..', shell=True)
subprocess.check_output('python3 /home/ccl/filled_file_collector.py', shell=True)
subprocess.check_output('cd ' + current_path, shell=True)


