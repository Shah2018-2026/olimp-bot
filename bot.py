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

COOKIE = "secured=1; OASPRD4=e292230b-bcf2-475f-a299-7e89b890eba7; BWPRD4=801060d1-4635-49a3-92f7-b6d03e3d6b7e; cf_clearance=g4HUNUT4PaXBEWa2hcr1Tri1dhgFbpRw5StL0Sa9hvI-1782020658-1.2.1.1-YRNF.eJdXsg8wdeh4MNw0FTIBNY1CxnlkfpI5Sva1E.3pB5brk_fuVKgDpgvPzoTB_9aNb9ZEeH5BpGPwJHJdj3.bhX4kCkZE59SN5TSxiQSOqnXIgJeAJfo84.qQ6QO2BO30nUJlZTKMswkJkP0c96fC.v4hBJkZUd7_8X5KbYbni6aJHHXlbeZ4bU070CTWBCRA2YdZZ9U7jyOtsyd87DiDyfYJd9j0u55774MxXxLkwT1KT3LMEYRoNNlCHIFGZ4aQOqPBfSZYOk1xe54NjyMvDWTZqd3W65sM_E476DS36vvw7XES0ww_F.EwaIftAk9tLOhgPwkgQzMEcj5ZQ"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "accept": "application/json",
    "x-platform": "web-desktop-classic",
    "referer": "https://old.olimpbet.kz/live/?slds=110"
})

proigryshi = 0
stavki = []
tekushaya = STAVKA

print("BOT ZAPUSHEN!")

while True:
    if proigryshi >= MAX_PROIGRYSH:
        print("STOP!")
        break

    print("Poisk... Stavka:", tekushaya, "Proigryshi:", proigryshi)
    
    r = session.get("https://old.olimpbet.kz/api/v2/events?locale=ru&include-subsports=true&statuses=OPEN&statuses=TRADING&live=true&sportId=110&kinds=GENERAL&page-size=50")
    
    if r.status_code != 200:
        print("Oshibka:", r.status_code)
        time.sleep(10)
        continue
    
    data = r.json()
    events = data.get("items", [])
    
    najdeno = False
    for m in events:
        mid = m.get("id")
        if mid in stavki:
            continue
        score = m.get("score") or {}
        s1 = int(score.get("score1", 0) or 0)
        s2 = int(score.get("score2", 0) or 0)
        if (s1 == 0 and s2 == 2) or (s1 == 2 and s2 == 0):
            name = m.get("name", "?")
            print("NAJDEN:", name, s1, ":", s2)
            stavki.append(mid)
            najdeno = True
            break
    
    if not najdeno:
        print("Net matchej 0:2")
    
    time.sleep(15)

    
          



  
