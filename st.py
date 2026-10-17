import json
import requests

def fetch_icc_tv_matches():
    url = "https://dapi.icc-cricket.com/v2/content/en-gb/videos?workflow=LIVE"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.icc-cricket.com/"
    }
    
    # Netherlands ki public proxy configuration (Auto-fallback ke sath)
    proxies = {
        "http": "http://185.220.101.5:80",
        "https": "http://185.220.101.5:80"
    }
    
    data = None
    
    # Pehle Netherlands proxy ke through try karega
    try:
        print("Trying to fetch data through Netherlands proxy...")
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Successfully fetched via NL proxy!")
    except Exception as e:
        print(f"Proxy connection failed ({e}), falling back to direct connection...")
        # Agar proxy kaam na kare toh direct connection try karega taaki workflow fail na ho
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            print("Successfully fetched via direct connection!")
        except Exception as err:
            print(f"Error fetching data from ICC TV API: {err}")
            return

    # Filter logic (Netherlands ya general global tournament matches ke liye)
    def filter_matches(item):
        title = item.get('title', '').lower()
        slug = item.get('slug', '').lower()
        
        for tag in item.get('tags', []):
            extra_data = tag.get('extraData', {})
            series_name = extra_data.get('seriesName', '').lower()
            team_a = extra_data.get('teamA', '').lower()
            team_b = extra_data.get('teamB', '').lower()
            
            # Agar Netherlands match mein shamil hai
            if 'netherlands' in team_a or 'netherlands' in team_b or 'netherlands' in series_name or 'netherlands' in title:
                return True
            
            # Agar koi official tournament / League match hai
            if extra_data.get('seriesType') == 'Tournament':
                return True
                
        return False

    content_items = data.get('content', [])
    filtered_matches = [item for item in content_items if filter_matches(item)]

    output_data = {
        "name": "ICC TV Scraped Matches API (NL Proxy)",
        "total_matches": len(filtered_matches),
        "matches": filtered_matches
    }

    output_filename = "icc_scraped_matches.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Scraping complete! Saved {len(filtered_matches)} matches to {output_filename}")

if __name__ == "__main__":
    fetch_icc_tv_matches()
  
