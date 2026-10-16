import json

def filter_icc_tv_global_events(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def is_true_icc_tournament(item):
        for tag in item.get('tags', []):
            extra_data = tag.get('extraData', {})
            series_name = extra_data.get('seriesName', '')
            tour_name = extra_data.get('tourName', '')
            
            # Keywords jo bilkul nahi chahiye (Tri-Series aur Bilateral/Tours)
            exclude_keywords = ['Tri-Series', 'tour of', 'in India', 'in Pakistan', 'in UAE']
            if any(keyword in series_name or keyword in tour_name for keyword in exclude_keywords):
                return False
            
            # Sirf official tournaments / league matches ko allow karein
            if extra_data.get('seriesType') == 'Tournament':
                return True
        return False

    # Filter live and upcoming lists
    filtered_live = [item for item in data.get('live', []) if is_true_icc_tournament(item)]
    filtered_upcoming = [item for item in data.get('upcoming', []) if is_true_icc_tournament(item)]

    # Update metadata
    data['live'] = filtered_live
    data['upcoming'] = filtered_upcoming
    data['live_matches'] = len(filtered_live)
    data['upcoming_matches'] = len(filtered_upcoming)
    data['total_matches'] = data['live_matches'] + data['upcoming_matches']
    data['name'] = "ICC TV Global Stream Filtered API"

    # Save to file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Filtering complete! File saved as: {output_filename}")

if __name__ == "__main__":
    input_file = "icc.json"
    output_file = "icc_tv_global.json"
    filter_icc_tv_global_events(input_file, output_file)
    
