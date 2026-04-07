import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1490931945570566174/OsKTPlbCpCZ28VDvxErtx5O9qEgI2txN2b568JsFBfrPfuuyX2FWyjVeQPHVUNfeBQL2"

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

            if "¥" in text or "空室" in text:
                notify(f"🔥{name} 空室の可能性！\n{url}")

        except:
            print(f"{name} エラー")

if __name__ == "__main__":
    check()