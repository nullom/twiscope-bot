# twiscope/priority_scoring.py
# Assigns priority scores to RSS entries based on security-related keywords

from typing import List, Dict, Any

# Security-related keywords and their weight scores
SECURITY_KEYWORDS = {
    "0-day": 10,        # Critical zero-day vulnerabilities
    "exploit": 9,       # Active exploitation
    "breach": 8,        # Security breaches
    "ransomware": 7,    # Ransomware attacks
    "critical": 6,      # Critical security issues
    "patch": 5,         # Security patches
    "vulnerability": 5, # General vulnerabilities
    "malware": 4,       # Malware threats
    "CVE": 3,          # Common Vulnerabilities and Exposures
    "security": 2,      # General security news
}

def score_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Score RSS entries based on security-related keywords in their title and summary.
    
    Args:
        entries (List[Dict[str, Any]]): List of RSS entries, each containing 'title' and 'summary'
        
    Returns:
        List[Dict[str, Any]]: The same entries with added 'score' field, sorted by score
        
    Example entry format:
    {
        'title': 'Article Title',
        'summary': 'Article Summary',
        'link': 'https://example.com',
        'score': 15  # Added by this function
    }
    """
    for entry in entries:
        score = 0
        title = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()

        # Calculate score based on keyword presence
        for keyword, weight in SECURITY_KEYWORDS.items():
            keyword_lower = keyword.lower()
            if keyword_lower in title:
                score += weight * 2  # Double weight for keywords in title
            if keyword_lower in summary:
                score += weight

        entry["score"] = score

    # Sort entries by score (highest first)
    entries.sort(key=lambda x: x["score"], reverse=True)
    return entries
