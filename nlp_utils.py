<<<<<<< HEAD
import spacy
import re
import logging

# Loading the spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_query(query):
    query_cleaned = re.sub(r"[^\w\s\-_]", "", query.lower())
    doc = nlp(query_cleaned)

    intents = {
        "pods": ["pod", "pods", "workload", "container"],
        "namespace": ["namespace", "default"],
        "status": ["status", "state", "condition", "restarts"],
        "deployments": ["deployment", "app", "application"],
        "logs": ["log", "event", "detail"]
    }

    # Detecting intents
    identified_intents = {
        key: any(token.text in intents[key] for token in doc)
        for key in intents.keys()
    }

    # Extracting Kubernetes-like names (e.g., bot-deployment)
    deployment_pattern = re.compile(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*") 
    extracted_keywords = deployment_pattern.findall(query_cleaned)

    # Filtering out intent-related words and irrelevant keywords
    stop_words = set(intents["pods"] + intents["status"] + intents["deployments"] + intents["logs"] + ["how", "many", "has", "the", "had"])
    filtered_keywords = [kw for kw in extracted_keywords if kw not in stop_words]

    # Matching deployment names
    deployment_name = next((kw for kw in filtered_keywords if "deployment" in kw.lower()), None)

    logging.info(f"Identified Intents: {identified_intents}, Filtered Keywords: {filtered_keywords}, Deployment Name: {deployment_name}")
    return identified_intents, filtered_keywords, deployment_name

=======
import spacy
import re
import logging

# Loading the spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_query(query):
    query_cleaned = re.sub(r"[^\w\s\-_]", "", query.lower())
    doc = nlp(query_cleaned)

    intents = {
        "pods": ["pod", "pods", "workload", "container"],
        "namespace": ["namespace", "default"],
        "status": ["status", "state", "condition", "restarts"],
        "deployments": ["deployment", "app", "application"],
        "logs": ["log", "event", "detail"]
    }

    # Detecting intents
    identified_intents = {
        key: any(token.text in intents[key] for token in doc)
        for key in intents.keys()
    }

    # Extracting Kubernetes-like names (e.g., bot-deployment)
    deployment_pattern = re.compile(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*") 
    extracted_keywords = deployment_pattern.findall(query_cleaned)

    # Filtering out intent-related words and irrelevant keywords
    stop_words = set(intents["pods"] + intents["status"] + intents["deployments"] + intents["logs"] + ["how", "many", "has", "the", "had"])
    filtered_keywords = [kw for kw in extracted_keywords if kw not in stop_words]

    # Matching deployment names
    deployment_name = next((kw for kw in filtered_keywords if "deployment" in kw.lower()), None)

    logging.info(f"Identified Intents: {identified_intents}, Filtered Keywords: {filtered_keywords}, Deployment Name: {deployment_name}")
    return identified_intents, filtered_keywords, deployment_name

>>>>>>> c33188015ddd15f7c364ffa34c902c7ec91cd909
