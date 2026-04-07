import requests
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

URLS = {
    "Marriott": "https://www.marriott.com/search/findHotels.mi?destinationAddress.city=Motegi&checkInDate=2026-10-02&checkOutDate=2026-10-04&rooms=1&adults=2",
    "楽天": "https://travel.rakuten.co.jp/HOTEL/167879/167879.html",
    "じゃらん": "https://www.jalan.net/yad372995/"
}

def notify(msg):
    requests.post(
        WEBHOOK_URL,
        json={"content": msg}
    )

def check():
    headers = {"User-Agent": "Mozilla/5.0"}

    for name, url in URLS.items():
        try:
            r = requests.get(url, headers=headers, timeout=10)
            text = r.text

            # ===== ここが重要（インデント） =====
            if name == "Marriott":
                if "¥" in text or "JPY" in text:
                    notify(f"🔥Marriott 空室！\n{url}")

            elif name == "楽天":
                if "フェアフィールド" in text and "もてぎ" in text and ("空室" in text):
                    notify(f"🔥楽天 本命ホテル空室！\n{url}")

            elif name == "じゃらん":
                if "フェアフィールド" in text and "もてぎ" in text and ("空室" in text):
                    notify(f"🔥じゃらん 本命ホテル空室！\n{url}")

        except Exception as e:
            print(f"{name} エラー: {e}")

if __name__ == "__main__":
    notify("テスト通知")
    check()