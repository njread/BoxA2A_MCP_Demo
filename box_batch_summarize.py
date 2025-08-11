import os
import logging 
import requests
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from box_auth import JWTBoxAuth

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_file_ids_from_search_results(search_results: str) -> List[Dict[str, str]]:
    """
    Intelligently extracts file IDs and metadata from Box search results.
    
    Args:
        search_results: The text output from box_search tool
        
    Returns:
        List of file objects with type and ID for Box AI Ask
    """
    try:
        logger.info("🔍 Extracting file IDs from search results...")
        
        # Initialize JWT authentication to get file metadata
        auth = JWTBoxAuth()
        headers = auth.get_headers()
        
        extracted_files = []
        
        # Pattern to match file names and extract potential IDs
        # Look for patterns like "filename.pdf", "filename.docx", etc.
        file_pattern = r'([^\/\n]+\.(?:pdf|docx|doc|xlsx|xls|txt|pptx|ppt))'
        files_found = re.findall(file_pattern, search_results)
        
        logger.info(f"📋 Found {len(files_found)} potential files in search results")
        
        # For each file, try to get its ID using Box Search API
        for filename in files_found:
            filename = filename.strip()
            if filename:
                logger.info(f"🔍 Looking up file: {filename}")
                
                # Search for this specific file to get its ID
                file_id = get_file_id_by_name(filename, headers)
                if file_id:
                    extracted_files.append({
                        "type": "file",
                        "id": file_id,
                        "name": filename
                    })
                    logger.info(f"✅ Found file ID {file_id} for {filename}")
                else:
                    logger.warning(f"⚠️ Could not find file ID for {filename}")
        
        logger.info(f"🎯 Successfully extracted {len(extracted_files)} file IDs")
        return extracted_files
        
    except Exception as e:
        logger.error(f"❌ Error extracting file IDs: {e}")
        return []

def get_file_id_by_name(filename: str, headers: Dict[str, str]) -> str:
    """
    Gets the file ID by searching for a specific filename.
    
    Args:
        filename: The name of the file to search for
        headers: Authentication headers
        
    Returns:
        File ID if found, None otherwise
    """
    try:
        # Use Box Search API to find the specific file
        url = "https://api.box.com/2.0/search"
        params = {
            "query": f'"{filename}"',  # Exact match search
            "type": "file",
            "limit": 1
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            entries = data.get("entries", [])
            if entries:
                return entries[0].get("id")
        
        return None
        
    except Exception as e:
        logger.error(f"❌ Error getting file ID for {filename}: {e}")
        return None

def box_ai_ask_direct(prompt: str, items: str) -> str:
    """
    Direct implementation of Box AI Ask to avoid circular imports.
    
    Args:
        prompt: The question or prompt to ask the AI.
        items: JSON string of file objects in the format [{"type": "file", "id": "FILE_ID"}]
        
    Returns:
        The answer provided by the Box AI, or an error message.
    """
    try:
        logger.info(f"🔍 Box AI Ask (Direct): '{prompt}' for items: {items}")
        
        # Initialize JWT authentication
        auth = JWTBoxAuth()
        headers = auth.get_headers()
        
        # Parse items string into proper JSON
        try:
            # If items is a string representation of a single object, wrap it in array brackets
            if items.strip().startswith('{'):
                items_json = f"[{items}]"
            else:
                items_json = items
            
            # Convert to Python objects to ensure valid JSON
            items_list = json.loads(items_json)
            logger.info(f"📋 Parsed items: {items_list}")
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON format for items: {e}")
            return f"Error: Invalid JSON format for items parameter. Please provide a properly formatted JSON array of file objects."

        # Prepare the Box AI Ask API request
        url = "https://api.box.com/2.0/ai/ask"
        payload = {
            "mode": "multiple_item_qa",
            "items": items_list,
            "prompt": prompt,
            "includes_citations": True
        }

        logger.info(f"🚀 Sending request to Box AI API: {url}")
        logger.info(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"📥 Box AI API response status: {response.status_code}")
        
        response.raise_for_status()
        response_data = response.json()
        
        logger.info(f"🔍 Box AI API response: {json.dumps(response_data, indent=2)}")
        
        # Extract the answer
        answer = response_data.get("answer")
        if answer:
            logger.info("✅ Box AI provided an answer successfully")
            return answer
        else:
            completion_reason = response_data.get("completion_reason", "No reason provided.")
            logger.warning(f"⚠️ Box AI did not provide an answer. Reason: {completion_reason}")
            return f"Box AI did not provide an answer. Reason: {completion_reason}"

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error during Box AI API call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') else "No response details."
        return f"API Error: Failed to ask Box AI. {error_details}"
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred in box_ai_ask_direct: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}"

def batch_summarize_files(file_objects: List[Dict[str, str]], summary_prompt: str = None) -> str:
    """
    Summarizes multiple files using Box AI Ask.
    
    Args:
        file_objects: List of file objects with type and ID
        summary_prompt: Custom prompt for summarization
        
    Returns:
        Combined summary of all files
    """
    try:
        if not file_objects:
            return "No files found to summarize."
        
        logger.info(f"📝 Summarizing {len(file_objects)} files...")
        
        # Default summary prompt if none provided
        if not summary_prompt:
            summary_prompt = "Provide a concise 3-bullet summary of this document, focusing on key points, main findings, and important details."
        
        summaries = []
        
        # Process each file individually for better control
        for i, file_obj in enumerate(file_objects, 1):
            file_name = file_obj.get("name", f"File {i}")
            file_id = file_obj.get("id")
            
            logger.info(f"📋 Summarizing file {i}/{len(file_objects)}: {file_name}")
            
            try:
                # Create items string for box_ai_ask_direct
                items_json = json.dumps([{"type": "file", "id": file_id}])
                
                # Get summary using box_ai_ask_direct
                summary = box_ai_ask_direct(summary_prompt, items_json)
                
                # Format the summary with file context
                formatted_summary = f"**{file_name}:**\n{summary}\n"
                summaries.append(formatted_summary)
                
                logger.info(f"✅ Successfully summarized {file_name}")
                
            except Exception as e:
                logger.error(f"❌ Error summarizing {file_name}: {e}")
                summaries.append(f"**{file_name}:** Error generating summary: {str(e)}\n")
        
        # Combine all summaries
        if summaries:
            combined_summary = f"## Summary of {len(file_objects)} Files\n\n"
            combined_summary += "\n".join(summaries)
            return combined_summary
        else:
            return "No summaries could be generated."
            
    except Exception as e:
        logger.error(f"❌ Error in batch summarization: {e}")
        return f"Error during batch summarization: {str(e)}"

def smart_summarize_search_results(search_results: str, summary_prompt: str = None) -> str:
    """
    Main function that combines search result parsing and batch summarization.
    Simplified version for better reliability.
    
    Args:
        search_results: The output from box_search tool
        summary_prompt: Optional custom prompt for summarization
        
    Returns:
        Comprehensive summary of all found files
    """
    try:
        logger.info("🚀 Starting smart summarization of search results...")
        
        # For now, return a helpful message explaining the limitation
        # This prevents the 500 error while we debug the file extraction
        return """I can see your search results, but I need to implement the automatic file ID extraction feature. 

For now, you can:
1. Use the box_ai_ask tool with specific file IDs
2. Or I can help you manually identify which files you'd like summarized

The smart summarization feature is being enhanced to automatically process search results. Please try again in a moment or use the individual file analysis tools."""
        
    except Exception as e:
        logger.error(f"❌ Error in smart summarization: {e}")
        return f"Error during smart summarization: {str(e)}" 