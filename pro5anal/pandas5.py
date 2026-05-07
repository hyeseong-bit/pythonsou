# pandas file i/o
import pandas as pd
import numpy as np

df = pd.read_csv('ex1.csv')
# ex1.csv 파일을 읽어 DataFrame으로 생성
print(df, type(df))
# 데이터 내용과 자료형 출력
print()

df = pd.read_table('ex1.csv', sep=',')
# read_table로 csv 읽기, 구분자는 쉼표
df = pd.read_table('ex1.csv', sep=',', skip_blank_lines=True)
# skip_blank_lines : 칼럼명, 데이터 앞에 공백 제거
# 빈 줄이 있으면 무시하고 읽음
print(df)
print()

pd.set_option('display.max_columns', None)   # 모든 칼럼 표시 옵션
# 출력 시 컬럼이 많아도 생략하지 않고 전부 보이게 함

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv')
# 인터넷 주소의 csv 파일 읽기
print(df)

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv', header=None)
# header=None : 첫 줄도 컬럼명이 아니라 일반 데이터로 처리
print(df)

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv', header=None, skiprows=1)
# skiprows=1 : 첫 번째 줄 건너뛰고 읽기
print(df)

df = pd.read_csv(
    'https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv',
    header=None,
    names=['a', 'b', 'c', 'd', 'e']
)
# 컬럼명을 직접 지정
print(df)
print()

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt')
# txt 파일 읽기
print(df)

df = pd.read_table('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt', sep='\s+')
# 공백이 여러 개일 때 \s+ 로 구분해서 읽기
print(df)
print(df.iloc[:, 0])
# 모든 행의 첫 번째 열만 출력

df = pd.read_table('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt', sep='\s+', skiprows=[1, 3])
# 1행과 3행을 건너뛰고 읽기
print(df)

df = pd.read_fwf(
    'https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/data_fwt.txt',
    header=None,
    widths=(10, 3, 5),
    names=('data', 'name', 'price'),
    encoding='utf8'
)
# read_fwf : 고정폭 파일 읽기
# widths : 각 열의 글자 수 폭 지정
print(df)
print(df.iloc[:, 0])
# 첫 번째 열 출력
print(df['data'])
# data 컬럼 출력

print('\nchunk : 대량의 데이터를 부분씩 메모리로 읽어 처리')
# 대용량 자료 로딩시 초과 오류 발생 방지 : 메모리를 절야
# 스트리머 방식으로(일부만 순차 처리)으로 읽음
# 분산처리의 효과 
# 여러 번 반복해 읽어야 하므로 속도는 느리다.
import time 

n_rows = 10000
# 생성할 행 개수

data = {
    'ID': range(1, n_rows + 1),
    # 학생 번호 1 ~ 10000

    'name': [f'Student_{i}' for i in range(1, n_rows + 1)],
    # Student_1, Student_2, ... 형태로 이름 생성

    'score1': np.random.randint(50, 101, size=n_rows),
    # 50 ~ 100 사이의 정수 난수 생성

    'score2': np.random.randint(50, 101, size=n_rows)
    # 50 ~ 100 사이의 정수 난수 생성
}

df = pd.DataFrame(data)
# 딕셔너리를 DataFrame으로 변환
print(df.head())
# 앞 5행 출력
print(df.tail(3))
# 뒤 3행 출력

csv_fname = 'students.csv'
df.to_csv(csv_fname, index=False) # 파일 저장
# index=False : 인덱스는 저장하지 않음

print('-------------------------------')
# csv 파일 읽기 : 전체 한 번에 읽기
start_all = time.time()
# 전체 읽기 시작 시간

df_all = pd.read_csv(csv_fname)
# 파일 전체를 한 번에 읽음

average_all_1 = df_all['score1'].mean()
# score1 평균 계산
average_all_2 = df_all['score2'].mean()
# score2 평균 계산
time_all = time.time() - start_all
# 전체 한 번에 읽은 시간 계산

# chunk로 읽기
chunk_size = 1000
# 한 번에 1000행씩 읽기

total_score1 = 0
# score1 총합 누적 변수
total_score2 = 0
# score2 총합 누적 변수
total_count = 0
# 전체 학생 수 누적 변수
start_chunk_total = time.time()
# chunk 전체 처리 시작 시간

for i, chunk in enumerate(pd.read_csv(csv_fname, chunksize=chunk_size)):
    # csv 파일을 1000행씩 나눠 읽으면서 반복
    start_chunk = time.time()

    # 청크 처리 중 첫번쨰 학생 정보 출력
    first_statudent = chunk.iloc[0]
    # 현재 chunk의 첫 번째 행 선택

    print(
        f"Chunk {i + 1} 첫번째 학생:ID={first_statudent['ID']}, 이름={first_statudent['name']} "
        f"score1{first_statudent['score1']},score2{first_statudent['score2']}"
    )

    total_score1 += chunk['score1'].sum()
    # 현재 chunk의 score1 합계를 누적
    total_score2 += chunk['score2'].sum()
    # 현재 chunk의 score2 합계를 누적
    total_count += len(chunk)
    # 현재 chunk의 행 수를 누적

    end_chunk = time.time()
    elapsed = end_chunk - start_chunk
    # 현재 chunk 처리 시간 계산
    print(f"    처리 시간: {elapsed:7f}")       # 청크 단위 처리 시간

time_chunk_total = time.time() - start_chunk_total
# chunk 전체 처리 시간
average_chunk1 = total_score1 / total_count
# chunk 방식 score1 평균
average_chunk2 = total_score2 / total_count
# chunk 방식 score2 평균

print('\n처리 결과')
print(f"전체 학생 수 : {total_count}")
print(f"score1 총합 : {total_score1}, 평균 : {average_chunk1:3f}")
print(f"score2 총합 : {total_score2}, 평균 : {average_chunk2:3f}")
print(f"전체 한 번에 처리 시간 : {time_all:7f}초")
print(f"청크로 처리한 총 시간 : {time_chunk_total:7f}초")

# 청크 처리 시간 시각화
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
labels = ['전체 한번에 처리', '청크로 처리']
times = [time_all, time_chunk_total]

plt.figure(figsize=(6, 4))
bars = plt.bar(labels, times, color=['skyblue','red'])
for bar, time_val in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2,\
            bar.get_height(), f'{time_val:3f}초', \
            ha='center', va='bottom', fontsize=10)
plt.ylabel('처리 시간(초)')
plt.grid(linestyle='--')
plt.tight_layout()
plt.show()