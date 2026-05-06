import docker 
from crewai.tools import tool

client = docker.from_env()

@tool("List docker containers")
def list_containers(input: str = ""):
    """ list all docker container and their status"""

    containers = client.containers.list(all=True)
    
    if not containers:
        return "No containers found."
    result = []
    for c in containers:
        result.append(f"Name: {c.name}, Status: {c.status}, ID: {c.short_id}")
    return "\n".join(result)

@tool("Detect Failed Containers")
def detect_failed_containers(input: str = ""):
    """" Detect containers that have stopped unexpectedly (status: exited or dead)"""

    containers = client.containers.list(all=True)
    issues = []

    for c in containers:
        if c.status in ["exited", "dead"]:
            issues.append(f"Name: {c.name}, Status: {c.status}, ID: {c.short_id}")
        if not issues:
            return "All Containers are Healthy."
    return "\n".join(issues)

@tool("Get Container Logs")
def get_container_logs(container_name: str):
    """Fetch the last 50 lines of logs for a specific container"""
    
    try:
        containers = client.containers.get(container_name)
        logs = containers.logs(tail=50).decode('utf-8')
        return logs if logs else "No logs available."
    except Exception as e:
        return f"Error retrieving logs: {e}"
    
@tool("Restart Container")
def restart_container(container_name: str):
    """Restart a specific container by name"""
    
    try:
        container = client.containers.get(container_name)
        container.restart()
        return f"Container '{container_name}' restarted successfully."
    except Exception as e:
        return f"Error restarting container '{container_name}': {e}"