import requests
import re

# যে সাইটগুলো থেকে লিঙ্ক নিতে চাও
targets = [
    {"name": "EPlayHD Live", "url": "https://eplayhd.com/"}
]

def grab_links():
    playlist = "#EXTM3U\n"
    headers = {"User-Agent": "Mozilla/5.0"}

    for target in targets:
        try:
            response = requests.get(target["url"], headers=headers)
            # ম্যাচ পেজ লিঙ্ক খোঁজা
            matches = re.findall(r'href="(https://eplayhd\.com/match/[^"]+)"', response.text)
            
            for match_url in matches[:5]: # প্রথম ৫টি ম্যাচ নিবে
                title = match_url.split('/')[-1].replace('-', ' ').upper()
                sub_res = requests.get(match_url, headers=headers)
                # m3u8 বা ts লিঙ্ক খোঁজা
                stream = re.search(r'"(https?://[^"]+\.(?:m3u8|ts)[^"]*)"', sub_res.text)
                
                if stream:
                    playlist += f'#EXTINF:-1 group-title="Sports Live", {title}\n{stream.group(1)}\n'
        except Exception as e:
            print(f"Error grabbing {target['name']}: {e}")

    with open("playlist.m3u", "w") as f:
        f.write(playlist)

if __name__ == "__main__":
    grab_links()
  
