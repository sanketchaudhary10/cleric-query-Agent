## Cleric Query Agent
The application is designed to handle user queries related to Kubernetes clusters by using OpenAI's GPT model. The project includes:

## Project Overview
- A Flask application that processes queries.
- Integration with OpenAI API for parsing and understanding queries.
- Kubernetes utilities to fetch relevant cluster data.


**Core Features**:
- Parse user queries using OpenAI's GPT model.
- Retrieve Kubernetes cluster information (e.g., pods, nodes, deployments).
- Handle specific intents like pod restarts, deployment details, and cluster status.

### Steps to Use Rufus

**1. Installation**:

## Cloning the Repository
```bash
git clone https://github.com/sanketchaudhary10/cleric-query-Agent.git
cd cleric-query-agent
```

## Installing the required libraries
```bash
pip install -r requirements.txt
```
## Running the Application
**Step 1: Start the Flask Server**
**Run the application:**
```bash
python main.py
```

**You should see:**
```bash
Running on http://127.0.0.1:8000
```

## Project Structure
```
cleric-query-agent
├─ agent.log
├─ gpt_utils.py
├─ kube_utils.py
├─ main.py
├─ models.py
├─ nlp_utils.py
├─ README.md
└─ requirements.txt

```

