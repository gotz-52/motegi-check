import requests
import os
from bs4 import BeautifulSoup

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

URLS = {
    "Marriott": "https://www.marriott.com/search/findHotels.mi?destinationAddress.city=Motegi&checkInDate=2026-10-02&checkOutDate=2026-10-04&rooms=1&adults=2",
    "楽天": "https://travel.rakuten.co.jp/HOTEL/167879/167879.html",
    "じゃらん": "https://www.jalan.net/yad372995/"
}

# ===== Webhook通知（安全版）=====
def notify(msg):
    if not WEBHOOK_URL:
        print("⚠️ WEBHOOK_URL未設定")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print(f"通知エラー: {e}")


# ===== ページ取得（安全版）=====
def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"[DEBUG] {url} status={r.status_code} size={len(r.text)}")
        return r.text
    except Exception as e:
        print(f"取得エラー: {e}")
        return ""


# ===== Marriottチェック =====
def check_marriott(url):
    text = fetch(url)

    keywords = ["per night", "rate", "availability", "JPY", "¥"]

    for k in keywords:
        if k.lower() in text.lower():
            return True

    return False


# ===== 楽天・じゃらんチェック =====
def check_rakuten_jalan(url):
    text = fetch(url)

    # 満室系ワードがあれば除外
    deny_words = ["満室", "sold out", "予約できません", "空室なし"]

    for w in deny_words:
        if w in text:
            return False

    # ホテル名が含まれていれば候補
    if "もてぎ" in text or "フェアフィールド" in text:
        return True

    return False


# ===== 全体チェック =====
def check():
    for name, url in URLS.items():
        try:
            if name == "Marriott":
                available = check_marriott(url)
            else:
                available = check_rakuten_jalan(url)

            if available:
                notify(f"🔥 {name} 空室の可能性あり！\n{url}")
                print(f"{name} → 空室通知")
            else:
                print(f"{name} → 空室なし")

        except Exception as e:
            print(f"{name} エラー: {e}")


# ===== 実行 =====
if __name__ == "__main__":
    notify("✅ 通知テスト")
    check()
