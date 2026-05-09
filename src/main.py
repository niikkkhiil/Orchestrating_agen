import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load env before importing crewai
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "dummy-not-used")

from crewai import Crew, Process, LLM
from crew.agents import get_monitor_agent, get_analyzer_agent, get_executor_agent
from crew.tasks import get_monitor_task, get_analyzer_task, get_executor_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def run_crew():
    logging.info(" Assembling crew...")

    monitor = get_monitor_agent(llm)
    analyzer = get_analyzer_agent(llm)
    executor = get_executor_agent(llm)

    monitor_task = get_monitor_task(monitor)
    analyzer_task = get_analyzer_task(analyzer, [monitor_task])
    executor_task = get_executor_task(executor, [analyzer_task])

    crew = Crew(
        agents=[monitor, analyzer, executor],
        tasks=[monitor_task, analyzer_task, executor_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


def main():
    logging.info(" Starting Self-Healing Agent...")

    while True:
        try:
            logging.info(f" Scan started at {datetime.now()}")
            crew = run_crew()
            result = crew.kickoff()
            logging.info(f" Scan complete:\n{result}")

        except Exception as e:
            error_msg = str(e)
            if "rate_limit_exceeded" in error_msg:
                logging.warning(" Groq rate limit hit — waiting 2 minutes before retry...")
                time.sleep(120)
                continue
            else:
                logging.error(f" Error: {e}")

        logging.info(" Next scan in 5 minutes...\n")
        time.sleep(300)


if __name__ == "__main__":
    main()