import requests

url = "http://127.0.0.1:8000/query"
headers = {"Content-Type": "application/json"}

queries = [
    "How many pods are in the default namespace?",
    "What is the status of all pods?",
    "How many nodes are in the cluster?",
    "How many restarts has the pod bot-deployment experienced?",
    "Which pod is spawned by website-deployment?",
    "What is the status of the pod named 'orange'?"
]


for query in queries:
    data = {"query": query}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Query: {query}")
            print("Response:", response.json())
        else:
            print(f"Query: {query}")
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to send query: {query}")
        print(f"Error: {e}")
