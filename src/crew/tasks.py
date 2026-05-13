from crewai import Task


def get_monitor_task(agent):
    return Task(
        description="""
        Use DetectFailedContainers tool to scan all Docker containers.
        Return the exact name, status and ID of any failed containers.
        If all healthy, say so clearly.
        """,
        expected_output="List of failed containers with Name, Status, ID. Or: All containers healthy.",
        agent=agent
    )


def get_analyzer_task(agent, context):
    return Task(
        description="""
        From the monitor output, get the failed container name.
        Call SearchIncidents with that container name.
        If NO MEMORY HIT, call AnalyzeErrorType with the container name, then call SaveIncident with 'container_name|||error_type|||action'.
        Report the container name, error type, and action.
        """,
        expected_output="""Container: <name>
Error Type: <type>
Source: MEMORY or ANALYSIS
Action: <action>""",
        agent=agent,
        context=context
    )


def get_executor_task(agent, context):
    return Task(
        description="""
        Get container name and error type from analyzer output.
        Steps:
        1. Call FixContainer with format: container_name|||error_type
        2. If error type contains CRASH or UNKNOWN call SendSlackAlert
        3. Report result
        """,
        expected_output="""Container: <name>
Action taken: <action>
Result: <success/failed>
Alert sent: <yes/no>
Final status: <running/needs attention>""",
        agent=agent,
        context=context
    )
