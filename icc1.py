import json
import time
from datetime import datetime
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.icc-cricket.com/",
    "Origin": "https://www.icc-cricket.com",
    "Accept": "application/json, text/plain, */*"
}

def get_icc_videos():
    # Primary API endpoint for live videos and events
    endpoints = [
        "https://dapi.icc-cricket.com/v2/content/en-gb/videos?page=0&pageSize=50",
        "https://dapi.icc-cricket.com/v2/content/en-gb/events?page=0&pageSize=50"
    ]
    
    all_content = []
    for url in endpoints:
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code == 200:
                data = res.json()
                items = data.get("content", []) or data.get("items", [])
                if isinstance(items, list):
                    all_content.extend(items)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    # Deduplicate by _entityId or slug
    seen_ids = set()
    unique_items = []
    for item in all_content:
        ent_id = item.get("_entityId") or item.get("slug")
        if ent_id and ent_id not in seen_ids:
            seen_ids.add(ent_id)
            unique_items.append(item)
            
    return unique_items

def resolve_playback(video_id):
    return {
        "Status_code": 302,
        "create_date": datetime.now().strftime("%A, %B %d, %Y, %I:%M:%S %p"),
        "expire_date": "",
        "headers": [
            f"User-Agent: {HEADERS['User-Agent']}",
            "Referer: https://www.icc-cricket.com/",
            "Origin: https://www.icc-cricket.com"
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

def build_icc_json():
    raw_videos = get_icc_videos()
    live_items = []
    upcoming_items = []

    for item in raw_videos:
        fields = item.get("fields", {})
        status = str(fields.get("videoStatus", "")).strip().lower()
        workflow = str(fields.get("workflow", "")).strip().lower()
        vid_id = fields.get("videoId")

        # Live condition: videoStatus == live or workflow == live
        if status == "live" or workflow == "live":
            item["playback"] = resolve_playback(vid_id)
            live_items.append(item)
        elif status == "scheduled" or workflow == "scheduled":
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
    
