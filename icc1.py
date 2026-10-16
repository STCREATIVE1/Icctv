from datetime import datetime
import json
import requests

EMAIL = "Desiminecraftfacts@gmail.com"
PASSWORD = "KnEmnBX4PS4A-uP"

BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.icc-cricket.com/",
    "Origin": "https://www.icc-cricket.com",
    "Accept": "application/json, text/plain, */*",
}

session = requests.Session()
session.headers.update(BASE_HEADERS)


def login():
  login_url = "https://identity.icc-cricket.com/api/v1/auth/login"
  payload = {"email": EMAIL, "password": PASSWORD}
  try:
    res = session.post(login_url, json=payload, timeout=15)

    if res.status_code == 200:
      try:
        data = res.json()
        token = data.get("access_token") or data.get("token")
        if token:
          session.headers.update({"Authorization": f"Bearer {token}"})
          print("Login successful, token updated.")
          return token
      except json.JSONDecodeError:
        print("Login failed: Response is not valid JSON (Possible WAF block).")
    else:
      print(f"Login failed: HTTP {res.status_code} - {res.text[:150]}")

  except Exception as e:
    print(f"Login request error: {e}")
  return None


def get_live_events():
  url = "https://dapi.icc-cricket.com/v2/content/en-gb/videos?page=0&pageSize=30"
  try:
    res = session.get(url, timeout=15)
    if res.status_code == 200:
      try:
        data = res.json()
        return data.get("content", []) or data.get("items", [])
      except json.JSONDecodeError:
        print(
            "Error fetching matches: API returned non-JSON response (Blocked"
            " or 400 Error)."
        )
    else:
      print(f"Failed to fetch matches: HTTP {res.status_code}")
  except Exception as e:
    print(f"Error fetching matches: {e}")
  return []


def resolve_playback(video_id):
  return {
      "Status_code": 302,
      "create_date": datetime.now().strftime("%A, %B %d, %Y, %I:%M:%S %p"),
      "expire_date": "",
      "headers": [
          f"User-Agent: {BASE_HEADERS['User-Agent']}",
          "Referer: https://www.icc-cricket.com/",
          "Origin: https://www.icc-cricket.com",
      ],
      "audioTracks": [{"id": "primary", "displayName": "English"}],
      "is_redirect": True,
      "playbackUrl": (
          "https://live-d-01-icc-we.akamaized.net/variant/v1blackout/vcg-01-d/DASH_DASH/Live/channel(vcg-01-ch-hd-08)/manifest.mpd?vcfilter="
          f"{video_id}&"
      ),
      "keys": {
          "hex": (
              "39bd302cdeed3710a89fb004d232ab67:9869f804ba18d7e508cbff781829221c"
          ),
          "jwk": {
              "keys": [{
                  "kty": "oct",
                  "k": "mGn4BLoY1-UIy_94GCkiHA",
                  "kid": "Ob0wLN7tNxCon7AE0jKrZw",
              }],
              "type": "temporary",
          },
      },
  }


def main():
  print("Starting authentication...")
  login()

  print("Fetching live events...")
  raw_content = get_live_events()

  if not raw_content:
    print(
        "No content retrieved. Exiting without overwriting icc.json with empty"
        " data."
    )
    return

  live_items = []
  upcoming_items = []

  for item in raw_content:
    fields = item.get("fields", {})
    status = str(fields.get("videoStatus", "")).strip().lower()
    workflow = str(fields.get("workflow", "")).strip().lower()
    vid_id = fields.get("videoId")

    if status == "live" or workflow == "live":
      if vid_id:
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
          "notice": (
              "Headers are dynamic per stream. Please check the 'playback'"
              " field for specific 'licence' and 'headers'."
          )
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
          "SERVER_STATUS": "NORMAL",
      },
      "live": live_items,
      "upcoming": upcoming_items,
  }

  with open("icc.json", "w", encoding="utf-8") as f:
    json.dump(final_payload, f, indent=2, ensure_ascii=False)

  print(
      f"Successfully updated icc.json: {len(live_items)} Live,"
      f" {len(upcoming_items)} Upcoming"
  )


if __name__ == "__main__":
  main()
    
