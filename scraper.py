import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    # সকার স্ট্রিম পেজ থেকে লিঙ্ক নেওয়ার জন্য উন্নত হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footystream.pk/"
    }

    try:
        # ১. সরাসরি সকার স্ট্রিম পেজটি লোড করা
        target_url = "https://footystream.pk/soccer-streams"
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text

        # ২. ম্যাচের কার্ড বা লিঙ্কগুলো খুঁজে বের করা
        # এখানে সাধারণত 'href' এর ভেতর ম্যাচের নাম থাকে
        matches = re.findall(r'href="(https://footystream\.pk/[^"]+)"', html)
        
        # ডুপ্লিকেট লিঙ্ক সরানো
        unique_matches = list(dict.fromkeys(matches))
        
        count = 0
        for match_url in unique_matches:
            # শুধু আসল ম্যাচের লিঙ্কগুলো নিবে (অপ্রাসঙ্গিক লিঙ্ক বাদ দিবে)
            if "/soccer-streams" in match_url or count > 8:
                continue
                
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            try:
                # ৩. ম্যাচের ভেতরের পেজে গিয়ে m3u8 বা আইফ্রেম সোর্স খোঁজা
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # এই সাইটগুলো অনেক সময় জাভাস্ক্রিপ্টে লিঙ্ক লুকিয়ে রাখে, তাই আমরা m3u8 খুঁজি
                stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    stream_url = stream.group(1)
                    playlist += f'#EXTINF:-1 group-title="Soccer Live", {title}\n{stream_url}\n'
                else:
                    # যদি সরাসরি লিঙ্ক না পায়, তবে অন্তত পেজ লিঙ্কটি দিচ্ছি
                    playlist += f'#EXTINF:-1 group-title="Soccer Web", {title} (WATCH ON WEB)\n{match_url}\n'
                
                count += 1
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    # ফাইনাল প্লেলিস্ট সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Soccer Playlist updated successfully!")

if __name__ == "__main__":
    grab_links()
