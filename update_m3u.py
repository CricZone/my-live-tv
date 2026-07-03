import re
import requests

def get_m3u8(youtube_url):
    video_id = None
    # Extract video ID using regex from different types of youtube URLs
    match = re.search(r'(?:live\/|v=|\/v\/|youtu\.be\/|\/embed\/)([\w-]+)', youtube_url)
    if match:
        video_id = match.group(1)
    
    if video_id:
        # YouTube directly provides HLS streams via this endpoint pattern
        return f"https://youtube.com/api/v1/live/manifest/video_id/{video_id}/format/m3u8"
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
        m3u8_url = get_m3u8(line)
        if m3u8_url and current_info:
            m3u_content += f"{current_info}\n{m3u8_url}\n"
            current_info = ""

with open("live_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
print("M3U Playlist Updated Successfully!")
