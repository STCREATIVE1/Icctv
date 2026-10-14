import json
import time
from datetime import datetime
import requests

# Default Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0",
    "Referer": "https://www.icc-cricket.com/",
    "Origin": "https://www.icc-cricket.com"
}

# 1. ICC listing fetch karne ka function
def get_icc_videos():
    url = "https://dapi.icc-cricket.com/v2/content/en-gb/videos?page=0&pageSize=20&type=Event"
    res = requests.get(url, headers=HEADERS, timeout=15)
    if res.status_code == 200:
        return res.json().get("content", [])
    return []

# 2. Playback / MPD resolve karne ka logic
def resolve_playback(video_id):
    # Dummy fallback agar auth token bypass chahiye ho
    # Real setup me Diva connector endpoint hit hota hai
    playback_data = {
        "Status_code": 302,
        "create_date": datetime.now().strftime("%A, %B %d, %Y, %I:%M:%S %p"),
        "expire_date": "",
        "headers": [
            f"User-Agent: {HEADERS['User-Agent']}",
            f"Referer: {HEADERS['Referer']}",
            f"Origin: {HEADERS['Origin']}"
        ],
        "audioTracks": [{"id": "primary", "displayName": "English"}],
        "is_redirect": True,
        "playbackUrl": f"https://live-d-01-icc-we.akamaized.net/variant/v1blackout/vcg-01-d/DASH_DASH/Live/channel(vcg-01-ch-hd-08)/manifest.mpd?vcfilter={video_id}&",
        "keys": {
            "hex": "39bd302cdeed3710a89fb004d232ab67:9869f804ba18d7e508cbff781829221c",
            "jwk": {
                "keys": [
                    {
                        "kty": "oct",
                        "k": "mGn4BLoY1-UIy_94GCkiHA",
                        "kid": "Ob0wLN7tNxCon7AE0jKrZw"
                    }
                ],
                "type": "temporary"
            }
        }
    }
    return playback_data

# 3. Main Builder function
def build_icc_json():
    raw_videos = get_icc_videos()
    
    live_items = []
    upcoming_items = []

    for item in raw_videos:
        fields = item.get("fields", {})
        status = fields.get("videoStatus", "").lower()
        vid_id = fields.get("videoId")

        if status == "live":
            # Live streams ke liye playback block attach hota hai
            item["playback"] = resolve_playback(vid_id)
            live_items.append(item)
        elif status == "scheduled":
            upcoming_items.append(item)

    final_payload = {
        "Author": "DOCTOR STRANGE",
        "Telegram": "https://t.me/jitendraunatti_github",
        "name": "ICC Live Matches API",
        "last_updated": datetime.now().strftime("%I:%M:%S %p %d-%m-%Y"),
        "total_matches": len(live_items) + len(upcoming_items),
        "live_matches": len(live_items),
        "upcoming_matches": len(upcoming_items),
        "message": {
            "notice": "Headers are dynamic per stream. Please check the 'playback' field for specific 'licence' and 'headers'."
        },
        "app_settings": {
            "PROXY": "ON",
            "REALTIME_CLEARKEY": True,
            "MULTI_CDN": "OFF",
            "Debugging": "ON",
            "SUB_TYPE": "FREEMIUM",
            "RECIVER": "OFF",
            "REALTIME": "OFF",
            "REPLACEMENT": "OFF",
            "ALL_IN_ONE": "ON",
            "SERVER_STATUS": "NORMAL"
        },
        "live": live_items,
        "upcoming": upcoming_items
    }

    with open("icc.json", "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2, ensure_ascii=False)
    
    print(f"Updated icc.json: {len(live_items)} Live, {len(upcoming_items)} Upcoming")

if __name__ == "__main__":
    build_icc_json()
  
