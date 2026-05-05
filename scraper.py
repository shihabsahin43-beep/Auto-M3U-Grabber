import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footystream.pk/"
    }

    try:
        # ১. সকার স্ট্রিম পেজটি লোড করা
        target_url = "https://footystream.pk/soccer-streams"
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text

        # ২. স্ক্রিনশটে দেখা ম্যাচের ব্লকগুলো খুঁজে বের করা
        # প্রতিটি ম্যাচের জন্য তারা সাধারণত নির্দিষ্ট ক্লাস বা স্লাগ ব্যবহার করে
        matches = re.findall(r'href="(https://footystream\.pk/[^"]+)"', html)
        
        unique_matches = []
        # অপ্রাসঙ্গিক লিঙ্কগুলো ফিল্টার করা
        for link in matches:
            if any(x in link for x in ["soccer-streams", "privacy", "contact", "dmca"]):
                continue
            if link not in unique_matches:
                unique_matches.append(link)

        print(f"Found {len(unique_matches)} potential match links.")

        for match_url in unique_matches[:10]:
            # টাইটেল সুন্দর করা (যেমন: ARSENAL VS ATLETICO MADRID)
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            try:
                # ৩. ম্যাচের ভেতর ঢুকে প্লেয়ারের সোর্স খোঁজা
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # m3u8 বা আইফ্রেম সোর্স খোঁজা (এটিই আসল স্ট্রিমিং লিঙ্ক)
                stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    playlist += f'#EXTINF:-1 group-title="Live Sports", {title}\n{stream.group(1)}\n'
                else:
                    # যদি ম্যাচ শুরু না হয়, তবে অন্তত পেজ লিঙ্কটা দিচ্ছি যাতে পরে দেখা যায়
                    playlist += f'#EXTINF:-1 group-title="Upcoming Matches", {title} (STILL NOT LIVE)\n{match_url}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Final Playlist updated!")

if __name__ == "__main__":
    grab_links()
