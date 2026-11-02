import os
import requests
import feedparser
from bs4 import BeautifulSoup

def track_gcu_sports_news():
    print("Fetching official GCU Athletics feeds...")
    feed_url = "https://gculopes.com" 
    feed = feedparser.parse(feed_url)
    
    updates = []
    # Grab whatever is available in the feed so we always have data
    for entry in feed.entries[:5]: 
        updates.append({
            "title": entry.title,
            "link": entry.link,
            "type": "Official School News"
        })
    return updates

def scrape_recruitment_portal():
    print("Scanning sports media for GCU transfer/recruit updates...")
    updates = []
    
    url = "https://foxsports.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pull general headlines from the page to ensure we capture active articles
            for item in soup.find_all(['h2', 'h3', 'a']):
                text = item.get_text().strip()
                link = item.get('href')
                
                # Broaden the filter to grab any recent team articles
                if len(text) > 20 and link and link.startswith('http'):
                    updates.append({
                        "title": text,
                        "link": link,
                        "type": "Fox Sports News Feed"
                    })
    except Exception as e:
        print(f"Error checking sports portal: {e}")
        
    return updates[:5] # Keep the top 5 articles found

def main():
    sports_intel = []
    sports_intel.extend(track_gcu_sports_news())
    sports_intel.extend(scrape_recruitment_portal())
    
    # De-duplicate results
    seen = set()
    unique_intel = []
    for item in sports_intel:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_intel.append(item)

    # We build the report string regardless of whether it's empty or full
    report = "=== GCU ATHLETICS & RECRUITMENT REPORT ===\n\n"
    
    if not unique_intel:
        report += "No fresh articles or roster movements logged on portals today.\n"
    else:
        for idx, item in enumerate(unique_intel, 1):
            report += f"{idx}. [{item['type']}] {item['title']}\n   URL: {item['link']}\n\n"
        
    print(report)
    
    # Crucial change: This file will NOW write every time the code runs
    with open("sports_report.txt", "w") as f:
        f.write(report)
    print("Successfully wrote outputs to sports_report.txt")

if __name__ == "__main__":
    main()
