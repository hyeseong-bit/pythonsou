# 통계량 : 데이터의 특징을 하나의 숫자로 요약한 것.
# 표본 데이터를 추출해 전체(모집단) 데이터를 짐작 가능
# 평균, 분산, 표준편차 ...

grades = [1, 3, -2, 4]   # 점수(변량)들을 리스트에 저장

# 리스트 안의 값을 하나씩 출력하는 함수
def show_grades(grades):
    for g in grades:              # grades 안에 있는 값을 하나씩 g에 넣음
        print(g, end=" ")         # 줄바꿈하지 않고 옆으로 출력

show_grades(grades)               # 함수 호출 → 1 3 -2 4 출력
print()                           # 한 줄 띄우기

# 리스트의 합계를 구하는 함수
def grades_sum(grades):
    tot = 0                       # 합계를 저장할 변수, 처음엔 0으로 시작
    for g in grades:              # 리스트 값을 하나씩 꺼냄
        tot += g                  # 현재 값을 tot에 누적해서 더함
    return tot                    # 반복문이 다 끝난 뒤 최종 합계를 반환

print('합은 ', grades_sum(grades))  # 합계 출력 → 6

# 리스트의 평균을 구하는 함수
def grades_ave(grades):
    ave = grades_sum(grades) / len(grades)   # 합계 / 데이터 개수
    return ave                               # 계산한 평균 반환

print('평균은 ', grades_ave(grades))         # 평균 출력 → 1.5

# 분산(편차 제곱의 평균) : 평균값 기준으로 다른 값 들의 흩어진 정도
def grades_variance(grades):
    ave =grades_ave(grades)
    vari = 0
    for su in grades:
        vari += (su - ave) ** 2
    return vari / len(grades)
        # return vari / (len(grades)- 1)

print('분산은 ', grades_variance(grades))

# 표준편차 구하는 함수
def grades_std(grades):
    # 먼저 grades_variance(grades)로 분산을 구하고
    # 그 분산 값에 ** 0.5 를 해서 제곱근(루트)을 구함
    # 제곱근을 구한 값이 바로 표준편차
    return grades_variance(grades) ** 0.5

# 계산된 표준편차를 출력

grades = [1, 3, -2, 4]   # 점수 리스트

print('\n넘파이 지원 함수 사용')   # 줄바꿈 후 제목 출력

import numpy                      # numpy 라이브러리 불러오기

print('합 ', numpy.sum(grades))         # 리스트 전체 합계
print('평균 ', numpy.mean(grades))      # 리스트 평균
print('분산 ', numpy.var(grades))       # 리스트 분산
print('표준편차 ', numpy.std(grades))   # 리스트 표준편차
