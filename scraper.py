import requests
import os
import json
import re

# GitHub Secrets se login details uthana
EMAIL = os.getenv('ICC_EMAIL')
PASSWORD = os.getenv('ICC_PASSWORD')

def get_icc_data():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.icc-cricket.com/"
    }

    # 1. Login Logic (Basic Auth / Session initialization)
    # Note: ICC login process handle karne ke liye session maintain karna zaroori hai
    login_page = "https://www.icc-cricket.com/icc-tv/login"
    session.get(login_page, headers=headers)

    # 2. Upcoming Events aur Live Data fetch karna
    # ICC ki GraphQL API ya JSON endpoints ka use karein
    api_url = "https://api.icc-cricket.com/video/v1/content?type=LIVE_EVENT"
    
    try:
        response = session.get(api_url, headers=headers)
        data = response.json()
        
        extracted_data = []
        
        # 3. Data Extraction Loop
        for item in data.get('content', []):
            event_info = {
                "title": item.get('title'),
                "status": item.get('status'),
                "mpd_url": item.get('playbackUrl'), # MPD link yahan mil sakta hai
                "image": item.get('thumbnail'),
                "startTime": item.get('startTime')
            }
            extracted_data.append(event_info)
            
        # 4. JSON File mein save karna (Jo GitHub Action commit karega)
        with open('icc_live.json', 'w') as f:
            json.dump(extracted_data, f, indent=4)
        print("Success: Data saved to icc_live.json")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_icc_data()
        
