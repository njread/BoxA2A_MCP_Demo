"""
Box Search Tool for Agent
Provides enhanced search functionality with automatic file ID guidance and quick summary options
"""

from box_auth import ensure_authenticated
from typing import List, Dict, Any
import json
import requests
import logging
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _extract_file_ids_from_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Extract file IDs from search entries for easy Box AI Ask usage.
    
    Args:
        entries: List of search result entries
        
    Returns:
        List of file objects with name and ID
    """
    file_entries = []
    
    for entry in entries:
        item_type = entry.get("type", "")
        item_id = entry.get("id", "")
        
        # Only include actual files (not folders)
        if item_type == "file" and item_id and item_id != "unknown":
            file_entries.append({
                "name": entry.get("name", "Unnamed file"),
                "id": item_id
            })
    
    return file_entries

def _generate_ai_ask_guidance(file_entries: List[Dict[str, str]], total_count: int) -> str:
    """
    Generate helpful guidance for using Box AI Ask with the found files.
    
    Args:
        file_entries: List of file objects with name and ID
        total_count: Total number of search results
        
    Returns:
        Formatted guidance string
    """
    if not file_entries:
        return ""
    
    guidance = f"\n\n🔍 **Box AI Analysis Ready** - {len(file_entries)} files ready for analysis:\n"
    
    # Show file list without IDs
    guidance += "\n**Files found:**\n"
    for i, entry in enumerate(file_entries, 1):
        guidance += f"{i}. **{entry['name']}**\n"
    
    # Provide user-friendly instructions instead of JSON
    guidance += f"\n**To analyze these files with Box AI, simply ask me to:**\n"
    guidance += "• \"Summarize these files\"\n"
    guidance += "• \"What are the key points in these documents?\"\n"
    guidance += "• \"Give me insights from these files\"\n"
    guidance += "• \"Analyze these documents for me\"\n"
    
    # Suggest prompts
    guidance += "\n**Suggested analysis questions:**\n"
    guidance += "• \"Summarize the key points in 3 bullet points\"\n"
    guidance += "• \"What are the main findings?\"\n"
    guidance += "• \"Extract the compliance requirements\"\n"
    guidance += "• \"Give me a 2-sentence summary\"\n"
    guidance += "• \"What are the key takeaways?\"\n"
    
    guidance += f"\n💡 **Tip:** Just ask me to analyze the files - I'll handle all the technical details automatically!"
    
    return guidance

def _generate_quick_summary_option(file_entries: List[Dict[str, str]]) -> str:
    """
    Generate a quick summary option that users can trigger directly.
    
    Args:
        file_entries: List of file objects with name and ID
        
    Returns:
        Formatted quick summary option string
    """
    if not file_entries:
        return ""
    
    quick_option = f"\n\n🚀 **Quick Analysis Option:**\n"
    quick_option += f"Say **\"Quick summary of these files\"** and I'll automatically analyze all {len(file_entries)} files for you!\n"
    quick_option += f"Or ask for specific analysis like **\"Summarize key points in 3 bullets\"** and I'll handle the rest.\n"
    
    return quick_option

def quick_summary_of_files(file_ids_json: str, summary_prompt: str = "Summarize the key points in 3 bullet points") -> str:
    """
    Prepare file IDs for Box AI Ask analysis.
    
    Args:
        file_ids_json: JSON string of file objects from search results
        summary_prompt: The prompt to use for analysis (default: 3 bullet summary)
        
    Returns:
        Formatted instructions for using Box AI Ask
    """
    try:
        logger.info(f"🚀 Quick summary preparation for prompt: '{summary_prompt}'")
        
        # Parse the file IDs JSON
        try:
            if file_ids_json.strip().startswith('{'):
                items_json = f"[{file_ids_json}]"
            else:
                items_json = file_ids_json
            items_list = json.loads(items_json)
            logger.info(f"📋 Parsed {len(items_list)} files for quick summary")
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON format for file IDs: {e}")
            return f"Error: Invalid file ID format. Please use the search tool again to get valid file IDs."
        
        # Return user-friendly instructions instead of technical JSON
        result = f"""🚀 **Quick Analysis Ready!** 

