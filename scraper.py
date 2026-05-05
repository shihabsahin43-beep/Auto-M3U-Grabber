import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    # ফুটস্ট্রিম সাইটটি ভিজিট করার জন্য হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footystream.pk/"
    }

    try:
        # ১. হোমপেজ থেকে লাইভ ইভেন্ট বা চ্যানেলের লিস্ট আনা
        response = requests.get("https://footystream.pk/", headers=headers, timeout=15)
        html = response.text

        # ২. ম্যাচের লিঙ্ক বা চ্যানেল লিঙ্ক খুঁজে বের করা
        # এই সাইটটি সাধারণত 'live-stream' বা 'channel' স্লাগ ব্যবহার করে
        matches = re.findall(r'href="(https://footystream\.pk/[^"]+)"', html)
        
        # ডুপ্লিকেট সরানো এবং অপ্রাসঙ্গিক লিঙ্ক (যেমন privacy policy) বাদ দেওয়া
        unique_matches = []
        for link in matches:
            if any(x in link for x in ['channel', 'stream', 'live']) and link not in unique_matches:
                unique_matches.append(link)

        for match_url in unique_matches[:8]: # প্রথম ৮টি লিঙ্ক চেক করবে
            # টাইটেল তৈরি করা (URL থেকে নাম নিয়ে)
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            # ৩. ভেতরের পেজে গিয়ে m3u8 বা iframe সোর্স খোঁজা
            try:
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # m3u8 লিঙ্ক খোঁজার চেষ্টা
                stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    stream_url = stream.group(1)
                    playlist += f'#EXTINF:-1 group-title="FootyStream Live", {title}\n{stream_url}\n'
                else:
                    # যদি সরাসরি m3u8 না পায়, তবে অন্তত ওই পেজের লিঙ্কটি দিচ্ছি যাতে আপনি অ্যাপে ট্রাই করতে পারেন
                    playlist += f'#EXTINF:-1 group-title="Web Streams", {title}\n{match_url}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("FootyStream Playlist updated!")

if __name__ == "__main__":
    grab_links()
