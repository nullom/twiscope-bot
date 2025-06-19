# Priority scoring for RSS entries
from typing import List, Dict, Any

# Security-related keywords and their weight scores
SECURITY_KEYWORDS = {
    "0-day": 10,
    "exploit": 9,
    "breach": 8,
    "ransomware": 7,
    "critical": 6,
    "patch": 5,
    "vulnerability": 5,
    "malware": 4,
    "CVE": 3,
    "security": 2,
}

def calculate_keyword_score(text: str, keywords: Dict[str, int]) -> int:
    """Calculate score for a text based on keyword presence."""
    score = 0
    text_lower = text.lower()
    for keyword, weight in keywords.items():
        if keyword.lower() in text_lower:
            score += weight
    return score

def calculate_entry_score(entry: Dict[str, Any]) -> int:
    """Calculate total score for a single entry."""
    title = entry.get("title", "")
    summary = entry.get("summary", "")
    title_score = calculate_keyword_score(title, SECURITY_KEYWORDS) * 2  # Double weight for title
    summary_score = calculate_keyword_score(summary, SECURITY_KEYWORDS)
    return title_score + summary_score

def sort_entries_by_score(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort entries by score in descending order."""
    return sorted(entries, key=lambda x: x["score"], reverse=True)

def score_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Score RSS entries by security keywords."""
    for entry in entries:
        entry["score"] = calculate_entry_score(entry)
    return sort_entries_by_score(entries)
