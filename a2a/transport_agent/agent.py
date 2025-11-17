import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard, AgentCapabilities

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "id-iprd-1111-ps-abcchallenge"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

transport_agent_card = AgentCard(
    name="transport_agent",
    # url="http://localhost:8003",
    url="https://transport-agent-333079573063.us-central1.run.app",
    description="Helpful assistant that can provide transportation information.",
    version="1.0.0",
    capabilities=AgentCapabilities(),
    skills=[
        {
            "id": "transport_agent",
            "name": "Transport Agent Assistant",
            "description": "Helpful assistant that can provide transportation information between two locations.",
            "tags": ["transportation", "travel", "routes", "price"],
        }
    ],
    examples=[
        "How can I go to Jakarta from Bali?",
        "What transportation options are available from London to Paris and what are their prices?",
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    supports_authenticated_extended_card=False,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Helpful assistant that can provide transportation information.",
    instruction="""Use English language.
                Answer user questions to the best of your knowledge.
                When asked about transportation, use the `google_search` to find information about transportation options, prices, and routes between specified locations.
                Always ask for the origin and destination if they are not provided.
                """,
    tools=[google_search],
)

a2a_app = to_a2a(
    root_agent,
    port=8003,
    agent_card=transport_agent_card,
)
