import logging

logger = logging.getLogger(__name__)

def simple_summarize_search_results(search_results: str, summary_prompt: str = None) -> str:
    """
    Super simple file ID extraction from Box search results.
    No external dependencies, just basic string processing.
    
    Args:
        search_results: The output from box_search tool
        summary_prompt: Optional custom prompt (not used)
        
    Returns:
        Simple instructions for using Box AI Ask
    """
    try:
        logger.info("🚀 Starting simple file ID extraction...")
        
        if not search_results or not isinstance(search_results, str):
            return "No search results provided or invalid format."
        
        # Count lines that contain file info
        lines = search_results.split('\n')
        file_count = 0
        
        for line in lines:
            if 'Type: file' in line and 'ID:' in line:
                file_count += 1
        
        logger.info(f"📊 Found {file_count} potential file entries")
        
        if file_count == 0:
            return """No file information found in the search results.

**What to do:**
1. Try a different search query
2. Check if the search returned file results
3. Use the box_search tool again with different terms

**For manual extraction:**
Look for lines containing 'Type: file' and 'ID:' in your search results."""
        
        # Simple response
        result = f"""Found {file_count} files in your search results!

**To analyze these files with Box AI Ask:**

1. **Look for file IDs** in your search results (lines with 'Type: file' and 'ID:')
2. **Use the box_ai_ask tool** with the file ID in this format:
   ```json
   {{"type": "file", "id": "FILE_ID_HERE"}}
   ```

**Example prompts:**
• "Summarize the key points in 3 bullet points"
• "What are the main findings?"
• "Extract the compliance requirements"
• "Give me a 2-sentence summary"

**Current status:** {file_count} files detected and ready for analysis!"""
        
        logger.info("✅ Simple file ID extraction completed")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in simple file ID extraction: {e}")
        return f"Error during file ID extraction: {str(e)}" 