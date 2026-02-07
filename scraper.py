import requests
import json
import os

# GitHub Secrets se credentials lena
EMAIL = os.getenv('ICC_EMAIL')
PASSWORD = os.getenv('ICC_PASSWORD')

def get_icc_session():
    session = requests.Session()
    
    # 1. Login Endpoint (ICC aksar Gigya ya Auth0 use karta hai)
    # Note: Ye URL aapko Network tab mein 'login' ya 'auth' search karke verify karni hogi
    login_url = "https://api.icc-cricket.com/auth/login" 
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json"
    }

    try:
        response = session.post(login_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Login Successful!")
            return session
        else:
            print(f"Login Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_live_links(session):
    # Live matches aur MPD links fetch karne ka logic
    tv_url = "https://www.icc-cricket.com/icc-tv"
    # Yahan hum ICC ki internal API use karenge jo live video metadata deti hai
    api_url = "https://api.icc-cricket.com/video/live/manifests" 
    
    if session:
        response = session.get(api_url)
        data = response.json()
        
        # Data ko JSON file mein save karna taaki GitHub use commit kar sake
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Data updated in data.json")

if __name__ == "__main__":
    icc_session = get_icc_session()
    fetch_live_links(icc_session)
  
