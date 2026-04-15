import requests
import time

TOKEN ="8658156705:AAFfR1UpI9lnqlES7fEr7oU9BU8xy_neTDI"
CHAT_ID ="8740152058"

group_urls = [
    "https://www.facebook.com/share/g/17k5cvKEHd/",
    "https://www.facebook.com/share/g/1CeRnV6efd/"

]

keywords = [
    "بشرة",
    "بشره",
    "ديرمابن",
    "ديرما",
    "ديرما بلانينج"
    "derma"
    "تنضيف بشرة"
    "تنضيف بشره"
    "باديكير"
]

seen_posts = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def fetch_group(url):
    # ملاحظة: دي نسخة مبسطة (بدون Selenium)
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.text

while True:

    for url in group_urls:

        try:
            html = fetch_group(url)

            # بحث بسيط عن كلمات (بدون Selenium)
            lower_html = html.lower()

            for word in keywords:
                if word in lower_html:

                    if url + word in seen_posts:
                        continue

                    send_message(
                        f"🚨 New Match\nKeyword: {word}\nGroup: {url}"
                    )

                    seen_posts.add(url + word)

        except Exception as e:
            print("Error:", e)

    time.sleep(300)