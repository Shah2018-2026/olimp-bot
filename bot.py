import requests
import time
import pyautogui

STAVKA = 30
MIN_KOEF = 1.8
MAX_PROIGRYSH = 5
SUMMA_X = 1260
SUMMA_Y = 210
STAVKA_X = 1215
STAVKA_Y = 369

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "accept": "application/json",
    "x-platform": "web-desktop-classic",
    "referer": "https://old.olimpbet.kz/"
})

proigryshi = 0
stavki = []
tekushaya = STAVKA

print("BOT ZAPUSHEN!")
while True:
    if proigryshi >= MAX_PROIGRYSH:
        print("STOP! Limit progryshey!")
        break
    print("Poisk matchey... Stavka:", tekushaya, "Proigryshi:", proigryshi)
    r = session.get("https://old.olimpbet.kz/api/events?statuses=OPEN&live=true&sportId=110&locale=ru")
    if r.status_code != 200:
        print("Oshibka:", r.status_code)
        time.sleep(10)
        continue
    data = r.json()
    events = data.get("items", [])
    print("Matchej naideno:", len(events))
    for m in events:
        mid = m.get("id")
        if mid in stavki:
            continue
        score = m.get("score", {})
        s1 = int(score.get("score1", 0) or 0)
        s2 = int(score.get("score2", 0) or 0)
        if (s1 == 0 and s2 == 2) or (s1 == 2 and s2 == 0):
            print("NAJDEN:", m.get("name"), s1, ":", s2)
            stavki.append(mid)
    time.sleep(15)
