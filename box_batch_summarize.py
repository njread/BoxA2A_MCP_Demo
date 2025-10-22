import os
import logging 
import json
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_file_ids_from_search_results(search_results: str) -> str:
    """
    Simplified file ID extraction from Box search results.
    Uses basic, reliable parsing instead of complex logic.
    
    Args:
        search_results: The output from box_search tool
        
    Returns:
        Formatted string with file IDs and instructions for Box AI Ask
    """
    try:
        logger.info("🔍 Starting simple file ID extraction...")
        
        if not search_results or not isinstance(search_results, str):
            return "No search results provided or invalid format."
        
        # Simple line-by-line processing
        file_entries = []
        lines = search_results.split('\n')
        
        logger.info(f"📋 Processing {len(lines)} lines from search results")
        
        for line_num, line in enumerate(lines, 1):
            # Skip empty lines
            if not line.strip():
                continue
                
            # Simple check: does this line contain file info?
            if 'Type: file' in line and 'ID:' in line:
                logger.info(f"📄 Found potential file line {line_num}: {line[:50]}...")
                
                # Extract filename (everything before the first parenthesis)
                try:
                    # Remove any leading dashes or bullets
                    clean_line = line.strip()
                    if clean_line.startswith('- '):
                        clean_line = clean_line[2:]
                    if clean_line.startswith('• '):
                        clean_line = clean_line[2:]
                    
                    # Find filename (before first parenthesis)
                    if '(' in clean_line:
                        filename = clean_line.split('(')[0].strip()
                    else:
                        filename = clean_line.strip()
                    
                    # Find ID (after "ID: " and before closing parenthesis or end of line)
                    id_start = clean_line.find('ID: ')
                    if id_start != -1:
                        id_start += 4  # Skip "ID: "
                        
                        # Find where ID ends
                        id_end = clean_line.find(')', id_start)
                        if id_end == -1:
                            id_end = len(clean_line)
                        
                        file_id = clean_line[id_start:id_end].strip()
                        
                        # Basic validation
                        if file_id and file_id != "unknown" and len(file_id) > 3:
                            file_entries.append({
                                "filename": filename,
                                "id": file_id
                            })
                            logger.info(f"✅ Extracted: {filename} (ID: {file_id})")
                        else:
                            logger.warning(f"⚠️ Invalid ID format: {file_id}")
                            
                except Exception as e:
                    logger.warning(f"⚠️ Could not parse line {line_num}: {str(e)}")
                    continue
        
        logger.info(f"📊 Found {len(file_entries)} valid file entries")
        
        # Generate simple, clear output
        if not file_entries:
            return """No file IDs could be extracted from the search results.

**Possible reasons:**
- Search results don't contain file information
- File format is different than expected
- No files were found in the search

**What to do:**
1. Try a different search query
2. Check if the search returned file results
3. Use the box_search tool again with different terms"""
        
        # Simple, clear formatting
        result = f"**Found {len(file_entries)} files for analysis:**\n\n"
        
        for i, entry in enumerate(file_entries, 1):
            result += f"{i}. **{entry['filename']}**\n"
        
        result += "\n**To analyze these files with Box AI, simply ask me to:**\n"
        result += "• \"Summarize these files\"\n"
        result += "• \"What are the key points in these documents?\"\n"
        result += "• \"Give me insights from these files\"\n"
        result += "• \"Analyze these documents for me\"\n\n"
        
        result += "**Suggested analysis questions:**\n"
        result += "• \"Summarize the key points in 3 bullet points\"\n"
        result += "• \"What are the main findings?\"\n"
        result += "• \"Extract the compliance requirements\"\n"
        result += "• \"Give me a 2-sentence summary\"\n\n"
        
        result += "💡 **Tip:** Just ask me to analyze the files - I'll handle all the technical details automatically!"
        
        logger.info("✅ File ID extraction completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in file ID extraction: {e}")
        return f"""An error occurred while extracting file IDs: {str(e)}

**What to do:**
1. Try the search again
2. Check if the search returned results
3. Use a simpler search query

**For now, you can manually extract file IDs from the search results and use them with the box_ai_ask tool.**"""

def smart_summarize_search_results(search_results: str, summary_prompt: str = None) -> str:
    """
    Main function for smart file ID extraction from search results.
    Simplified and robust approach.
    
    Args:
        search_results: The output from box_search tool
        summary_prompt: Optional custom prompt (not used in current implementation)
        
    Returns:
        Formatted instructions for using Box AI Ask with extracted file IDs
    """
    try:
        logger.info("🚀 Starting smart file ID extraction...")
        
        # Use the simplified extraction function
        result = extract_file_ids_from_search_results(search_results)
        
        logger.info("✅ Smart file ID extraction completed")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in smart file ID extraction: {e}")
        return f"Error during file ID extraction: {str(e)}" 