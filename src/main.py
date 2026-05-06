import docker
import ollama
import time
import logging
from datetime import datetime

client = docker.from_env()


def get_containers():
    containers = client.containers.list()
    for c in containers:
        print(f"Name: {c.name}, Status: {c.status}, ID: {c.short_id}")

def detect_issues():
    containers = client.containers.list(all=True)
    issues = []
    for c in containers:
        if c.status in ["exited", "dead"]:
            issues.append({
                "name": c.name,
                "status": c.status,
                "id": c.short_id
            })
    return issues

def get_logs(container_name):
    try:
        container = client.containers.list(all=True)
        for c in container:
            if c.name == container_name:
                logs =  c.logs(tail=50).decode('utf-8')
                return logs if logs else "No logs available."
    except Exception as e:
        return f"Error retrieving logs: {str(e)}"

def analyze_logs(logs, container_name):
    print(f"Analyzing logs for : {container_name}...")

    response = ollama.chat(
        model = "llama3.2:latest",
        messages = [{
            "role": "system",
            "content": "You are a DevOps assistant. Analyze Docker container failures concisely. Give: 1) Cause 2) Fix."
        }, {
            "role": "user",
            "content": f"Container '{container_name}' has stopped unexpectedly (status: exited).\n\nLast 50 lines of logs:\n{logs}\n\n1) What caused this container to stop?\n2) What is the exact fix?"
        }]
    )
    return response ["message"]["content"]

def fix_container(container_name):
    try:
        container = client.containers.list(all=True)
        for c in container:
            if c.name == container_name:
                c.restart()
                return f"Container '{container_name}' restarted successfully."
    except Exception as e:
        return f"Error restarting container: {str(e)}"
    

print("Analyzing Docker containers...")
get_containers()

def run_agent():
    issue = detect_issues()
    if not issue:
        print("No issue detected. All container are running smoothly.")

    for i in issue:
        print(f"\n Issue detected in container '{i['name']}' (status: {i['status']}), ID: {i['id']}")
        logs = get_logs(i['name'])
        diagonosis = analyze_logs(logs, i['name'])
        logging.info(f"Diagnosis for container '{i['name'] }:\{diagonosis}")
        fix_container(i['name'])

    else:
        print("All issues have been addressed.")
    logging.info(f"Agent run completed at {datetime.now()}")
    time.sleep(60) 



if __name__ == "__main__":
    run_agent()
    
