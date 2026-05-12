import os
from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

print("Connected")

# v4 correct API
with langfuse.start_as_current_observation(
    name="test-self-healing-scan"
) as observation:
    observation.update(
        input={"container": "test-nginx", "status": "exited"},
        output={"action": "restarted", "result": "success"}
    )
    print(f"Trace ID: {langfuse.get_current_trace_id()}")

langfuse.flush()
print("Flushed — check cloud.langfuse.com now")
