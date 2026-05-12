from src.crew.agents import get_monitor_agent, get_analyzer_agent, get_executor_agent
from src.crew.tasks import get_monitor_task, get_analyzer_task, get_executor_task

monitor = get_monitor_agent()
analyzer = get_analyzer_agent()
executor = get_executor_agent()

monitor_task = get_monitor_task(monitor)
analyzer_task = get_analyzer_task(analyzer, [monitor_task])
executor_task = get_executor_task(executor, [analyzer_task])

print(f" Monitor Task created")
print(f" Analyzer Task created")
print(f" Executor Task created")
