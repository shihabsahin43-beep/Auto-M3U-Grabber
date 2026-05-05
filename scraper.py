import requests
import re
import base64

def grab_links():
    playlist = "#EXTM3U\n"
    # ব্রাউজারের মতো ছদ্মবেশ ধরার জন্য শক্তিশালী হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://eplayhd.com/"
    }

    try:
        # ১. হোমপেজ থেকে লাইভ ইভেন্ট বের করা
        response = requests.get("https://eplayhd.com/", headers=headers, timeout=15)
        # ম্যাচ লিঙ্কের নতুন প্যাটার্ন
        matches = re.findall(r'href="(https://eplayhd\.com/(?:match|live)/[^"]+)"', response.text)
        
        # ডুপ্লিকেট লিঙ্ক সরানো
        unique_matches = list(dict.fromkeys(matches))
        
        for match_url in unique_matches[:6]: # প্রথম ৬টি ম্যাচ চেক করবে
            title = match_url.rstrip('/').split('/')[-1].replace('-', ' ').upper()
            
            # ২. প্রতিটি ম্যাচের পেজে গিয়ে লিঙ্ক খোঁজা
            sub_res = requests.get(match_url, headers=headers, timeout=15)
            html_content = sub_res.text

            # ৩. m3u8 বা ts লিঙ্ক খোঁজার মাল্টিপল প্যাটার্ন (Base64 বা Hidden লিঙ্ক চেক করবে)
            stream_links = re.findall(r'[\'"](https?://[^\'"]+\.(?:m3u8|ts)[^\'"]*)[\'"]', html_content)
            
            if stream_links:
                # প্রথম ভ্যালিড লিঙ্কটি নিবে
                playlist += f'#EXTINF:-1 group-title="Live Sports", {title}\n{stream_links[0]}\n'
            else:
                # যদি সরাসরি না পায়, তবে অন্তত পেজ লিঙ্কটা রাখছি যাতে তুমি ক্লিক করে দেখতে পারো
                playlist += f'#EXTINF:-1 group-title="Manual Links", {title} (OPEN IN BROWSER)\n{match_url}\n'

    except Exception as e:
        print(f"Error: {e}")

    # ফাইলটি সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Playlist updated successfully!")

if __name__ == "__main__":
    grab_links()
    
