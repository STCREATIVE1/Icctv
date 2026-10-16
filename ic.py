import json

def filter_icc_tv_global_events(input_filename, output_filename):
    # JSON file read karein
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Function jo check karega ki item official ICC TV Tournament event hai ya nahi
    def is_icc_tv_global(item):
        for tag in item.get('tags', []):
            extra_data = tag.get('extraData', {})
            series_type = extra_data.get('seriesType', '')
            
            # ICC TV global streams par zyadatar 'Tournament' series type wale matches aate hain
            # Jaise ICC CWC League 2, ECA Women's European Cup, etc.
            if series_type == 'Tournament':
                return True
        return False

    # 'live' aur 'upcoming' lists ko filter karein
    filtered_live = [item for item in data.get('live', []) if is_icc_tv_global(item)]
    filtered_upcoming = [item for item in data.get('upcoming', []) if is_icc_tv_global(item)]

    # Data update karein
    data['live'] = filtered_live
    data['upcoming'] = filtered_upcoming
    data['live_matches'] = len(filtered_live)
    data['upcoming_matches'] = len(filtered_upcoming)
    data['total_matches'] = data['live_matches'] + data['upcoming_matches']
    data['name'] = "ICC TV Global Stream Filtered API"

    # Filtered data ko naye JSON file mein write karein
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Filtering complete! File saved as: {output_filename}")

# Script ko run karne ke liye input file name yahan dein:
if __name__ == "__main__":
    input_file = "icc.json"                 # Apni original JSON file ka naam
    output_file = "icc_tv_global.json"      # Output file ka naam
    filter_icc_tv_global_events(input_file, output_file)
