import requests
import re

def grab_links():
    playlist = "#EXTM3U\n"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footystream.pk/soccer-streams"
    }

    try:
        # ১. সকার স্ট্রিম পেজটি লোড করা যেখানে লাইভ ম্যাচ থাকে
        target_url = "https://footystream.pk/soccer-streams"
        response = requests.get(target_url, headers=headers, timeout=15)
        html = response.text

        # ২. লাইভ ম্যাচের লিঙ্কগুলো খোঁজা (অ্যাড লিঙ্ক ফিল্টার করা)
        # সাধারণত ম্যাচের লিঙ্কগুলোতে 'soccer-stream' বা 'live' কথাটি থাকে না, থাকে সরাসরি দলের নাম
        matches = re.findall(r'href="(https://footystream\.pk/[^"]+)"', html)
        
        unique_matches = []
        for link in matches:
            # সকার স্ট্রিমস পেজ বা প্রাইভেসি পলিসি বাদ দিয়ে শুধুমাত্র ম্যাচের লিঙ্কগুলো নেওয়া
            if "/soccer-streams" not in link and "privacy" not in link and "contact" not in link:
                if link not in unique_matches:
                    unique_matches.append(link)

        count = 0
        for match_url in unique_matches:
            if count >= 10: break # অনেক বেশি লিঙ্ক হয়ে গেলে প্লেলিস্ট স্লো হয়ে যায়
            
            # টাইটেল সুন্দর করা (URL থেকে নাম নিয়ে)
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            try:
                # ৩. ম্যাচের ভেতর ঢুকে আসল স্ট্রিমিং সার্ভার খোঁজা
                sub_res = requests.get(match_url, headers=headers, timeout=10)
                sub_html = sub_res.text

                # m3u8 বা .ts ফাইল খোঁজার জন্য আরও উন্নত প্যাটার্ন
                # এই সাইটগুলো অনেক সময় iframe এর ভেতর লিঙ্ক লুকিয়ে রাখে
                stream = re.search(r'[\'"](https?://[^\'"]+\.(?:m3u8|ts)[^\'"]*)[\'"]', sub_html)
                
                if stream:
                    stream_url = stream.group(1)
                    # কিছু লিঙ্ক হয়তো ফেইক হতে পারে, সেগুলোকে বাদ দেওয়ার চেষ্টা
                    if "ads" not in stream_url and "analytics" not in stream_url:
                        playlist += f'#EXTINF:-1 group-title="LIVE FOOTBALL", {title}\n{stream_url}\n'
                        count += 1
                else:
                    # যদি সরাসরি না পাওয়া যায়, তবে অন্তত পেজ লিঙ্কটি রাখা যাতে ম্যানুয়ালি দেখা যায়
                    playlist += f'#EXTINF:-1 group-title="WEB STREAM", {title}\n{match_url}\n'
                    count += 1
            except:
                continue

    except Exception as e:
        print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print(f"Playlist updated with {count} matches!")

if __name__ == "__main__":
    grab_links()
