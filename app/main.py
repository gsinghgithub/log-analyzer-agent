from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
import json

# Import your existing tool
from app.tools import analyze_logs

app = FastAPI()
client = Anthropic()

class LogInput(BaseModel):
    log_text: str


@app.post("/analyze")
def analyze(log_input: LogInput):
    """
    FastAPI endpoint for Claude-powered Log Analyzer Agent.
    Claude decides when to call analyze_logs automatically.
    """

    tools = [
        {
            "name": "analyze_logs",
            "description": "Analyze log text and extract errors",
            "input_schema": {
                "type": "object",
                "properties": {
                    "log_text": {"type": "string"}
                },
                "required": ["log_text"]
            }
        }
    ]

    # Step 1: Send user message to Claude
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        tools=tools,
        tool_choice="auto",
        messages=[
            {
                "role": "user",
                "content": f"Analyze these logs:\n{log_input.log_text}"
            }
        ]
    )

    # Step 2: If Claude decides to call a tool
    if response.stop_reason == "tool_use":
        tool_call = response.content[0]

        if tool_call.name == "analyze_logs":
            # Execute your Python tool
            tool_result = analyze_logs(**tool_call.input)

            # Step 3: Send tool result back to Claude for final reasoning
            final_response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": "Here is the result of the tool execution."
                    },
                    {
                        "role": "assistant",
                        "content": tool_call
                    },
                    {
                        "role": "tool",
                        "tool_name": "analyze_logs",
                        "content": json.dumps(tool_result)
                    }
                ]
            )

            return {"result": final_response.content[0].text}

    # Step 4: If Claude responded directly without tool use
    return {"result": response.content[0].text}
