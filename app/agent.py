from anthropic import Anthropic
import json
from app.tools import analyze_logs

client = Anthropic()

def run_claude_agent(log_text: str):
    """
    Claude-powered Log Analyzer Agent.
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

    # Send message to Claude
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        tools=tools,
        tool_choice="auto",
        messages=[
            {
                "role": "user",
                "content": f"Analyze these logs:\n{log_text}"
            }
        ]
    )

    # If Claude calls a tool
    if response.stop_reason == "tool_use":
        tool_call = response.content[0]

        if tool_call.name == "analyze_logs":
            result = analyze_logs(**tool_call.input)

            # Send tool result back to Claude
            final_response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": "Here is the tool result."
                    },
                    {
                        "role": "assistant",
                        "content": tool_call,
                    },
                    {
                        "role": "tool",
                        "tool_name": "analyze_logs",
                        "content": json.dumps(result)
                    }
                ]
            )

            return final_response.content[0].text

    # If Claude responded directly
    return response.content[0].text
