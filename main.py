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

# ===== Marriottチェック（料金タグで判定） =====
def check_marriott(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    # ページに料金情報があるかチェック
    # Marriottのページでは「JPY」や金額が含まれるspanタグなどを探す
    if soup.find(string=lambda t: t and ("¥" in t or "JPY" in t)):
        return True
    return False

# ===== 楽天・じゃらんチェック（空室タグで判定） =====
def check_rakuten_jalan(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    # 楽天・じゃらんの空室表示は「空室」や「宿泊可」が含まれる要素をチェック
    availability_texts = soup.find_all(string=lambda t: t and ("空室" in t or "宿泊可" in t))
    for t in availability_texts:
        if "フェアフィールド" in t or "もてぎ" in t:
            return True
    return False

# ===== 全体チェック =====
def check():
    for name, url in URLS.items():
        try:
            available = False
            if name == "Marriott":
                available = check_marriott(url)
            else:  # 楽天・じゃらん
                available = check_rakuten_jalan(url)

            if available:
                notify(f"🔥{name} 空室！\n{url}")
                print(f"{name} 空室通知送信")
            else:
                print(f"{name} 空室なし")

        except Exception as e:
            print(f"{name} エラー: {e}")
