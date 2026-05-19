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
        If all containers are healthy, report that and stop — do not call any tools.
        Otherwise, call search_incidents with the container name.
        If NO MEMORY HIT, call analyze_error_type with the container name, then call save_incident with 'container_name|||error_type|||action'.
        Report the container name, error type, and action.
        """,
        expected_output="""All containers healthy. OR:
Container: <name>
Error Type: <type>
Source: MEMORY or ANALYSIS
Action: <action>""",
        agent=agent,
        context=context
    )


def get_executor_task(agent, context):
    return Task(
        description="""
        From the analyzer output, if all containers are healthy, report that and stop — do not call any tools.
        Otherwise get container name and error type, call smart_fix with format: container_name|||error_type.
        If error type contains CRASH or UNKNOWN also call slack_alert.
        Report result.
        """,
        expected_output="""All containers healthy. OR:
Container: <name>
Action taken: <action>
Result: <success/failed>
Alert sent: <yes/no>
Final status: <running/needs attention>""",
        agent=agent,
        context=context
    )
