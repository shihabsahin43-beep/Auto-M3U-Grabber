import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    # এই সাইটটি ভিজিট করার জন্য হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "http://iptvidn.com/"
    }

    try:
        # ১. সরাসরি মেইন পেজটি লোড করা
        target_url = "http://iptvidn.com/"
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text

        # ২. m3u8 বা প্লেয়ারের লিঙ্কগুলো সরাসরি খোঁজা
        # এই সাইটটি অনেক সময় পেজেই সরাসরি m3u8 লিঙ্ক দিয়ে দেয়
        direct_streams = re.findall(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', html)
        
        # ৩. যদি সরাসরি না পায়, তবে ভেতরের পোস্ট লিঙ্কগুলো খোঁজা
        post_links = re.findall(r'href="(http://iptvidn\.com/[^"]+)"', html)
        unique_posts = list(dict.fromkeys(post_links))

        # সরাসরি পাওয়া লিঙ্কগুলো আগে যোগ করা
        for stream in list(set(direct_streams))[:10]:
            playlist += f'#EXTINF:-1 group-title="IDN Direct", CHANNEL-{direct_streams.index(stream)}\n{stream}\n'

        # পোস্টের ভেতরের লিঙ্কগুলো খোঁজা
        for post_url in unique_posts[:5]:
            if "category" in post_url or post_url == target_url:
                continue
            
            title = post_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            try:
                sub_res = requests.get(post_url, headers=headers, timeout=10)
                sub_stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_res.text)
                
                if sub_stream:
                    playlist += f'#EXTINF:-1 group-title="IDN Post", {title}\n{sub_stream.group(1)}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("IDN Playlist updated!")

if __name__ == "__main__":
    grab_links()
