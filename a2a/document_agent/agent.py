import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard, AgentCapabilities

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "id-iprd-1111-ps-abcchallenge"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

document_agent_card = AgentCard(
    name="document_agent",
    # url="http://localhost:8004",
    url="https://document-agent-333079573063.us-central1.run.app",
    description="Helpful assistant that can provide information about necessary travel documents.",
    version="1.0.0",
    capabilities=AgentCapabilities(),
    skills=[
        {
            "id": "document_agent",
            "name": "Document Agent Assistant",
            "description": "Helpful assistant that can provide information about necessary travel documents, visas, and passports between two locations.",
            "tags": [
                "documents",
                "travel documents",
                "visa",
                "passport",
                "requirements",
            ],
        }
    ],
    examples=[
        "What documents do I need to travel from Jakarta to Singapore?",
        "Do I need a visa for Japan as an Indonesian citizen?",
        "What are the passport requirements for traveling to the US?",
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    supports_authenticated_extended_card=False,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Helpful assistant that can provide information about necessary travel documents.",
    instruction="""Use English language.
                Answer user questions to the best of your knowledge.
                When asked about travel documents, use the `google_search` to find information about necessary documents, visas, and passport requirements between specified locations.
                Always ask for the origin and destination if they are not provided.
                """,
    tools=[google_search],
)

a2a_app = to_a2a(
    root_agent,
    port=8004,
    agent_card=document_agent_card,
)
