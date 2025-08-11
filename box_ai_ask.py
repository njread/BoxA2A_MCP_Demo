import os
import logging 
import requests
import json
from dotenv import load_dotenv
from box_auth import JWTBoxAuth

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def box_ai_ask(prompt: str, items: str) -> str:
    """
    Sends a prompt to Box AI to get answers based on specified file content.
    Uses JWT authentication for secure access.

    Args:
        prompt: The question or prompt to ask the AI.
        items: JSON string of file objects in the format [{"type": "file", "id": "FILE_ID"}]
               Example: '[{"type": "file", "id": "12345"}]'

    Returns:
        The answer provided by the Box AI, or an error message.
    """
    try:
        logger.info(f"🔍 Box AI Ask: '{prompt}' for items: {items}")
        
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
        logger.error(f"❌ An unexpected error occurred in box_ai_ask: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}" 