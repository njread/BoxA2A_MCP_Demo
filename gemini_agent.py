
import os
from google.adk.agents import LlmAgent
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from google.adk.tools import FunctionTool

# --- DEFINE YOUR TOOLS HERE ---
from box_search import box_search, quick_summary_of_files
from box_ai_ask import box_ai_ask
from box_hub_ask import box_hub_ask
# Gradually re-enabling Box Doc Gen - adding smart discovery tools
from box_doc_gen import guide_capital_call_creation, create_sample_lp_data, smart_template_discovery, capital_call_workflow_assistant
# Adding focused FOIA tools
from foia_processor import foia_metadata_applier, foia_workflow_assistant, foia_report_generator
# Adding Box MCP Remote Server tools
from box_mcp_client import box_mcp_who_am_i, box_mcp_search_files, box_mcp_ai_qa_single_file, box_mcp_ai_qa_multi_file, box_mcp_ai_qa_hub, box_mcp_ai_extract_structured, box_mcp_workflow_assistant

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
        # - Box Doc Gen: Use document generation tools to create capital call notices and other documents
        - Enterprise Content Discovery: Help users locate specific documents, regulatory files, reports, and other business content
        - Content Organization: Provide structured summaries of search results with file names, types, and relevant details

        BOX SEARCH GUIDELINES:
        - Always use the box_search tool when users ask to find documents, files, or content
        - The enhanced search automatically provides file ID guidance for Box AI Ask
        - Search results include clean, user-friendly guidance without technical JSON
        - **NEW: Quick Summary Option** - Users can say "Quick summary of these files" for instant analysis
        - **QUICK SUMMARY PREPARATION**: When users ask for a quick summary, use the quick_summary_of_files tool to prepare file IDs and provide instructions for Box AI Ask
        - **AUTOMATIC ANALYSIS**: When users ask for analysis, summaries, or insights about found files, automatically use box_ai_ask with the search results
        - **HIDE TECHNICAL DETAILS**: Never show JSON or file IDs to users - handle all technical details automatically
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

        # Temporarily commenting out Box Doc Gen guidelines to isolate the issue
        # BOX DOC GEN GUIDELINES:
        # - Use the create_capital_call_notice_batch tool when users want to generate capital call notices
        # - Use the list_available_templates tool to help users find document templates
        # - Use the get_batch_status tool to check the progress of document generation
        # - Use the guide_capital_call_creation tool to provide comprehensive guidance on the process
        # - **CAPITAL CALL NOTICE WORKFLOW**: When users ask to create capital call notices:
        #   1. Help them find their template using list_available_templates
        #   2. Help them locate their output folder using box_search
        #   3. Guide them through preparing LP data using guide_capital_call_creation
        #   4. Execute the document generation using create_capital_call_notice_batch
        #   5. Provide the batch ID for status tracking
        # - **TEMPLATE MANAGEMENT**: Help users organize and find their document templates
        # - **BATCH PROCESSING**: Support generating multiple capital call notices in one operation
        # - **STATUS TRACKING**: Enable users to monitor document generation progress

        SMART CAPITAL CALL GUIDELINES:
        - Use the smart_template_discovery tool when users want to find and understand their available templates
        - Use the capital_call_workflow_assistant tool to guide users through the complete capital call notice creation process
        - **SMART TEMPLATE DISCOVERY**: Help users understand their available templates using existing search results
        - **WORKFLOW ASSISTANCE**: Guide users through each phase of capital call notice creation step by step
        - **PHASE-BASED GUIDANCE**: Break down the process into manageable phases with clear next actions
        - **INTEGRATION WITH EXISTING TOOLS**: Use Box search and Box AI to enhance the workflow
        - **MANUAL PROCESS SUPPORT**: Guide users through manual document creation when automation isn't available

        FOIA REQUEST PROCESSING GUIDELINES:
        - Use the foia_metadata_applier tool when users want to apply FOIA retention metadata to folders and files
        - Use the foia_workflow_assistant tool to guide users through the complete FOIA request processing workflow
        - Use the foia_report_generator tool to create comprehensive compliance reports and audit trails
        - **FOIA METADATA APPLICATION**: Apply your specific FOIA metadata template to folders and files
        - **WORKFLOW ORCHESTRATION**: Guide users through the complete FOIA request processing workflow step by step
        - **COMPLIANCE REPORTING**: Generate comprehensive reports with audit trails and compliance documentation
        - **METADATA TEMPLATE**: Use the specific FOIA template with retentionForFoia field
        - **FOLDER-BASED PROCESSING**: Apply metadata to entire folders and their contents
        - **AUDIT TRAIL**: Create complete audit trails for compliance tracking

        BOX MCP REMOTE SERVER GUIDELINES:
        - Use the box_mcp_who_am_i tool when users want to verify their Box user information and permissions
        - Use the box_mcp_search_files tool when users want enhanced file search with advanced filtering capabilities
        - Use the box_mcp_ai_qa_single_file tool when users want deep AI analysis of individual documents
        - Use the box_mcp_ai_qa_multi_file tool when users want cross-document analysis and pattern recognition
        - Use the box_mcp_ai_qa_hub tool when users want project-level insights and status analysis
        - Use the box_mcp_ai_extract_structured tool when users want to extract structured data from unstructured documents
        - Use the box_mcp_workflow_assistant tool when users want guidance on MCP capabilities and workflows
        - **MCP INTEGRATION**: Leverage Box MCP Remote Server for enhanced AI capabilities and seamless integration
        - **ADVANCED AI**: Use Box AI through MCP for deeper document analysis and insights
        - **STRUCTURED EXTRACTION**: Convert unstructured documents into structured data for better reporting
        - **CROSS-PLATFORM**: Works with Claude, Copilot Studio, Mistral AI, and other leading AI platforms
        - **ENTERPRISE SECURITY**: OAuth 2.0 authentication with enterprise-grade security controls

        WORKFLOW RECOMMENDATIONS:
        - Use box_search to find documents and automatically get file ID guidance
        - **NEW: Use quick_summary_of_files for instant analysis of search results**
        - **QUICK SUMMARY WORKFLOW**: When users ask for "quick summary" or "summarize these files", use quick_summary_of_files to prepare file IDs, then guide them to use Box AI Ask
        - **AUTOMATIC ANALYSIS WORKFLOW**: When users ask for analysis, insights, or summaries of found files, automatically execute box_ai_ask with the search results
        - **SEAMLESS USER EXPERIENCE**: Handle all file IDs and technical details automatically - never show JSON or technical details to users
        # - **CAPITAL CALL NOTICE WORKFLOW**: When users ask to create capital call notices, guide them through the complete process from template selection to document generation
        - **SMART CAPITAL CALL WORKFLOW**: When users ask to create capital call notices, use the capital_call_workflow_assistant to guide them through each phase step by step
        - **FOIA REQUEST WORKFLOW**: When users ask to process FOIA requests, use the foia_workflow_assistant to guide them through metadata application and compliance reporting
        - **BOX MCP WORKFLOW**: When users want enhanced AI capabilities, use Box MCP tools for deeper analysis, structured extraction, and cross-platform integration
        - Use box_ai_ask to ask questions about specific file content
        - Use box_hub_ask for general questions that could be answered by any hub
        # - Use Box Doc Gen tools for automated document creation and management
        - Use smart template discovery and workflow assistance for capital call notice creation
        - Use FOIA processing tools for compliance workflows and Box file management
        - Use Box MCP tools for advanced AI analysis, structured data extraction, and enhanced search capabilities
        - Combine all tools for comprehensive enterprise content discovery, analysis, guided document workflows, compliance processing, and advanced AI capabilities

        COMMUNICATION STYLE:
        - Professional and business-appropriate
        - Clear and concise responses
        - Helpful suggestions for refining searches
        - No puns or casual language - maintain enterprise professionalism

        TOOL DESCRIPTIONS:
        - get_weather: Get current weather information for a specific location
        - box_search: Enhanced Box search with automatic file ID guidance and clean, user-friendly results
        - box_ai_ask: Ask questions about specific file content using Box AI. Use this for automatic analysis of found files
        - box_hub_ask: Get answers from the most relevant Box Hub for general questions
        - quick_summary_of_files: Prepare file IDs and provide clean instructions for Box AI Ask analysis. Use this when users ask for "quick summary" or "summarize these files"
        - guide_capital_call_creation: Provide comprehensive guidance on creating capital call notices. Use this to help users understand the process and data requirements
        - create_sample_lp_data: Provide sample LP data structure with detailed explanations. Use this to help users understand how to prepare their data for capital call notices
        - smart_template_discovery: Smart template discovery using existing search results and user guidance. Use this to help users find and understand their available templates
        - capital_call_workflow_assistant: Complete workflow assistant for capital call notice creation. Use this to guide users through the entire process step by step
        - foia_metadata_applier: Apply FOIA retention metadata template to folders and files. Use this to tag files with FOIA compliance metadata
        - foia_workflow_assistant: Complete FOIA workflow assistant that guides users through the entire process. Use this to orchestrate the complete FOIA request workflow
        - foia_report_generator: Generate comprehensive FOIA compliance reports. Use this to create audit trails and compliance documentation
        - box_mcp_who_am_i: Get detailed information about the currently authenticated Box user via MCP. Use this to verify user permissions and account status
        - box_mcp_search_files: Search for files using keywords via Box MCP server with advanced filtering. Use this for enhanced file discovery
        - box_mcp_ai_qa_single_file: Ask questions to individual files using Box AI via MCP server. Use this for deep document analysis
        - box_mcp_ai_qa_multi_file: Ask questions across multiple files using Box AI via MCP server. Use this for cross-document analysis
        - box_mcp_ai_qa_hub: Ask questions about entire Box Hubs using Box AI via MCP server. Use this for project-level insights
        - box_mcp_ai_extract_structured: Extract structured metadata from files using Box AI via MCP server. Use this to convert unstructured documents into structured data
        - box_mcp_workflow_assistant: Guide users through Box MCP capabilities and workflows. Use this to understand and utilize MCP tools effectively
        # - foia_request_analyzer: Analyze Enron email data source to identify projects and create knowledge transfer plans. Use this for FOIA request processing
        # - box_foia_processor: Process Box files for FOIA compliance with metadata application and file locking. Use this to apply compliance metadata and security controls
        # - create_capital_call_notice_batch: Generate capital call notices for multiple LPs using Box Doc Gen API. Use this when users want to create capital call notices
        # - get_batch_status: Check the status of document generation batches. Use this to monitor progress of capital call notice generation

        QUICK SUMMARY WORKFLOW:
        - When users ask for "quick summary" or "summarize these files", use the quick_summary_of_files tool
        - Extract file IDs from the most recent search results
        - Provide formatted JSON and instructions for using Box AI Ask
        - Guide users to complete the analysis with the Box AI Ask tool

        AUTOMATIC ANALYSIS WORKFLOW:
        - When users ask for "analysis", "insights", "summarize", or "tell me about" found files, automatically use box_ai_ask
        - Extract file IDs from the most recent search results
        - Execute the analysis immediately without asking for additional user input
        - Return the analysis results directly to the user
        - Use the user's specific question as the prompt for box_ai_ask

        You can also use the weather tool for location-based queries if needed.
        """
        

        # --- REGISTER YOUR TOOLS HERE ---
        tools = [
            get_weather,
            box_search,
            box_ai_ask,
            box_hub_ask,
            quick_summary_of_files,
            guide_capital_call_creation,  # Testing basic Box Doc Gen functionality
            create_sample_lp_data,  # Adding sample data tool
            smart_template_discovery,  # Adding smart template discovery
            capital_call_workflow_assistant,  # Adding workflow assistant
            foia_metadata_applier,  # Adding FOIA metadata application tool
            foia_workflow_assistant,  # Adding FOIA workflow assistant
            foia_report_generator,  # Adding FOIA report generator
            box_mcp_who_am_i,  # Adding Box MCP user information tool
            box_mcp_search_files,  # Adding Box MCP search tool
            box_mcp_ai_qa_single_file,  # Adding Box MCP single file AI analysis
            box_mcp_ai_qa_multi_file,  # Adding Box MCP multi-file AI analysis
            box_mcp_ai_qa_hub,  # Adding Box MCP hub AI analysis
            box_mcp_ai_extract_structured,  # Adding Box MCP structured data extraction
            box_mcp_workflow_assistant,  # Adding Box MCP workflow assistant
            # foia_request_analyzer,  # Adding FOIA analysis tool
            # box_foia_processor,  # Adding Box FOIA processing tool
            # create_capital_call_notice_batch, # Temporarily commenting out Box Doc Gen tools
            # get_batch_status,
            # list_available_templates,
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
                ),
                AgentSkill(
                    id="quick_summary",
                    name="Quick Summary Analysis",
                    description="Automatically analyze multiple files from search results using Box AI for instant insights.",
                    tags=["enterprise", "ai-analysis", "batch-analysis", "content-summary"],
                    examples=["Quick summary of these files", "Summarize these files", "Analyze all found documents"]
                ),
                # Temporarily commenting out Box Doc Gen skills to isolate the issue
                # AgentSkill(
                #     id="capital_call_generation",
                #     name="Capital Call Notice Generation",
                #     description="Generate professional capital call notices using Box Doc Gen API with customizable templates and LP data.",
                #     tags=["enterprise", "document-generation", "capital-calls", "private-equity", "automation"],
                #     examples=["Create capital call notices for Fund III", "Generate capital call documents", "Make capital call notices for multiple LPs"]
                # ),
                # AgentSkill(
                #     id="document_templates",
                #     name="Document Template Management",
                #     description="Find, organize, and manage document templates for automated document generation.",
                #     tags=["enterprise", "template-management", "document-templates", "automation"],
                #     examples=["List available templates", "Find capital call templates", "Show me document templates"]
                # ),
                # AgentSkill(
                #     id="batch_processing",
                #     name="Batch Document Processing",
                #     description="Process multiple documents in batch operations with status tracking and progress monitoring.",
                #     tags=["enterprise", "batch-processing", "automation", "status-tracking"],
                #     examples=["Generate multiple capital call notices", "Check batch status", "Monitor document generation"]
                # ),
                AgentSkill(
                    id="foia_request_processing",
                    name="FOIA Request Processing",
                    description="Complete FOIA request processing workflow including metadata application and compliance reporting.",
                    tags=["enterprise", "foia", "compliance", "audit", "metadata", "security"],
                    examples=["Apply FOIA metadata to folder", "Process FOIA request", "Generate compliance report", "Help with FOIA workflow"]
                ),
                AgentSkill(
                    id="box_compliance_management",
                    name="Box Compliance Management",
                    description="Apply compliance metadata and security controls to Box files for regulatory requirements.",
                    tags=["enterprise", "compliance", "box", "metadata", "security", "access-control"],
                    examples=["Apply FOIA metadata to files", "Tag files for compliance", "Generate compliance reports", "Manage file metadata"]
                ),
                AgentSkill(
                    id="box_mcp_integration",
                    name="Box MCP Remote Server Integration",
                    description="Leverage Box MCP Remote Server for enhanced AI capabilities, structured data extraction, and cross-platform integration.",
                    tags=["enterprise", "mcp", "ai", "integration", "structured-data", "cross-platform"],
                    examples=["Search files via MCP", "Analyze documents with Box AI via MCP", "Extract structured data via MCP", "Get project status via MCP"]
                )
            ]

        )
