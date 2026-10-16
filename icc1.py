import json
import time
import requests

# Main list endpoint
list_url = (
    "https://dapi.icc-cricket.com/v2/content/en-gb/videos?page=0&pageSize=30"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101"
        " Firefox/157.0"
    ),
    "Referer": "https://www.icc-cricket.com/",
    "Origin": "https://www.icc-cricket.com",
    "Accept": "application/json",
}


def fetch_icc_data():
  print("Step 1: Fetching main video/match list...")
  try:
    response = requests.get(list_url, headers=headers, timeout=15)

    if response.status_code != 200:
      print(f"Failed to fetch list. Status code: {response.status_code}")
      return

    data = response.json()
    items = data.get("content", [])

    print(f"Total items found: {len(items)}\n")
    all_extracted_data = []

    for index, item in enumerate(items, start=1):
      fields = item.get("fields", {})
      title = fields.get("title", "Unknown Title")
      video_status = fields.get("videoStatus", "Unknown")

      # Match ka unique path/slug nikalne ke liye
      path = item.get("path", "")

      print(
          f"[{index}] Match Name: {title} | Status: {video_status} | Slug/Path:"
          f" {path}"
      )

      # Step 2: Agar path available hai, toh uske individual deep link ko hit karo
      if path:
        # Agar path relative hai toh full URL banayein
        if path.startswith("http"):
          detail_url = path
        else:
          detail_url = f"https://dapi.icc-cricket.com/v2/content/en-gb{path if path.startswith('/') else '/' + path}"

        print(f"   -> Fetching deep details from: {detail_url}")

        try:
          detail_res = requests.get(detail_url, headers=headers, timeout=10)
          if detail_res.status_code == 200:
            detail_data = detail_res.json()
            # Yahan aapko us specific match ki saari deep details mil jayengi
            all_extracted_data.append(detail_data)
          else:
            print(f"   -> Failed to fetch detail. Code: {detail_res.status_code}")
        except Exception as e:
          print(f"   -> Error fetching individual detail: {e}")

        # Server par load na pade isliye thoda chhota gap dein
        time.sleep(1)

    # Saara data ek JSON file mein save kar lein
    with open("icc_detailed_matches.json", "w", encoding="utf-8") as f:
      json.dump(all_extracted_data, f, indent=2, ensure_ascii=False)

    print(
        "\nSuccessfully fetched all matches and saved to"
        " 'icc_detailed_matches.json'!"
    )

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  fetch_icc_data()
    
