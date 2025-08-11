"""
Box Search Tool for Agent
Provides basic search functionality across Box content
"""

from box_auth import ensure_authenticated
from typing import List, Dict, Any
import json
import requests
import logging
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def box_search(query: str, limit: int = 20) -> str:
    """
    Searches Box content using the Box Search API.
    
    Args:
        query: The search query to find Box content
        limit: Maximum number of results to return (default: 20, max: 200)
    
    Returns:
        The search results from Box, or an error message.
    """
    logger.info(f"Searching Box content for: '{query}'")
    
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
            # Format the results nicely
            results = [f"Found {total_count} items (showing {len(entries)}):\n"]
            
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
            
            return "\n".join(results)
        else:
            return f"No Box content found matching '{query}'."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Box Search call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') and e.response else "No response details."
        return f"Box search failed: {error_details}"
    except Exception as e:
        logger.error(f"Unexpected error during Box search: {e}")
        return f"Box search failed with error: {str(e)}"

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