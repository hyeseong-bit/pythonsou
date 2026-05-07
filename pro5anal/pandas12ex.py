import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = "https://finance.naver.com/sise/sise_market_sum.naver"
headers = {"User-Agent": "Mozilla/5.0"}

rows = []   # 종목명, 시가총액 저장용 리스트

for page in range(1, 3):   # 1페이지~2페이지 반복
    params = {"page": page}
    res = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.select_one("table.type_2")   # 시가총액 표 선택
    trs = table.select("tr")                  # 표의 모든 행 가져오기

    for tr in trs:
        tds = tr.select("td")   # 한 행의 모든 칸 가져오기

        if len(tds) < 12:
            continue   # 데이터 행이 아니면 건너뜀

        name = tds[1].get_text(strip=True)        # 종목명
        market_cap = tds[6].get_text(strip=True)  # 시가총액

        if name and market_cap:
            rows.append([name, market_cap])

# csv 파일 저장
with open("market_sum.csv", mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["종목명", "시가총액"])   # 헤더 작성
    writer.writerows(rows)                  # 내용 작성

print("csv 저장 완료")

# csv 파일 읽기
df = pd.read_csv("market_sum.csv", encoding="utf-8-sig")

# 시가총액 컬럼 쉼표 제거 후 정수형 변환
df["시가총액"] = df["시가총액"].str.replace(",", "", regex=False).astype(int)

# 시가총액 상위 3개
top3 = df.sort_values(by="시가총액", ascending=False).head(3)

print(top3[["종목명", "시가총액"]])