from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from datetime import datetime

# =========================
# Selenium setup (أسرع + بروفايل)
# =========================
options = Options()
options.add_argument("user-data-dir=C:\\selenium_profile")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(20)

# =========================
# Telegram
# =========================
TOKEN ="8658156705:AAFfR1UpI9lnqlES7fEr7oU9BU8xy_neTDI"
CHAT_ID ="8740152058"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# =========================
# الجروبات
# =========================
group_urls = [
    "https://www.facebook.com/share/g/17k5cvKEHd/",
    "https://www.facebook.com/share/g/1CeRnV6efd/"
]

# =========================
# الكلمات
# =========================
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

# =========================
# منع التكرار لكل جروب
# =========================
seen_posts = {}

# =========================
# تشغيل مستمر
# =========================
while True:

    for group_url in group_urls:

        if group_url not in seen_posts:
            seen_posts[group_url] = set()

        try:
            driver.get(group_url)

            # استنى بسيط جدًا (سرعة أعلى)
            time.sleep(3)

            # Scroll خفيف للأحدث فقط
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)

            posts = driver.find_elements(By.XPATH, "//div[@role='article']")

            # ناخد الأحدث أول 5 بس (أسرع + جديد)
            for post in posts[:5]:

                try:
                    text = post.text.lower()

                    if len(text) < 10:
                        continue

                    # استخراج لينك
                    post_link = None
                    links = post.find_elements(By.TAG_NAME, "a")

                    for link in links:
                        href = link.get_attribute("href")
                        if href and "facebook.com" in href:
                            post_link = href
                            break

                    if not post_link:
                        continue

                    # منع التكرار داخل نفس الجروب
                    if post_link in seen_posts[group_url]:
                        continue

                    # البحث عن الكلمات
                    matched = any(word in text for word in keywords)

                    if not matched:
                        continue

                    print("🚨 NEW POST FOUND")

                    send_message(
                        f"🚨 New Post\n\nLink:\n{post_link}\n\n{text[:150]}"
                    )

                    seen_posts[group_url].add(post_link)

                except Exception as e:
                    print("Post error:", e)
                    continue

        except Exception as e:
            print("Group error:", e)

    # كل 3 دقايق (أسرع)
    time.sleep(180)