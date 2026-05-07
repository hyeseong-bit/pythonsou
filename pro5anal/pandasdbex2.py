import sys
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# 콘솔 / 그래프 한글 설정
sys.stdout.reconfigure(encoding='utf-8')
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False


config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8'
}


# =========================
# a) jikwon, buser, gogek 테이블 분석
# =========================
conn = None
cursor = None

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    sql1 = """
        select
            j.jikwonno as 사번,
            j.jikwonname as 이름,
            b.busername as 부서명,
            j.jikwonpay as 연봉,
            j.jikwonjik as 직급
        from jikwon j
        inner join buser b
            on j.busernum = b.buserno
    """

    df = pd.read_sql(sql1, conn)
    print("직원 기본 정보 DataFrame")
    print(df.head())
    print()

    df.to_csv('jikwon_analysis.csv', index=False, encoding='utf-8-sig')
    print("파일 저장 완료 : jikwon_analysis.csv")
    print()

    dept_pay = df.groupby('부서명')['연봉'].agg(['sum', 'max', 'min'])
    print("부서명별 연봉의 합 / 최대 / 최소")
    print(dept_pay)
    print()

    ctab = pd.crosstab(df['부서명'], df['직급'])
    print("부서명-직급 교차표")
    print(ctab)
    print()

    sql2 = """
        select
            j.jikwonno as 사번,
            j.jikwonname as 직원명,
            g.gogekno as 고객번호,
            g.gogekname as 고객명,
            g.gogektel as 고객전화
        from jikwon j
        left join gogek g
            on j.jikwonno = g.gogekdamsano
        order by j.jikwonno
    """

    df_gogek = pd.read_sql(sql2, conn)

    df_gogek['고객번호'] = df_gogek['고객번호'].fillna('담당 고객 X')
    df_gogek['고객명'] = df_gogek['고객명'].fillna('담당 고객 X')
    df_gogek['고객전화'] = df_gogek['고객전화'].fillna('담당 고객 X')

    print("직원별 담당 고객자료")
    print(df_gogek)
    print()

    q80 = df['연봉'].quantile(0.8)
    high20 = df[df['연봉'] >= q80]
    print("연봉 상위 20% 직원")
    print(high20)
    print()

    median_pay = df['연봉'].median()
    print("전체 직원 연봉 중앙값 :", median_pay)
    print()

    sql3 = f"""
        select
            j.jikwonno as 사번,
            j.jikwonname as 이름,
            b.busername as 부서명,
            j.jikwonpay as 연봉,
            j.jikwonjik as 직급
        from jikwon j
        inner join buser b
            on j.busernum = b.buserno
        where j.jikwonpay >= {int(median_pay)}
    """

    df_top50 = pd.read_sql(sql3, conn)

    jik_avg = df_top50.groupby('직급')['연봉'].mean()
    print("연봉 상위 50% 직원의 직급별 평균 연봉")
    print(jik_avg)
    print()

    dept_avg = df.groupby('부서명')['연봉'].mean().sort_values()

    plt.figure(figsize=(8, 5))
    plt.barh(dept_avg.index, dept_avg.values)
    plt.xlabel('평균 연봉')
    plt.ylabel('부서명')
    plt.title('부서명별 평균 연봉')
    plt.tight_layout()
    plt.show()

except Exception as e:
    print("처리 오류 :", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# =========================
# b) jikwon 테이블을 이용한 pandas 분석
# - pivot_table : 성별 연봉 평균
# - 성별 평균 연봉 시각화
# - 부서명, 성별 crosstab
# =========================
conn = None

try:
    conn = pymysql.connect(**config)

    sql = """
        select
            j.jikwonname as 이름,
            b.busername as 부서명,
            j.jikwongen as 성별,
            j.jikwonpay as 연봉
        from jikwon j
        inner join buser b
            on j.busernum = b.buserno
    """

    df = pd.read_sql(sql, conn)
    print(df.head())
    print()

    pivot1 = pd.pivot_table(df, index='성별', values='연봉', aggfunc='mean')
    print('성별 연봉 평균')
    print(pivot1)
    print()

    gender_pay = df.groupby('성별')['연봉'].mean()

    plt.figure(figsize=(6, 4))
    plt.bar(gender_pay.index, gender_pay.values)
    plt.xlabel('성별')
    plt.ylabel('평균 연봉')
    plt.title('성별 평균 연봉')
    plt.tight_layout()
    plt.show()

    ctab = pd.crosstab(df['부서명'], df['성별'])
    print('부서명-성별 교차표')
    print(ctab)

except Exception as e:
    print('처리 오류 :', e)

finally:
    if conn:
        conn.close()


# =========================
# c) 사번, 직원명 입력 로그인
# - 로그인 성공 시 같은 부서 직원 출력
# - 인원수 출력
# - 성별 연봉 boxplot
# - 남/여 연봉 histogram
# =========================
conn = None
cursor = None

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    sabun = input("사번 입력 : ").strip()
    irum = input("직원명 입력 : ").strip()

    sql_login = """
        select jikwonno, jikwonname, busernum
        from jikwon
        where jikwonno = %s and jikwonname = %s
    """
    cursor.execute(sql_login, (sabun, irum))
    login_row = cursor.fetchone()

    if login_row is None:
        print("로그인 실패")

    else:
        print("로그인 성공\n")

        busernum = login_row[2]

        sql_emp = """
            select
                j.jikwonno as 사번,
                j.jikwonname as 직원명,
                b.busername as 부서명,
                j.jikwonjik as 직급,
                b.busertel as 부서전화,
                j.jikwongen as 성별,
                j.jikwonpay as 연봉
            from jikwon j
            inner join buser b
                on j.busernum = b.buserno
            where j.busernum = %s
        """

        df = pd.read_sql(sql_emp, conn, params=[busernum])

        print(df[['사번', '직원명', '부서명', '직급', '부서전화', '성별']])
        print()
        print("인원수 :", len(df), "명")

        male_pay = df[df['성별'] == '남']['연봉']
        female_pay = df[df['성별'] == '여']['연봉']

        plt.figure(figsize=(8, 5))
        data = []
        labels = []

        if len(male_pay) > 0:
            data.append(male_pay)
            labels.append('남')
        if len(female_pay) > 0:
            data.append(female_pay)
            labels.append('여')

        if len(data) > 0:
            plt.boxplot(data, tick_labels=labels)
            plt.title('성별 연봉 분포 및 이상치 확인')
            plt.xlabel('성별')
            plt.ylabel('연봉')
            plt.tight_layout()
            plt.show()
        else:
            print("성별 연봉 boxplot을 그릴 데이터가 없습니다.")

        plt.figure(figsize=(8, 5))

        if len(male_pay) > 0:
            plt.hist(male_pay, bins=5, alpha=0.5, label='남')
        if len(female_pay) > 0:
            plt.hist(female_pay, bins=5, alpha=0.5, label='여')

        plt.title('남/여 연봉 분포 비교')
        plt.xlabel('연봉')
        plt.ylabel('빈도수')
        plt.legend()
        plt.tight_layout()
        plt.show()

except pymysql.MySQLError as e:
    print("DB 처리 오류 :", e)

except Exception as e:
    print("처리 오류 :", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()