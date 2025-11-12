# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Trip planning: provide planning of a trip along with the itinerary"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# A2A
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "id-iprd-1111-ps-abcchallenge"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

from . import prompt
from .sub_agents.planner_agent import planner_agent
from .sub_agents.summarize_agent import summarize_agent

weather_agent = RemoteA2aAgent(
    name="weather_agent",
    description="Helpful assistant that can provide 7-day weather forecasts.",
    agent_card=(f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}"),
)

hotel_agent = RemoteA2aAgent(
    name="hotel_agent",
    description="Helpful assistant that can provide nearby hotels information.",
    agent_card=(f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}"),
)

transport_agent = RemoteA2aAgent(
    name="transport_agent",
    description="Helpful assistant that can provide transportation information.",
    agent_card=(f"http://localhost:8003{AGENT_CARD_WELL_KNOWN_PATH}"),
)

document_agent = RemoteA2aAgent(
    name="document_agent",
    description="Helpful assistant that can provide information about necessary travel documents.",
    agent_card=(f"http://localhost:8004{AGENT_CARD_WELL_KNOWN_PATH}"),
)

MODEL = "gemini-2.5-flash"

ai_travel_planner = LlmAgent(
    name="ai_travel_planner",
    model=MODEL,
    description=(
        "This is a top-level AI agent for trip planning. "
        "It orchestrates the entire planning process by first gathering 6 required inputs "
        "from the user (departure, destination, budget, people, date, duration). "
        "It then delegates tasks, calling the trip_planner_activity_agent for the detailed itinerary."
        "(If available) the weather_agent for a forecast. "
        "(If available) the hotel_agent for nearby hotels. "
        "(If available) the transport_agent for transportation information. "
        "(If available) the document_agent for necessary travel documents. "
        "Finally, it synthesizes these outputs into a single, cohesive response."
    ),
    instruction=prompt.ROOT_AGENT_PROMPT,
    output_key="ai_travel_planner_output",
    sub_agents=[
        weather_agent,
        hotel_agent,
        transport_agent,
        document_agent,
        summarize_agent,
    ],
    tools=[
        AgentTool(agent=planner_agent),
    ],
)

root_agent = ai_travel_planner
