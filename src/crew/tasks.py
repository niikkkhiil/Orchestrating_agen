from crewai import Task
from crew.agents import get_monitor_agent, get_analyzer_agent, get_executor_agent

def get_monitor_task(agent):
    return Task(
        description = """Scan all running and stopped Docker containers on this system. Identify any container that have status of 'exited' or 'dead', Return a clear list of failed containers with their name, status and ID.
        If all containers are healthy, report that clearly.""",
        expected_output=""" A list of failed containers in this format:
        - Container Name: <name> | Status: <status> | ID: <id>
        Or: 'All containers are healthy.' if none are failing.""",
        agent=agent
    )

def get_analyzer_task(agent, context):
    return Task(
        description="""
        For each failed container:
        1. Use SearchIncidents tool with the container name
        2. If MEMORY HIT — use known fix directly
        3. If NO MEMORY HIT:
           - Use AnalyzeErrorType with container name
           - Save to memory using SaveIncident: 'name|||error_type|||action'
        Always include error type in your output.
        """,
        expected_output="""
        Container: <name>
        Error Type: <type>
        Source: MEMORY or ANALYSIS
        Recommended Action: <action>
        """,
        agent=agent,
        context=context
    )

def get_executor_task(agent, context):
    return Task(
        description="""
        Based on analyst findings:
        1. Use SmartFix with: 'container_name|||error_type'
        2. If error is APP_CRASH or UNKNOWN — also send SlackAlert
        3. Report final status
        """,
        expected_output="""
        Container: <name>
        Action taken: <action>
        Result: <success/failed>
        Alert sent: <yes/no>
        Final status: <running/needs attention>
        """,
        agent=agent,
        context=context
    )
