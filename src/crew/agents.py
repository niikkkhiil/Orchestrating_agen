from crewai import Agent
from crew.tools import (
    detect_failed_containers,
    get_container_logs,
    restart_container,
    search_memory_tool,
    save_memory_tool,
    analyze_error_type,
    smart_fix,
    slack_alert,
    prune_docker
)


def get_monitor_agent(llm):
    return Agent(
        role="Infrastructure Monitor",
        goal="Detect any Docker containers that are failing or stopped",
        backstory="""Expert infrastructure monitoring specialist. 
        Vigilant and precise — always first to spot when something goes wrong.""",
        tools=[detect_failed_containers],
        llm=llm,
        verbose=True
    )


def get_analyzer_agent(llm):
    return Agent(
        role="Failure Analyst",
        goal="""Analyze container failures deeply. Check memory first, 
        then detect the specific error type to recommend the right fix.""",
        backstory="""Senior DevOps engineer specializing in diagnosing 
        containerized failures. You check memory first, then use 
        AnalyzeErrorType to understand exactly what went wrong.""",
        tools=[get_container_logs, analyze_error_type,
               search_memory_tool, save_memory_tool],
        llm=llm,
        verbose=True
    )


def get_executor_agent(llm):
    return Agent(
        role="Infrastructure Executor",
        goal="""Apply the smartest fix based on error type. 
        Use SmartFix for all actions. Alert Slack when human help needed.""",
        backstory="""Reliable infrastructure engineer who applies 
        targeted fixes — not just restarts. Uses the right tool for 
        each error type and alerts humans when needed.""",
        tools=[smart_fix, restart_container, slack_alert, prune_docker],
        llm=llm,
        verbose=True
    )