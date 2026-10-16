from datetime import datetime, timedelta
import json
import requests

from_date = datetime.now().strftime("%Y%m%d")
to_date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")

api_url = (
    "https://assets-icc.sportz.io/cricket/v1/schedule?"
    "client_id=tPZJbRgIub3Vua93%2FDWtyQ%3D%3D&feed_format=json&lang=en&"
    "is_deleted=false&pagination=true&page_number=1&page_size=50&"
    f"from_date={from_date}&to_date={to_date}&"
    "is_upcoming=true&is_live=true&is_recent=false"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.icc-cricket.com/",
    "Origin": "https://www.icc-cricket.com",
}


def generate_icc_json():
  print("Fetching schedule from ICC API...")
  try:
    res = requests.get(api_url, headers=headers, timeout=15)
    if res.status_code != 200:
      print(f"Failed to fetch API: HTTP {res.status_code}")
      return

    data = res.json()
    matches = data.get("data", {}).get("matches", [])

    live_items = []
    upcoming_items = []

    for match in matches:
      is_live = match.get("live", False)
      is_upcoming = match.get("upcoming", False)
      live_coverage = match.get("live_coverage", False)

      # Sirf wahi match lenge jinka ICC-TV par live coverage ya streaming available ho
      if not live_coverage and not is_live:
        continue

      match_id = str(match.get("match_id", ""))
      team_a = match.get("teama", "Team A")
      team_b = match.get("teamb", "Team B")
      series_name = match.get("series_name", "ICC Tournament")
      series_id = str(match.get("series_id", ""))

      slug = f"{team_a.lower()}-v-{team_b.lower()}-1st-innings".replace(
          " ", "-"
      )
      self_url = f"https://dapi.icc-cricket.com/v2/content/en-gb/videos/{slug}"

      item_structure = {
          "type": "customentity",
          "_translationId": f"trans-{match_id}",
          "_entityId": f"entity-{match_id}",
          "selfUrl": self_url,
          "slug": slug,
          "title": f"{team_a} v {team_b} (1st Innings)",
          "tags": [
              {
                  "selfUrl": f"https://dapi.icc-cricket.com/v2/content/en-gb/tags/tournament-{series_id}",
                  "title": series_name,
                  "slug": f"tournament-{series_id}",
                  "extraData": {
                      "tournamentId": series_id,
                      "competitionType": match.get("comp_type", "ODI"),
                      "competitionTypeId": match.get("comp_type_id", "2"),
                  },
              },
              {
                  "selfUrl": f"https://dapi.icc-cricket.com/v2/content/en-gb/tags/match-{match_id}",
                  "title": (
                      f"{team_a} vs {team_b} - {match.get('match_number', '')} -"
                      f" {match.get('match_date_local', '')}"
                  ),
                  "slug": f"match-{match_id}",
                  "extraData": {
                      "matchId": match_id,
                      "teamA": team_a,
                      "teamB": team_b,
                      "matchDateLocal": match.get("match_date_local", ""),
                      "matchType": match.get("match_type", ""),
                      "seriesName": series_name,
                  },
              },
          ],
          "fields": {
              "videoId": f"vid-{match_id}",
              "workflow": "LIVE",
              "videoStatus": "Live" if is_live else "Scheduled",
              "v_has_data": True,
              "scheduledStartTime": match.get("start_date", ""),
              "offer": "Registered",
              "type": "Event",
              "countryRestrictions": {
                  "listType": "blacklist",
                  "countries": ["IN"],
              },
          },
          "thumbnail": {
              "title": f"{team_a} vs {team_b}",
              "templateUrl": (
                  "https://images.icc-cricket.com/image/upload/{formatInstructions}/prd/default"
              ),
              "thumbnailUrl": (
                  "https://images.icc-cricket.com/image/upload/t_ratio16_9-size20/prd/default"
              ),
          },
      }

      if is_live:
        live_items.append(item_structure)
      elif is_upcoming:
        upcoming_items.append(item_structure)

    final_payload = {
        "Author": "DOCTOR STRANGE",
        "Telegram": "https://t.me/jitendraunatti_github",
        "name": "ICC Live Matches API",
        "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M"),
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
        f"Successfully generated icc.json with {len(live_items)} Live and"
        f" {len(upcoming_items)} Streaming-supported Upcoming matches!"
    )

  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  generate_icc_json()
    
