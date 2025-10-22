import os
import logging 
import requests
import json
from dotenv import load_dotenv
from box_auth import JWTBoxAuth

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_available_hubs() -> list:
    """
    Retrieves all available hubs for the requesting enterprise using the new Box Hubs API.
    
    Returns:
        List of hub objects with their metadata
    """
    try:
        # Initialize JWT authentication
        auth = JWTBoxAuth()
        headers = auth.get_headers()
        
        # Add required Box API version header for Hubs API
        headers["box-version"] = "2025.0"
        
        logger.info("🔍 Retrieving available hubs from Box...")
        
        # Use the new Box Hubs API endpoint
        url = "https://api.box.com/2.0/hubs"
        # Use only basic parameters that are definitely supported
        params = {
            "limit": 100  # Reduced limit for better compatibility
        }
        
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"📥 Box Hubs API response status: {response.status_code}")
        
        # Log the full response for debugging
        if response.status_code != 200:
            logger.error(f"❌ Box Hubs API error: {response.status_code} - {response.text}")
            # Try without any parameters as fallback
            logger.info("🔄 Trying fallback call without parameters...")
            response = requests.get(url, headers=headers)
            logger.info(f"📥 Fallback response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"❌ Fallback also failed: {response.text}")
                return []
        
        response.raise_for_status()
        response_data = response.json()
        hubs = response_data.get("entries", [])
        
        logger.info(f"✅ Found {len(hubs)} available hubs")
        for hub in hubs:
            logger.info(f"   📁 Hub: {hub.get('title', 'Untitled')} (ID: {hub.get('id')}) - {hub.get('description', 'No description')}")
        
        return hubs
        
    except Exception as e:
        logger.error(f"❌ Error retrieving hubs: {e}")
        return []

def select_best_hub(prompt: str, hubs: list) -> dict:
    """
    Intelligently selects the most relevant hub based on the user's prompt.
    
    Args:
        prompt: The user's question or prompt
        hubs: List of available hubs
        
    Returns:
        The selected hub object or None if no suitable hub found
    """
    if not hubs:
        logger.warning("⚠️ No hubs available for selection")
        return None
    
    # Convert prompt to lowercase for better matching
    prompt_lower = prompt.lower()
    
    # Define priority keywords for different hub types
    priority_keywords = {
        "regulatory": ["regulation", "regulatory", "compliance", "policy", "legal", "rg", "rep"],
        "financial": ["financial", "finance", "banking", "accounting", "budget", "revenue", "cost"],
        "operational": ["operations", "operational", "process", "workflow", "procedure", "manual"],
        "strategic": ["strategy", "strategic", "planning", "quarterly", "annual", "roadmap", "initiative"],
        "technical": ["technical", "technology", "system", "platform", "infrastructure", "architecture"],
        "hr": ["hr", "human resources", "personnel", "employee", "staff", "hiring", "training"],
        "marketing": ["marketing", "brand", "campaign", "advertising", "promotion", "gtm"]
    }
    
    # Score each hub based on relevance
    hub_scores = []
    
    for hub in hubs:
        score = 0
        hub_title = hub.get('title', '').lower()
        hub_description = hub.get('description', '').lower()
        
        # Check for exact matches in title and description
        for category, keywords in priority_keywords.items():
            for keyword in keywords:
                if keyword in hub_title:
                    score += 10  # High score for title matches
                if keyword in hub_description:
                    score += 5   # Medium score for description matches
                if keyword in prompt_lower:
                    score += 3   # Bonus for keyword in user prompt
        
        # Additional scoring factors
        if hub.get('is_ai_enabled', False):
            score += 2  # Bonus for AI-enabled hubs
        
        if hub.get('view_count', 0) > 100:
            score += 1  # Bonus for frequently accessed hubs
        
        hub_scores.append({
            'hub': hub,
            'score': score,
            'title': hub_title,
            'description': hub_description
        })
    
    # Sort by score (highest first)
    hub_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Log the scoring results
    logger.info("🏆 Hub selection scoring results:")
    for i, item in enumerate(hub_scores[:5]):  # Show top 5
        logger.info(f"   {i+1}. {item['hub'].get('title')} - Score: {item['score']}")
    
    # Return the highest scoring hub
    if hub_scores and hub_scores[0]['score'] > 0:
        selected_hub = hub_scores[0]['hub']
        logger.info(f"🎯 Selected hub: {selected_hub.get('title')} (ID: {selected_hub.get('id')})")
        return selected_hub
    else:
        # If no good match, return the first hub as fallback
        fallback_hub = hubs[0]
        logger.info(f"🔄 No specific hub match found, using fallback: {fallback_hub.get('title')}")
        return fallback_hub

def box_hub_ask(prompt: str) -> str:
    """
    Intelligently discovers and uses the most relevant Box Hub to answer the user's question.
    
    Args:
        prompt: The question or prompt to ask the Box Hub.
        
    Returns:
        The answer provided by the Box Hub, or an error message.
    """
    try:
        logger.info(f"🔍 Box Hub Ask: '{prompt}'")
        
        # Step 1: Get all available hubs
        hubs = get_available_hubs()
        if not hubs:
            return "Error: No Box hubs available. Please check your Box configuration and permissions."
        
        # Step 2: Select the best hub for this question
        selected_hub = select_best_hub(prompt, hubs)
        if not selected_hub:
            return "Error: Unable to select an appropriate Box hub for your question."
        
        hub_id = selected_hub.get('id')
        hub_title = selected_hub.get('title', 'Unknown Hub')
        
        logger.info(f"🎯 Using hub: {hub_title} (ID: {hub_id}) for prompt: '{prompt}'")
        
        # Step 3: Initialize JWT authentication
        auth = JWTBoxAuth()
        headers = auth.get_headers()
        
        # Step 4: Send the question to the selected hub
        url = "https://api.box.com/2.0/ai/ask"
        payload = {
            "mode": "multiple_item_qa",
            "items": [
                {
                    "type": "hubs",
                    "id": hub_id
                }
            ],
            "prompt": prompt,
            "includes_citations": True
        }
        
        logger.info(f"🚀 Sending request to Box AI API for hub {hub_title}")
        logger.info(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"📥 Box AI API response status: {response.status_code}")
        
        response.raise_for_status()
        response_data = response.json()
        
        logger.info(f"🔍 Box AI API response: {json.dumps(response_data, indent=2)}")
        
        # Extract the answer
        answer = response_data.get("answer")
        if answer:
            logger.info("✅ Box Hub provided an answer successfully")
            # Include hub context in the response
            return f"Answer from Box Hub '{hub_title}':\n\n{answer}"
        else:
            completion_reason = response_data.get("completion_reason", "No reason provided.")
            logger.warning(f"⚠️ Box Hub did not provide an answer. Reason: {completion_reason}")
            return f"Box Hub '{hub_title}' did not provide an answer. Reason: {completion_reason}"
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error during Box Hub API call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') else "No response details."
        return f"API Error: Failed to ask Box Hub. {error_details}"
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred in box_hub_ask: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}" 