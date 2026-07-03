import os
import requests

def get_bioscope_m3u8(channel_id):
    # বায়োস্কোপের সিকিউরিটি বাইপাস করার জন্য অফিশিয়াল অ্যাপের হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Referer": "https://www.bioscopelive.com/",
        "Origin": "https://www.bioscopelive.com"
    }
    
    try:
        # বায়োস্কোপের লাইভ চ্যানেল এপিআই এন্ডপয়েন্ট
        api_url = f"https://api.bioscopelive.com/api/v1/channel/url/{channel_id}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # রেসপন্স ডাটা থেকে ডিরেক্ট m3u8 স্ট্রিম লিঙ্ক বের করা
            if 'data' in data and 'url' in data['data']:
                return data['data']['url']
    except Exception as e:
        print(f"Error fetching Bioscope link for {channel_id}: {e}")
    return None

try:
    with open("bioscope_channels.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []

m3u_content = "#EXTM3U\n"
current_info = ""

for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("#EXTINF"):
        current_info = line
    else:
        print(f"Fetching Bioscope Link for: {current_info.split(',')[-1]}")
        m3u8_url = get_bioscope_m3u8(line)
        if m3u8_url and current_info:
            m3u_content += f"{current_info}\n{m3u8_url}\n"
            current_info = ""

with open("live_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
print("Bioscope M3U Playlist Generated Successfully!")
