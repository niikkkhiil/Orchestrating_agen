from crewai import Agent
from crew.tools import (
    list_containers,
    detect_failed_containers,
    get_container_logs,
    restart_container
)

def get_monitor_agent():
    return Agent(
        role = "Infrastructure Monitor",
        goal= "Detect any Docker container that are failling or have stopped unexpectedly",
        backstory = """You are an Expert Infrastructure Monitoring specialist, with years of experience watching over containerized systems You are vigilant, precise, 
        and always the first to spot when something goes wrong.""",
        tools = [list_containers, detect_failed_containers],
        verbose = True
    )
def get_analyzer_agent():
    return Agent(
        role = "Failure Analyzer",
        goal = "Analyze the container logs to determine the root cause of failure and recommend fixes",
        backstory = """" You are a senior DevOps engineer specializing in diagnosing 
        containerized application failures. You read logs carefully, identify patterns, 
        and always provide clear cause and fix recommendations.""",
        tools = [get_container_logs],
        verbose = True
    )

def get_executor_agent():
    return Agent(
        role = "Infrastructure Executor",
        goal = "Apply fixes to failed Docker containers based on the analyst's recommendations",
        backstory = """You are a reliable infrastructure engineer responsible for applying 
        fixes to production systems. You act on clear instructions, restart containers, 
        and confirm every action you take.""",
        tools = [restart_container],
        verbose = True
    )