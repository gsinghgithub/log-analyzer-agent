from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI()
app = FastAPI()

class LogInput(BaseModel):
    log_text: str

@app.post("/analyze")
def analyze(log_input: LogInput):
    """
    API endpoint that sends logs to the Log Analyzer Agent.
    """

    # Create a thread for this request
    thread = client.beta.threads.create()

    # Run the agent
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="<YOUR_ASSISTANT_ID>",
        input=f"Analyze these logs:\n{log_input.log_text}"
    )

    # Poll until the run completes
    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve agent output
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content[0].text

    return {"result": result}

