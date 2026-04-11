import requests
import os
from bs4 import BeautifulSoup

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

URLS = {
    "Marriott": "https://www.marriott.com/search/findHotels.mi?destinationAddress.city=Motegi&checkInDate=2026-10-02&checkOutDate=2026-10-04&rooms=1&adults=2",
    "楽天": "https://travel.rakuten.co.jp/HOTEL/167879/167879.html",
    "じゃらん": "https://www.jalan.net/yad372995/"
}

# ===== Webhook通知 =====
def notify(msg):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": msg})
    else:
        print("⚠️ WEBHOOK_URLが設定されていません")

# ===== 共通：ページ取得 =====
def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)

    print(f"[DEBUG] {url} status={r.status_code} size={len(r.text)}")

    return r.text


# ===== Marriott（軽修正版）=====
def check_marriott(url):
    text = fetch(url)

    # 「料金・空室系キーワード」に寄せる（¥単体はやめる）
    keywords = ["per night", "rate", "availability", "JPY", "¥"]

    for k in keywords:
        if k.lower() in text.lower():
            return True

    return False


# ===== 楽天・じゃらん（見逃し減らす版）=====
def check_rakuten_jalan(url):
    text = fetch(url)

    # 明確な満室ワードだけ除外（＝無ければチャンス扱い）
    deny_words = ["満室", "sold out", "予約できません", "空室なし"]

    for w in deny_words: