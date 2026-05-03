import docker
client = docker.from_env()
containers = client.containers.list()
def get_containers():
    
    
    for c in containers:
        print(f"Name: {c.name}, Status: {c.status}, ID: {c.short_id}")

get_containers() 