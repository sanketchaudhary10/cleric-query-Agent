<<<<<<< HEAD
from kubernetes import client, config
import os
import logging

def initialize_k8s():
    kubeconfig_path = os.path.join(os.environ["USERPROFILE"], ".kube", "config")
    if not os.path.exists(kubeconfig_path):
        raise FileNotFoundError(f"Kubeconfig file not found at {kubeconfig_path}")
    config.load_kube_config(config_file=kubeconfig_path)

def get_pods_in_namespace(namespace="default"):
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace)
    return [
        {
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "restarts": sum(container.restart_count for container in pod.status.container_statuses or []),
        }
        for pod in pod_list.items
    ]

def get_pods_with_nodes(namespace="default"):
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace)
    return [
        {
            "name": pod.metadata.name,
            "node": pod.spec.node_name,
            "status": pod.status.phase,
        }
        for pod in pod_list.items
    ]

# def get_pod_restarts(pod_name, namespace="default"):
#     logging.info(f"Fetching restart count for pod: {pod_name} in namespace: {namespace}")
#     pods = get_pods_in_namespace(namespace)
#     for pod in pods:
#         if pod["name"] == pod_name:
#             logging.info(f"'{pod_name}' restarts: {pod['restarts']}")
#             return pod["restarts"]
#     logging.warning(f"Pod '{pod_name}' not found in namespace '{namespace}'.")
#     return None

def get_pod_restarts(pod_name, namespace="default"):
    logging.info(f"Fetching restart count for pod: {pod_name} in namespace: {namespace}")
    pods = get_pods_in_namespace(namespace)
    for pod in pods:
        if pod_name in pod["name"]:  # Substring matching
            logging.info(f"Found pod '{pod['name']}' for query pod '{pod_name}'. Restarts: {pod['restarts']}")
            return pod["restarts"]
    logging.warning(f"Pod '{pod_name}' not found in namespace '{namespace}'.")
    return None

def get_pods_by_deployment(deployment_name, namespace="default"):
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    try:
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        selector = deployment.spec.selector.match_labels
        label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])
        logging.info(f"Label selector for deployment '{deployment_name}': {label_selector}")

        pod_list = v1.list_namespaced_pod(namespace, label_selector=label_selector)
        pods = [
            {"name": pod.metadata.name, "status": pod.status.phase}
            for pod in pod_list.items
        ]
        logging.info(f"Pods found for deployment '{deployment_name}': {[pod['name'] for pod in pods]}")
        return pods
    except client.exceptions.ApiException as e:
        if e.status == 404:
            logging.warning(f"Deployment '{deployment_name}' not found in namespace '{namespace}'.")
            return []  
        raise RuntimeError(f"Error fetching pods for deployment '{deployment_name}': {e}")

def trim_identifier(name):
    return "-".join(name.split("-")[:-2]) if "-" in name else name

=======
from kubernetes import client, config
import os
import logging

def initialize_k8s():
    kubeconfig_path = os.path.join(os.environ["USERPROFILE"], ".kube", "config")
    if not os.path.exists(kubeconfig_path):
        raise FileNotFoundError(f"Kubeconfig file not found at {kubeconfig_path}")
    config.load_kube_config(config_file=kubeconfig_path)

def get_pods_in_namespace(namespace="default"):
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace)
    return [
        {
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "restarts": sum(container.restart_count for container in pod.status.container_statuses or []),
        }
        for pod in pod_list.items
    ]

def get_pods_with_nodes(namespace="default"):
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace)
    return [
        {
            "name": pod.metadata.name,
            "node": pod.spec.node_name,
            "status": pod.status.phase,
        }
        for pod in pod_list.items
    ]

# def get_pod_restarts(pod_name, namespace="default"):
#     logging.info(f"Fetching restart count for pod: {pod_name} in namespace: {namespace}")
#     pods = get_pods_in_namespace(namespace)
#     for pod in pods:
#         if pod["name"] == pod_name:
#             logging.info(f"'{pod_name}' restarts: {pod['restarts']}")
#             return pod["restarts"]
#     logging.warning(f"Pod '{pod_name}' not found in namespace '{namespace}'.")
#     return None

def get_pod_restarts(pod_name, namespace="default"):
    logging.info(f"Fetching restart count for pod: {pod_name} in namespace: {namespace}")
    pods = get_pods_in_namespace(namespace)
    for pod in pods:
        if pod_name in pod["name"]:  # Substring matching
            logging.info(f"Found pod '{pod['name']}' for query pod '{pod_name}'. Restarts: {pod['restarts']}")
            return pod["restarts"]
    logging.warning(f"Pod '{pod_name}' not found in namespace '{namespace}'.")
    return None

def get_pods_by_deployment(deployment_name, namespace="default"):
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    try:
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        selector = deployment.spec.selector.match_labels
        label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])
        logging.info(f"Label selector for deployment '{deployment_name}': {label_selector}")

        pod_list = v1.list_namespaced_pod(namespace, label_selector=label_selector)
        pods = [
            {"name": pod.metadata.name, "status": pod.status.phase}
            for pod in pod_list.items
        ]
        logging.info(f"Pods found for deployment '{deployment_name}': {[pod['name'] for pod in pods]}")
        return pods
    except client.exceptions.ApiException as e:
        if e.status == 404:
            logging.warning(f"Deployment '{deployment_name}' not found in namespace '{namespace}'.")
            return []  
        raise RuntimeError(f"Error fetching pods for deployment '{deployment_name}': {e}")

def trim_identifier(name):
    return "-".join(name.split("-")[:-2]) if "-" in name else name

>>>>>>> c33188015ddd15f7c364ffa34c902c7ec91cd909
