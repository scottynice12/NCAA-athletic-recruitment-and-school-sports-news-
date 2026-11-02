import os
import requests
import feedparser
from bs4 import BeautifulSoup

def track_gcu_sports_news():
    print("Fetching official GCU Athletics feeds...")
    # Official GCU sports news RSS feed
    feed_url = "https://gculopes.com" # Men's Basketball example
    feed = feedparser.parse(feed_url)
    
    updates = []
    for entry in feed.entries[:5]: # Grab the 5 most recent articles
        updates.append({
            "title": entry.title,
            "link": entry.link,
            "type": "Official School News"
        })
    return updates

def scrape_recruitment_portal():
    print("Scanning sports media for GCU transfer/recruit updates...")
    updates = []
    
    # Target a high-frequency sports news aggregator or portal feed
    url = "https://www.foxsports.com/college-basketball/grand-canyon-antelopes-team"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape headlines looking for transfer news, commits, or roster movement
            for item in soup.find_all(['h2', 'h3', 'a']):
                text = item.get_text().strip()
                link = item.get('href')
                
                # Filter for recruitment keywords
                if any(word in text.lower() for word in ["transfer", "commits", "recruit", "portal", "signs"]):
                    if link and link.startswith('http'):
                        updates.append({
                            "title": text,
                            "link": link,
                            "type": "Recruitment/Portal Alert"
                        })
    except Exception as e:
        print(f"Error checking sports portal: {e}")
        
    return updates

def main():
    sports_intel = []
    sports_intel.extend(track_gcu_sports_news())
    sports_intel.extend(scrape_recruitment_portal())
    
    if not sports_intel:
        print("No new sports or recruitment updates found today.")
        return

    # De-duplicate results
    seen = set()
    unique_intel = []
    for item in sports_intel:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_intel.append(item)

    # Format the report
    report = "=== GCU ATHLETICS & RECRUITMENT REPORT ===\n\n"
    for idx, item in enumerate(unique_intel, 1):
        report += f"{idx}. [{item['type']}] {item['title']}\n   URL: {item['link']}\n\n"
        
    print(report)
    
    # Save the output for GitHub Actions to commit
    with open("sports_report.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
