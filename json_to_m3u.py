import json

def convert_json_to_m3u(json_file_path, output_m3u_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(output_m3u_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write("#Author:- DOCTOR STRANGE\n")
            f.write("#Telegram:- https://t.me/jitendraunatti_github\n")
            f.write(f"#Last Updated:- {data.get('meta', {}).get('generatedAt', '')}\n")
            f.write("# ==========================================\n\n")
            
            # New JSON structure mein data 'items' array ke andar hota hai
            items = data.get("items", [])
            for item in items:
                title = item.get("title", "ICC Video")
                fields = item.get("fields", {})
                
                tvg_id = fields.get("videoId", "")
                video_url = fields.get("mezzanineUrl", "")
                
                if not video_url:
                    continue
                
                thumbnail = item.get("thumbnail", {}).get("thumbnailUrl", "")
                
                # M3U metadata line (#EXTINF)
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{thumbnail}" tvg-lang="English" group-title="ICC Highlights", {title}\n')
                
                # Direct MP4/VOD link
                f.write(f"{video_url}\n\n")
                
        print(f"[+] Successfully converted items to '{output_m3u_path}'!")

    except Exception as e:
        print(f"[!] Error occurred: {e}")

if __name__ == "__main__":
    convert_json_to_m3u("icc_matches_data.json", "playlist.m3u")
