
from openai import OpenAI

client = OpenAI()

def create_agent():
    """
    Creates the Log Analyzer Agent using OpenAI Assistants API.
    The agent knows how to call the analyze_logs tool.
    """

    assistant = client.beta.assistants.create(
        name="Log Analyzer Agent",
        instructions=(
            "You are a Log Analyzer Agent. "
            "When the user provides log text, call the analyze_logs tool "
            "to extract errors and summarize issues."
        ),
        model="gpt-4.1",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "analyze_logs",
                    "description": "Analyze log text and extract errors",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "log_text": {"type": "string"}
                        },
                        "required": ["log_text"]
                    }
                }
            }
        ]
    )

    return assistant
