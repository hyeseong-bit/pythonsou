from flask import Flask, render_template, request
import pymysql
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # Flask에서 그래프를 이미지로 처리
import matplotlib.pyplot as plt
from markupsafe import escape
import base64
from io import BytesIO

app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8mb4'
}

def get_connection():
    return pymysql.connect(**db_config)

# matplotlib 한글 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dbshow", methods=['GET', 'POST'])
def dbshow():
    dept = request.args.get("dept", "").strip()

    # 검색 결과용 SQL
    sql = """
        select
            j.jikwonno as 사번,
            j.jikwonname as 직원명,
            b.busername as 부서명,
            j.jikwonjik as 직급,
            j.jikwonpay as 연봉,
            j.jikwongen as 성별,
            timestampdiff(year, j.jikwonibsail, curdate()) as 근무년수
        from jikwon j
        inner join buser b
            on j.busernum = b.buserno
    """

    # 전체 비율 계산용 SQL
    all_sql = """
        select
            j.jikwonno as 사번,
            j.jikwonname as 직원명,
            b.busername as 부서명,
            j.jikwonjik as 직급,
            j.jikwonpay as 연봉,
            j.jikwongen as 성별,
            timestampdiff(year, j.jikwonibsail, curdate()) as 근무년수
        from jikwon j
        inner join buser b
            on j.busernum = b.buserno
        order by b.buserno asc, j.jikwonname asc
    """

    params = []
    if dept:
        sql += " where b.busername like %s"
        params.append(f"%{dept}%")

    # 문제 조건: 부서번호, 직원명 순 오름차순
    sql += " order by b.buserno asc, j.jikwonname asc"

    with get_connection() as conn:
        df = pd.read_sql(sql, conn, params=params)   # 검색 결과용
        all_df = pd.read_sql(all_sql, conn)          # 전체 비율 계산용

    # 1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수
    if not df.empty:
        jikwon_df = df[['사번', '직원명', '부서명', '직급', '연봉', '근무년수']]
        jikwondata = jikwon_df.to_html(index=False)
    else:
        jikwondata = "<p>직원 정보가 없어요</p>"

    # 2) 부서명, 직급 자료를 이용하여 각각 연봉합, 연봉평균
    if not df.empty:
        stats_df = (
            df.groupby(['부서명', '직급'])['연봉']
            .agg(연봉합='sum', 연봉평균='mean')
            .round(2)
            .reset_index()
            .sort_values(by=['부서명', '직급'])
        )
        statsdata = stats_df.to_html(index=False)
    else:
        statsdata = "<p>통계 대상 자료가 없어요</p>"

    # 3) 부서명별 연봉합, 평균 세로막대 그래프
    chart_url = None
    if not df.empty:
        dept_pay = (
            df.groupby('부서명')['연봉']
            .agg(연봉합='sum', 연봉평균='mean')
            .round(2)
        )

        dept_pay.plot(kind='bar', figsize=(8, 5))
        plt.title('부서명별 연봉합 / 연봉평균')
        plt.xlabel('부서명')
        plt.ylabel('연봉')
        plt.xticks(rotation=0)
        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

    # 4) 성별, 직급별 빈도표
    if not df.empty:
        freq_df = pd.crosstab(df['성별'], df['직급'])
        freqdata = freq_df.to_html()
    else:
        freqdata = "<p>빈도표 자료가 없어요</p>"

    # 5) 부서별 최고 연봉자 1명
    if not df.empty:
        idx = df.groupby('부서명')['연봉'].idxmax()
        highpay_df = (
            df.loc[idx, ['부서명', '직원명', '연봉']]
            .sort_values(by='부서명')
            .reset_index(drop=True)
        )
        highpaydata = highpay_df.to_html(index=False)
    else:
        highpaydata = "<p>최고 연봉자 자료가 없어요</p>"

    # 6) 부서별 직원 비율 (전체 직원 기준)
    if not all_df.empty:
        total = len(all_df)
        dept_count = all_df['부서명'].value_counts().sort_index()
        ratio_df = pd.DataFrame({
            '부서명': dept_count.index,
            '인원수': dept_count.values,
            '비율(%)': ((dept_count / total) * 100).round(2).values
        })
        ratiodata = ratio_df.to_html(index=False)
        total_count = total
    else:
        ratiodata = "<p>비율 자료가 없어요</p>"
        total_count = 0

    return render_template(
        "dbshow.html",
        dept=escape(dept),
        jikwondata=jikwondata,
        statsdata=statsdata,
        freqdata=freqdata,
        highpaydata=highpaydata,
        ratiodata=ratiodata,
        total_count=total_count,
        chart_url=chart_url
    )

if __name__ == '__main__':
    app.run(debug=True)