from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

planner_agent = Agent(
    model=MODEL,
    name="planner_agent",
    description=(
        "A concise, budget-focused AI travel planner that builds complete, "
        "day-by-day itineraries—including flights, hotels, "
        "and activities—that strictly adhere to your total budget."
    ),
    instruction=prompt.PLANNER_PROMPT,
    # output_key="trip_planner_activity_output",
    tools=[google_search],
)
