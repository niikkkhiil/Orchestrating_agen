import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "dummy-not-used")

from langfuse import Langfuse
from crewai import Crew, Process, LLM
from crew.agents import get_monitor_agent, get_analyzer_agent, get_executor_agent
from crew.tasks import get_monitor_task, get_analyzer_task, get_executor_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

llm = LLM(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)


def run_crew():
    monitor = get_monitor_agent(llm)
    analyzer = get_analyzer_agent(llm)
    executor = get_executor_agent(llm)

    monitor_task = get_monitor_task(monitor)
    analyzer_task = get_analyzer_task(analyzer, [monitor_task])
    executor_task = get_executor_task(executor, [analyzer_task])

    return Crew(
        agents=[monitor, analyzer, executor],
        tasks=[monitor_task, analyzer_task, executor_task],
        process=Process.sequential,
        verbose=True
    )


def main():
    logging.info("Starting Self-Healing Agent...")
    langfuse.auth_check()
    logging.info("Langfuse tracing active")

    while True:
        with langfuse.start_as_current_observation(
            name="self-healing-scan"
        ) as observation:
            try:
                logging.info(f"Scan started at {datetime.now()}")
                crew = run_crew()
                result = crew.kickoff()

                observation.update(
                    input={"scan_time": datetime.now().isoformat()},
                    output={"result": str(result), "status": "success"}
                )
                logging.info(f"Scan complete:\n{result}")

            except Exception as e:
                error_msg = str(e)
                observation.update(
                    output={"status": "error", "error": error_msg}
                )
                if "rate_limit_exceeded" in error_msg:
                    logging.warning("Groq rate limit — waiting 2 minutes...")
                    time.sleep(120)
                    continue
                else:
                    logging.error(f"Error: {e}")

        langfuse.flush()
        logging.info("Next scan in 1 minutes...\n")
        time.sleep(60)


if __name__ == "__main__":
    main()