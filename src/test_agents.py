from crew.agents import get_monitor_agent, get_analyzer_agent, get_executor_agent

monitor = get_monitor_agent()
analyzer = get_analyzer_agent()
executor = get_executor_agent()

print(f" Monitor Agent: {monitor.role}")
print(f" Analyzer Agent: {analyzer.role}")
print(f" Executor Agent: {executor.role}")
