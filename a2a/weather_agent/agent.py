import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard, AgentCapabilities

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "id-iprd-1111-ps-abcchallenge"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

weather_agent_card = AgentCard(
    name="weather_agent",
    # url="http://localhost:8001",
    url="https://weather-agent-333079573063.us-central1.run.app",
    description="Helpful assistant that can provide weather forecasts.",
    version="1.0.0",
    capabilities=AgentCapabilities(),
    skills=[
        {
            "id": "weather_agent",
            "name": "Weather Agent Forecast",
            "description": "Helpful assistant that can provide weather forecasts.",
            "tags": ["weather", "weather forecast", "forecast"],
        }
    ],
    examples=["can you share 7-day forecast on nov 17, 2025, in Jakarta?"],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    supports_authenticated_extended_card=False,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant that can provide weather forecasts.",
    instruction="""Use English language.
                Answer user questions to the best of your knowledge.
                When asked about weather forecasts, use the `google_search` to provide a forecast for a specified location, start date, and end date/duration.
                Always ask for both location, start date, and end date/duration if they are not provided.
                """,
    tools=[google_search],
)

a2a_app = to_a2a(
    root_agent,
    port=8001,
    agent_card=weather_agent_card,
)
