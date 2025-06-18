# twiscope/priority_scoring.py
# Assigns a basic priority score to each RSS entry based on keywords

def score_entries(entries):
    keywords = {
        "0-day": 10,
        "exploit": 9,
        "breach": 8,
        "ransomware": 7,
        "critical": 6,
        "patch": 5,
        "vulnerability": 5,
        "malware": 4,
        "CVE": 3
    }

    for entry in entries:
        score = 0
        title = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()

        for keyword, weight in keywords.items():
            if keyword in title:
                score += weight
            if keyword in summary:
                score += weight

        entry["score"] = score

    # Optional: sort entries by score (descending)
    entries.sort(key=lambda x: x["score"], reverse=True)
    return entries
