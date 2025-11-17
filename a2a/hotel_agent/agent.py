import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard, AgentCapabilities

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "id-iprd-1111-ps-abcchallenge"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

hotel_agent_card = AgentCard(
    name="hotel_agent",
    # url="http://localhost:8002",
    url="https://hotel-agent-333079573063.us-central1.run.app",
    description="Helpful assistant that can provide nearby hotels information.",
    version="1.0.0",
    capabilities=AgentCapabilities(),
    skills=[
        {
            "id": "hotel_agent",
            "name": "Hotel Agent Assitant",
            "description": "Helpful assistant that can provide nearby hotels information.",
            "tags": ["hotel", "hotel information", "nearby hotels"],
        }
    ],
    examples=["Can you share hotel information near Jakarta city?"],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    supports_authenticated_extended_card=False,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Helpful assistant that can provide nearby hotels information.",
    instruction="""Use English language.
                Answer user questions to the best of your knowledge.
                When asked about nearby hotels, use the `google_search` to find information about nearby hotels in the specified location.
                Always ask for the location if it is not provided.
                """,
    tools=[google_search],
)

a2a_app = to_a2a(
    root_agent,
    port=8002,
    agent_card=hotel_agent_card,
)
