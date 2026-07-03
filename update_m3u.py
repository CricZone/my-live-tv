import os
import re
import subprocess
import json

def get_m3u8(youtube_url):
    try:
        # ভিডিও আইডি খুঁজে বের করা
        match = re.search(r'(?:live\/|v=|\/v\/|youtu\.be\/|\/embed\/)([\w-]+)', youtube_url)
        video_id = match.group(1) if match else None
        
        if video_id:
            full_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # yt-dlp কে ব্রাউজারের ছদ্মবেশ ধারণ করতে বাধ্য করা (ইউজার এজেন্ট দিয়ে)
            # এটি ইউটিউবের ব্লকিং মেকানিজমকে সফলভাবে বাইপাস করে
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--force-overwrites',
                '--no-warnings',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                full_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            video_data = json.loads(result.stdout)
            
            # ডাটা থেকে সরাসরি লাইভ m3u8 ম্যানিফেস্ট লিংক বের করা
            if 'url' in video_data and '.m3u8' in video_data['url']:
                return video_data['url']
            elif 'formats' in video_data:
                for f in video_data['formats']:
                    if f.get('protocol') == 'm3u8_native' or '.m3u8' in f.get('url', ''):
                        return f['url']
    except Exception as e:
        print(f"Error extracting link for {youtube_url}: {e}")
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
        print(f"Extracting live stream for: {line}")
        m3u8_url = get_m3u8(line)
        if m3u8_url and current_info:
            m3u_content += f"{current_info}\n{m3u8_url}\n"
            current_info = ""

with open("live_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
print("Congratulation! Your personal M3U Playlist Updated Successfully!")
