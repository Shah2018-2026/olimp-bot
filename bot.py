import requests
import time
import pyautogui
import subprocess
import browser_cookie3

STAVKA = 30
MAX_RAZNICA = 3
SUMMA_X = 1260
SUMMA_Y = 210
STAVKA_X = 1215
STAVKA_Y = 369
OZHIDANIE = 7

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

stavki = []

def get_session():
    session = requests.Session()
    try:
        cookies = browser_cookie3.chrome(domain_name='.olimpbet.kz')
        session.cookies.update(cookies)
        print("Kuki polucheny iz Chrome!")
    except Exception as e:
        print("Oshibka kuki:", e)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "application/json",
        "x-platform": "web-desktop-classic",
        "referer": "https://old.olimpbet.kz/live/?slds=110"
    })
    return session

print("BOT ZAPUSHEN!")
print("Otkroj Chrome s Olimpbet i vojdi v kabinet!")
time.sleep(5)

session = get_session()

while True:
    print("Poisk... Stavka:", STAVKA)

    r = session.get("https://old.olimpbet.kz/api/v2/events?locale=ru&include-subsports=true&statuses=OPEN&statuses=TRADING&live=true&kinds=GENERAL&page-size=100")

    if r.status_code != 200:
        print("Oshibka:", r.status_code, "- obnovlyayu kuki...")
        session = get_session()
        time.sleep(10)
        continue

    data = r.json()
    events = data.get("items", [])
    tennis = [m for m in events if m.get("tournament") and str(m["tournament"].get("sportId","")) == "110"]
    print("Tenis matchej:", len(tennis))

    najdeno = False
    for m in tennis:
        mid = m.get("id")
        if mid in stavki:
            continue

        stats = m.get("statistics") or []
        score_str = ""
        periods_str = ""
        for s in stats:
            if s.get("code") == "score":
                score_str = s.get("value", "")
            if s.get("code") == "scores_by_periods":
                periods_str = s.get("value", "")

        if not score_str or ":" not in score_str:
            continue

        parts = score_str.split(":")
        try:
            s1 = int(parts[0].strip())
            s2 = int(parts[1].strip())
        except:
            continue

        if not ((s1 == 0 and s2 == 2) or (s1 == 2 and s2 == 0)):
            continue

        if periods_str:
            period_list = periods_str.split(",")
            if len(period_list) >= 3:
                third = period_list[2].strip()
                if ":" in third:
                    tp = third.split(":")
                    try:
                        t1 = int(tp[0].strip())
                        t2 = int(tp[1].strip())
                        raznica = abs(t1 - t2)
                        if raznica > MAX_RAZNICA:
                            print("Raznica bolshaya:", third, "propuskaem")
                            continue
                        print("3-j set:", third, "raznica:", raznica)
                    except:
                        pass

        name = m.get("name", "?")
        match_url = "https://old.olimpbet.kz/live/events/?ids=" + str(mid)
        print("NAJDEN:", name, score_str)
        print("U TEBYA", OZHIDANIE, "SEKUND - KLIKNI P1 ili P2!")
        stavki.append(mid)

        subprocess.Popen([CHROME, match_url])
        time.sleep(OZHIDANIE)

        pyautogui.click(SUMMA_X, SUMMA_Y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(str(STAVKA), interval=0.1)
        time.sleep(0.5)
        pyautogui.click(STAVKA_X, STAVKA_Y)
        time.sleep(1)
        print("STAVKA SDELANA:", STAVKA, "T")
        najdeno = True
        break

    if not najdeno:
        print("Net matchej 0:2")

    time.sleep(30)
