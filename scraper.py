import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    # শক্তিশালী ব্রাউজার হেডার যাতে সাইটটি ব্লক না করে
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://eplayhd.com/"
    }

    try:
        # ১. হোমপেজ লোড করা
        response = requests.get("https://eplayhd.com/", headers=headers, timeout=15)
        html_content = response.text

        # ২. ম্যাচের লিঙ্কগুলো খুঁজে বের করা
        # eplayhd সাধারণত /match/ বা সরাসরি স্লাগ ব্যবহার করে
        matches = re.findall(r'href="(https://eplayhd\.com/[^"]+)"', html_content)
        unique_matches = list(dict.fromkeys(matches)) # ডুপ্লিকেট সরানো

        for match_url in unique_matches:
            # অপ্রাসঙ্গিক লিঙ্ক ফিল্টার
            if any(x in match_url for x in ["privacy", "contact", "dmca", "about"]):
                continue
                
            # টাইটেল তৈরি এবং ক্যাটাগরি নির্ধারণ
            raw_title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            # কিউওয়ার্ড চেক করে গ্রুপ তৈরি করা
            group = "OTHERS LIVE"
            if any(x in raw_title for x in ["IPL", "CRICKET", "T20", "BPL"]): group = "CRICKET LIVE"
            elif any(x in raw_title for x in ["LALIGA", "FOOTBALL", "UEFA", "CHAMPIONS", "SOCCER"]): group = "FOOTBALL LIVE"
            elif "IPL" in raw_title: group = "IPL SPECIAL"

            try:
                # ৩. ম্যাচের ভেতরে ঢুকে m3u8 খোঁজা
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # m3u8 লিঙ্ক খোঁজার ৩টি আলাদা প্যাটার্ন (যাতে মিস না হয়)
                stream = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    stream_url = stream.group(1)
                    playlist += f'#EXTINF:-1 group-title="{group}", {raw_title}\n{stream_url}\n'
                else:
                    # যদি লিঙ্ক না পায়, তবে অন্তত পেজ লিঙ্কটা ব্যাকআপ হিসেবে রাখা
                    playlist += f'#EXTINF:-1 group-title="UPCOMING/WEB", {raw_title}\n{match_url}\n'
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("eplayhd Scraper updated successfully!")

if __name__ == "__main__":
    grab_links()
