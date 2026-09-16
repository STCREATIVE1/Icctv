import requests
import json

def fetch_live_icc_matches():
    # ICC ka general content/video listing endpoint
    api_url = "https://dapi.icc-cricket.com/v2/content/en-gb/videos"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0",
        "Referer": "https://www.icc-cricket.com/",
        "Origin": "https://www.icc-cricket.com",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        print("[*] Checking ICC API for live streams...")
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            # Sirf un items ko filter karo jo LIVE hain
            live_items = []
            for item in items:
                fields = item.get("fields", {})
                workflow = fields.get("workflow", "")
                status = fields.get("videoStatus", "")
                
                # Check agar workflow LIVE hai ya playback data mojood hai
                if workflow == "LIVE" or status == "Live" or "playback" in item:
                    live_items.append(item)
            
            if live_items:
                print(f"[+] Success! Found {len(live_items)} live stream(s).")
                
                # Structured JSON format banana jaisa aapko pasand hai
                output_data = {
                    "Author": "DOCTOR STRANGE",
                    "Telegram": "https://t.me/jitendraunatti_github",
                    "name": "ICC Live Matches API",
                    "total_matches": len(live_items),
                    "live": live_items,
                    "upcoming": []
                }
                
                with open("icc_live_matches.json", "w", encoding="utf-8") as f:
                    json.dump(output_data, f, indent=4)
                print("[+] Saved live matches to 'icc_live_matches.json'")
            else:
                print("[-] Filhal koi live match nahi chal raha hai (Sabhi VOD/Highlights hain).")
                
        else:
            print(f"[-] Failed to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    fetch_live_icc_matches()
