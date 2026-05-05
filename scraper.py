import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footystream.pk/"
    }

    try:
        # ১. হোমপেজ লোড করা
        target_url = "https://footystream.pk/"
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text

        # ২. শুধুমাত্র ম্যাচের লিঙ্কগুলো খোঁজা (মেনু এবং এসেট লিঙ্ক বাদ দিয়ে)
        # ম্যাচের লিঙ্কগুলো সাধারণত নির্দিষ্ট ফরম্যাটে থাকে, লোগো বা ক্যাটাগরি নয়
        links = re.findall(r'href="(https://footystream\.pk/[^"]+)"', html)
        
        unique_matches = []
        # ফিল্টার লিস্ট: যা যা আমরা চাই না
        exclude_list = [
            "assets", "logo", "icon", "manifest", "css", "js", # ফাইল এসেট
            "american-football", "nba-streams", "f1-streams", "motogp-streams", # মেনু ক্যাটাগরি
            "ufc-streams-free", "rugby-streams", "others", "cricket", "privacy", "dmca"
        ]

        for link in links:
            # যদি লিঙ্কে উপরের কোনো শব্দ না থাকে এবং লিঙ্কটি ডুপ্লিকেট না হয়
            if not any(x in link for x in exclude_list) and link != target_url:
                if link not in unique_matches:
                    unique_matches.append(link)

        print(f"Filtered matches: {len(unique_matches)}")

        for match_url in unique_matches[:12]: # প্রথম ১২টি আসল ম্যাচ
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            try:
                # ৩. ম্যাচের ভেতরে ঢুকে স্ট্রিম খোঁজা
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # m3u8 লিঙ্ক খোঁজা
                stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    playlist += f'#EXTINF:-1 group-title="LIVE NOW", {title}\n{stream.group(1)}\n'
                else:
                    # যদি ম্যাচ শুরু না হয়, তবে শুধু পেজ লিঙ্ক
                    playlist += f'#EXTINF:-1 group-title="UPCOMING", {title}\n{match_url}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Playlist cleanup successful!")

if __name__ == "__main__":
    grab_links()
