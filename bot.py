import requests
from bs4 import BeautifulSoup
import time
import re

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Cookie": "secured=1; OASPRD4=e292230b-bcf2-475f-a299-7e89b890eba7; BWPRD4=801060d1-4635-49a3-92f7-b6d03e3d6b7e"
})

STAVKA = 30
MIN_KOEF = 1.8
MAX_PROIGRYSH = 5
SUMMA_X = 1260
SUMMA_Y = 210
STAVKA_X = 1215
STAVKA_Y = 369

proigryshi = 0
stavki = []
tekushaya = STAVKA

print("BOT ZAPUSHEN!")

while True:
    if proigryshi >= MAX_PROIGRYSH:
        print("STOP!")
        break

    print("Poisk... Stavka:", tekushaya, "Proigryshi:", proigryshi)
    r = session.get("https://old.olimpbet.kz/live/?slds=110")
    soup = BeautifulSoup(r.text, "html.parser")
    
    najdeno = False
    for row in soup.find_all("tr"):
        text = row.get_text(" ", strip=True)
        if ("0:2" in text or "2:0" in text) and "сет" in text.lower():
            link = row.find("a", href=True)
            if link:
                href = link["href"]
                mid = href
                if mid in stavki:
                    continue
                name = link.get_text(strip=True)
                print("NAJDEN:", name, text[:80])
                stavki.append(mid)
                najdeno = True
                break

    if not najdeno:
        print("Net matchej 0:2")

    time.sleep(15)





  
