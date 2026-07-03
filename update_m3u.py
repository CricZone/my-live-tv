import os
import re
import subprocess

def get_m3u8(youtube_url):
    try:
        # Extract video ID
        match = re.search(r'(?:live\/|v=|\/v\/|youtu\.be\/|\/embed\/)([\w-]+)', youtube_url)
        video_id = match.group(1) if match else None
        
        if video_id:
            # Direct backup stream fetcher fallback using yt-dlp tool via subprocess
            result = subprocess.run(
                ['yt-dlp', '-g', f'https://www.youtube.com/watch?v={video_id}'],
                capture_output=True, text=True, check=True
            )
            urls = result.stdout.strip().split('\n')
            # Return the first m3u8 stream link found
            for url in urls:
                if '.m3u8' in url:
                    return url
    except Exception as e:
        print(f"Error fetching for {youtube_url}: {e}")
    return None

try:
    with open("youtube_links.txt", "r", encoding="utf-8") as f:
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
    elif "youtube.com" in line or "youtu.be" in line:
        print(f"Processing: {line}")
        m3u8_url = get_m3u8(line)
        if m3u8_url and current_info:
            m3u_content += f"{current_info}\n{m3u8_url}\n"
            current_info = ""

with open("live_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
print("M3U Playlist Re-Generated Successfully with yt-dlp!")
