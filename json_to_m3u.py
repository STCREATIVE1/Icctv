import json

def convert_json_to_m3u(json_file_path, output_m3u_path):
    try:
        # JSON file load karein
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # M3U file write karna shuru karein
        with open(output_m3u_path, 'w', encoding='utf-8') as f:
            # Header comments add karein
            f.write("#EXTM3U\n")
            f.write(f"#Author:- {data.get('Author', 'DOCTOR STRANGE')}\n")
            f.write(f"#Telegram:- {data.get('Telegram', '')}\n")
            f.write(f"#Last Updated:- {data.get('last_updated', '')}\n")
            f.write("# ==========================================\n\n")
            
            # Live matches process karein
            live_matches = data.get("live", [])
            for match in live_matches:
                # Tags se title aur ID nikalna
                tags = match.get("tags", [])
                match_title = "Live Match"
                tvg_id = match.get("fields", {}).get("videoId", "")
                
                for tag in tags:
                    if tag.get("externalTagType") == "match":
                        match_title = tag.get("title", "Live Match")
                        break
                
                # Thumbnail aur playback details
                thumbnail = match.get("thumbnail", {}).get("thumbnailUrl", "")
                playback = match.get("playback", {})
                playback_url = playback.get("playbackUrl", "")
                
                if not playback_url:
                    continue
                
                keys = playback.get("keys", {})
                jwk_keys = keys.get("jwk", {})
                
                # M3U metadata line (#EXTINF)
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{thumbnail}" tvg-lang="English" group-title="Cricket",English | {match_title}\n')
                
                # Kodi properties agar keys available hain
                if jwk_keys:
                    f.write("#KODIPROP:inputstream=inputstream.adaptive\n")
                    f.write("#KODIPROP:inputstream.adaptive.manifest_type=mpd\n")
                    f.write("#KODIPROP:inputstream.adaptive.license_type=com.clearkey.alpha\n")
                    # JSON keys ko compact format mein convert karna Kodi ke liye
                    keys_json_str = json.dumps(jwk_keys, separators=(',', ':'))
                    f.write(f"#KODIPROP:inputstream.adaptive.license_key={keys_json_str}\n")
                
                # VLC options aur HTTP headers
                f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0\n")
                f.write("#EXTVLCOPT:http-referrer=https://www.icc-cricket.com/\n")
                f.write("#EXTVLCOPT:http-origin=https://www.icc-cricket.com\n")
                f.write('#EXTHTTP:{"referer":"https://www.icc-cricket.com/","origin":"https://www.icc-cricket.com"}\n')
                
                # Final Stream URL
                f.write(f"{playback_url}\n\n")
                
        print(f"[+] Successfully converted '{json_file_path}' to '{output_m3u_path}'!")

    except Exception as e:
        print(f"[!] Error occurred: {e}")

if __name__ == "__main__":
    # Apni JSON file ka naam yahan dein (jaise jo scraper se save hui ho)
    convert_json_to_m3u("icc_matches_data.json", "playlist.m3u")
