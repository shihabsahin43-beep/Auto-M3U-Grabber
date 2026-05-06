import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://eplayhd.com/"
    }

    try:
        response = requests.get("https://eplayhd.com/", headers=headers, timeout=15)
        html_content = response.text
        matches = re.findall(r'href="(https://eplayhd\.com/[^"]+)"', html_content)
        unique_matches = list(dict.fromkeys(matches))

        for match_url in unique_matches:
            if any(x in match_url for x in ["privacy", "contact", "dmca", "about"]):
                continue
                
            raw_title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            try:
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # .m3u8 অথবা .ts উভয় লিঙ্কই খোঁজা হচ্ছে
                stream = re.search(r'[\'"](https?://[^\'"]+\.(?:m3u8|ts)[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    stream_url = stream.group(1)
                    
                    # যদি লিঙ্কটি .ts হয়, তবে সেটিকে সরাসরি প্লে করার জন্য ক্যাটাগরি করা
                    if stream_url.endswith(".ts"):
                        playlist += f'#EXTINF:-1 group-title="TS STREAMS", {raw_title}\n{stream_url}\n'
                    else:
                        playlist += f'#EXTINF:-1 group-title="LIVE SPORTS", {raw_title}\n{stream_url}\n'
                else:
                    playlist += f'#EXTINF:-1 group-title="WEB LINKS", {raw_title}\n{match_url}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Playlist with .ts support updated!")

if __name__ == "__main__":
    grab_links()