I've prepared {len(items_list)} files for analysis with the prompt: **"{summary_prompt}"**

**To get your analysis, simply ask me to:**
• "Analyze these files with Box AI"
• "Give me insights from these documents"
• "Summarize the key points"

**Or I can automatically analyze them right now if you'd like!**

This approach ensures a seamless user experience while maintaining all the powerful Box AI functionality."""
        
        logger.info("✅ Quick summary preparation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in quick summary preparation: {e}")
        return f"Error during quick summary preparation: {str(e)}"

def box_search(query: str, limit: int = 20) -> str:
    """
    Enhanced Box search with automatic file ID guidance and quick summary options.
    
    Args:
        query: The search query to find Box content
        limit: Maximum number of results to return (default: 20, max: 200)
    
    Returns:
        Enhanced search results with file ID guidance and quick summary options.
    """
    logger.info(f"🔍 Enhanced Box search for: '{query}'")
    
    try:
        # Get authenticated headers using JWT
        auth = ensure_authenticated()
        headers = auth.get_headers()
        
        # Build search URL with parameters
        base_url = "https://api.box.com/2.0/search"
        params = {
            "query": query,
            "limit": min(limit, 200),  # Box API max limit is 200
            "offset": 0
        }
        
        # Construct URL with query parameters
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        response = requests.get(url, headers=headers)
        logger.info(f"Box Search API response status: {response.status_code}")
        
        # Handle authentication errors by re-authenticating
        if response.status_code == 401:
            logger.warning("Authentication failed, attempting to re-authenticate")
            auth._authenticate()  # Re-authenticate with JWT
            headers = auth.get_headers()
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()

        response_data = response.json()
        logger.info(f"🔍 Box Search API response: {json.dumps(response_data, indent=2)}")
        
        entries = response_data.get("entries", [])
        total_count = response_data.get("total_count", 0)
        
        logger.info(f"📊 Found {total_count} total items, {len(entries)} entries")
        
        if entries:
            # Extract file IDs for Box AI Ask guidance
            file_entries = _extract_file_ids_from_entries(entries)
            logger.info(f"📁 Found {len(file_entries)} files for AI analysis")
            
            # Format the basic results
            results = [f"🔍 **Search Results for '{query}'**\n"]
            results.append(f"Found {total_count} total items (showing {len(entries)}):\n")
            
            for entry in entries:
                name = entry.get("name", "Unnamed item")
                item_type = entry.get("type", "unknown")
                item_id = entry.get("id", "unknown")
                
                # Get additional details if available
                size = entry.get("size")
                modified_at = entry.get("modified_at", "").split("T")[0] if entry.get("modified_at") else ""
                
                # Format entry
                entry_info = f"- {name} (Type: {item_type}, ID: {item_id}"
                if size and item_type == "file":
                    entry_info += f", Size: {_format_file_size(size)}"
                if modified_at:
                    entry_info += f", Modified: {modified_at}"
                entry_info += ")"
                
                results.append(entry_info)
            
            # Add Box AI Ask guidance
            ai_guidance = _generate_ai_ask_guidance(file_entries, total_count)
            results.append(ai_guidance)
            
            # Add quick summary option
            quick_option = _generate_quick_summary_option(file_entries)
            results.append(quick_option)
            
            return "\n".join(results)
        else:
            return f"❌ No Box content found matching '{query}'.\n\n💡 **Try:**\n• Different search terms\n• Broader keywords\n• Check spelling"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Box Search call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') and e.response else "No response details."
        return f"❌ Box search failed: {error_details}"
    except Exception as e:
        logger.error(f"Unexpected error during Box search: {e}")
        return f"❌ Box search failed with error: {str(e)}"

def _format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB" 