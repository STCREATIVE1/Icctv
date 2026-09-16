import requests
import json

def fetch_icc_matches():
    # ICC ka general content/video listing endpoint jahan se live aur upcoming matches ki list milti hai
    api_url = "https://dapi.icc-cricket.com/v2/content/en-gb/videos"
    
    # Headers jo server validation ke liye zaroori hain
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0",
        "Referer": "https://www.icc-cricket.com/",
        "Origin": "https://www.icc-cricket.com",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        print("[*] Fetching matches data from ICC API...")
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("[+] Data fetched successfully!\n")
            
            # Yahan aap items ko filter kar sakte hain ya poora JSON save kar sakte hain
            # Jaise live matches ya upcoming matches check karna
            
            # Example ke taur par JSON file mein save kar rahe hain taaki aap poora structure dekh sakein
            with open("icc_matches_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print("[+] Saved all data to 'icc_matches_data.json'")
            
            return data
        else:
            print(f"[-] Failed to fetch data. Status Code: {response.status_code}")
            return None

    except Exception as e:
        print(f"[!] An error occurred: {e}")
        return None

if __name__ == "__main__":
    fetch_icc_matches()
