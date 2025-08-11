
import os
from google.adk.agents import LlmAgent
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from google.adk.tools import FunctionTool

# --- DEFINE YOUR TOOLS HERE ---
from box_search import box_search
from box_ai_ask import box_ai_ask
from box_hub_ask import box_hub_ask

def get_weather(location: str) -> str:
    """Gets the weather for a given location."""
    # In a real scenario, you might call a weather API here.
    return f"The weather in {location} is sunny."


class GeminiAgent(LlmAgent):
    """An agent powered by the Gemini model via Vertex AI."""

    # --- AGENT IDENTITY ---
    # These are the default values. The notebook can override them.
    name: str = "enterprise_content_discovery_agent"
    description: str = "A professional enterprise content discovery assistant powered by Gemini, specializing in Box content search and enterprise document management."

    def __init__(self, **kwargs):
        print("Initializing GeminiAgent...")
        # --- SET YOUR SYSTEM INSTRUCTIONS HERE ---
        instructions = """
        You are a professional enterprise content discovery assistant powered by Gemini. Your primary role is to help users find and access content within their Box enterprise environment.

        CORE CAPABILITIES:
        - Box Content Search: Use the box_search tool to find files, documents, and folders in Box
        - Box AI Ask: Use the box_ai_ask tool to ask intelligent questions about specific file content
        - Box Hub Ask: Use the box_hub_ask tool to ask questions that will automatically discover and use the most relevant Box Hub
        - Enterprise Content Discovery: Help users locate specific documents, regulatory files, reports, and other business content
        - Content Organization: Provide structured summaries of search results with file names, types, and relevant details

        BOX SEARCH GUIDELINES:
        - Always use the box_search tool when users ask to find documents, files, or content
        - Provide clear, organized summaries of search results
        - Include file counts and key details like file types and names
        - If no results are found, suggest alternative search terms or broader queries
        - For regulatory documents, highlight compliance-related content
        - For reports and documents, organize by relevance and recency

        BOX AI ASK GUIDELINES:
        - Use the box_ai_ask tool when users want to ask questions about specific file content
        - The items parameter should be a JSON string in format: [{"type": "file", "id": "FILE_ID"}]
        - For single files, you can use: {"type": "file", "id": "FILE_ID"}
        - Always include citations when asking questions about documents
        - Provide clear, actionable answers based on the AI's response

        BOX HUB ASK GUIDELINES:
        - Use the box_hub_ask tool when users want to ask general questions that could be answered by any Box Hub
        - The tool automatically discovers all available hubs and selects the most relevant one
        - Perfect for questions about company policies, procedures, or general knowledge
        - No need to specify hub IDs - the tool intelligently selects the best hub
        - Provides context about which hub was used for the answer

        WORKFLOW RECOMMENDATIONS:
        - Use box_search to find specific documents or files
        - Use box_ai_ask to ask questions about specific file content
        - Use box_hub_ask for general questions that could be answered by any hub
        - Combine all tools for comprehensive enterprise content discovery and analysis

        COMMUNICATION STYLE:
        - Professional and business-appropriate
        - Clear and concise responses
        - Helpful suggestions for refining searches
        - No puns or casual language - maintain enterprise professionalism

        You can also use the weather tool for location-based queries if needed.
        """
        

        # --- REGISTER YOUR TOOLS HERE ---
        tools = [
            get_weather,
            box_search,
            box_ai_ask,
            box_hub_ask
        ]

        super().__init__(
            model=os.environ.get("MODEL", "gemini-2.5-flash"),
            instruction=instructions,
            tools=tools,
            **kwargs,
        )


    def create_agent_card(self, agent_url: str) -> "AgentCard":
        return AgentCard(
            
name=self.name,
            description=self.description,
            url=agent_url,
            version="1.0.0",
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            capabilities=AgentCapabilities(streaming=True),
            skills=[
                AgentSkill(
                    id="box_content_search",
                    name="Box Content Search",
                    description="Search and discover files, documents, and content within Box enterprise environment.",
                    tags=["enterprise", "content-discovery", "box-search", "document-management"],
                    examples=["Find regulatory documents", "Search for quarterly reports", "Locate compliance files"]
                ),
                AgentSkill(
                    id="box_ai_ask",
                    name="Box AI Ask",
                    description="Ask intelligent questions about specific file content using Box AI capabilities.",
                    tags=["enterprise", "ai-analysis", "content-analysis", "document-intelligence"],
                    examples=["What are the key points in this document?", "Summarize the main findings", "Extract compliance requirements"]
                ),
                AgentSkill(
                    id="box_hub_ask",
                    name="Box Hub Ask",
                    description="Automatically discover and use the most relevant Box Hub to answer general questions.",
                    tags=["enterprise", "hub-intelligence", "auto-discovery", "knowledge-base"],
                    examples=["What are our company policies?", "How do I submit expense reports?", "What are our security procedures?"]
                ),

                AgentSkill(
                    id="enterprise_assistance",
                    name="Enterprise Assistance",
                    description="Provide professional business assistance and content organization.",
                    tags=["enterprise", "business", "professional"],
                    examples=["Organize search results", "Suggest search refinements", "Highlight relevant content"]
                )
            ]

        )
