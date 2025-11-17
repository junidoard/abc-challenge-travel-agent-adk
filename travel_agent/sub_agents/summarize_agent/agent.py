from google.adk import Agent

from . import prompt

MODEL = "gemini-2.5-pro"

summarize_agent = Agent(
    model=MODEL,
    name="summarize_agent",
    description=(
        "A helpful agent that summarizes information from other agents (planner, weather, hotel, transport, document) "
        "and presents it in a standard JSON format."
    ),
    instruction=prompt.SUMMARIZE_AGENT_PROMPT,
    output_key="summarize_agent_output",
    tools=[],
)
