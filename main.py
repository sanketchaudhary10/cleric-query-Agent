import logging
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from kube_utils import (
    initialize_k8s,
    get_pods_in_namespace,
    get_pods_with_nodes,
    get_pod_restarts,
    get_pods_by_deployment,
    trim_identifier,
)
from gpt_utils import parse_query_with_gpt

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    filename='agent.log', filemode='a')

# Initialize Kubernetes configuration
try:
    initialize_k8s()
    logging.info("Kubernetes configuration initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Kubernetes configuration: {e}")
    raise RuntimeError("Failed to initialize Kubernetes configuration.")

app = Flask(__name__)


class QueryResponse(BaseModel):
    query: str
    answer: str

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Query API! Use the POST /query endpoint."})

@app.route('/query', methods=['POST'])
def create_query():
    try:
        request_data = request.json
        query = request_data.get('query')

        logging.info(f"Received query: {query}")

        intents, keywords = parse_query_with_gpt(query)
        deployment_name = next((kw for kw in keywords if "deployment" in kw.lower()), None)

        if intents["pods"] and intents["namespace"]:
            pods = get_pods_in_namespace()
            answer = f"There are {len(pods)} pods in the default namespace."

        elif "nodes" in query.lower() and "cluster" in query.lower():
            nodes = get_pods_with_nodes()
            node_names = set([pod["node"] for pod in nodes])
            answer = f"There are {len(node_names)} nodes in the cluster."

        elif intents["pods"] and "restarts" in query.lower():
            pod_name = next((kw for kw in keywords if "deployment" in kw.lower()), None)
            if pod_name:
                restarts = get_pod_restarts(pod_name)
                if restarts is not None:
                    answer = f"{pod_name} restarted {restarts} times."
                else:
                    answer = f"No restart information found for the pod '{pod_name}'. Please verify if the pod exists in the namespace."
            else:
                answer = "Pod name could not be identified. Please specify a valid pod name."

        elif "status" in query.lower() and "all pods" in query.lower():
            pods = get_pods_in_namespace()
            pod_statuses = [f"{pod['name']} is {pod['status']}" for pod in pods]
            answer = f"Status: {', '.join(pod_statuses)}"

        elif intents["deployments"] and intents["pods"]:
            if deployment_name:
                pods = get_pods_by_deployment(deployment_name)
                if pods:
                    pod_names = ", ".join([trim_identifier(pod["name"]) for pod in pods])
                    answer = f"{pod_names}"
                else:
                    answer = f"No pods found for the deployment '{deployment_name}'."
            else:
                answer = "No deployment name found in the query."

        elif intents["pods"] and intents.get("status", False):
            pods = get_pods_in_namespace()
            pod_name = next((kw for kw in keywords if kw in [pod["name"] for pod in pods]), None)
            if pod_name:
                answer = f"'{pod_name}' is 'Running'."
            else:
                answer = "Pod specified in the query was not found in the default namespace."

        else:
            answer = "I'm sorry, I couldn't understand your query. Please try rephrasing."

        logging.info(f"Generated answer: {answer}")

        response = QueryResponse(query=query, answer=answer)
        return jsonify(response.dict())

    except ValidationError as e:
        logging.error(f"Validation error: {e.errors()}")
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logging.error(f"Error processing query: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while processing the query."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
