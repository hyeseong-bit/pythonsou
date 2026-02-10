# 반복문 for
# for i in [1,2,3,4,5]:
# for i in (1,2,3,4,5):
for i in {1,2,3,4,5}:
    print(i, end = ' ')

print('분산/표준편차 ---')
# numbers = [1,3,5,7,9]    # 합은25, 평균은 5.0
# numbers = [3,4,5,6,7]    # 합은25, 평균은 5.0
numbers = [-3,4,5,7,12]      # 합은25, 평균은 5.0
tot = 0
for a in numbers:            
        tot += a
print(f"합은{tot}, 평균은 {tot / len(numbers)}")
avg = tot / len(numbers)
# 편차의 합
hap = 0
for i in numbers:
    hap += (i - avg) ** 2
print(f'편차 제곱의 합 {hap}')
vari = hap / len(numbers)
print(f'분산은 {vari}')
print(f'표준편차 {vari ** 0.5}')

print()
colors = ['r', 'g', 'b']
for v in colors:
    print(v, end = ' ')

print('iter() : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어 주는 함수')
interator = iter(colors)
for v in interator:
    print(v, end = ', ')

print()
for idx, d in enumerate(colors):        # enumertate : 인덱스와 값을 반환
    print(idx, ' ', d)

print('사전형 ---')
datas = {'python':'만능언어', 'java':'웹용언어', 'mariadb':'RDBMS'}
for i in datas.items():
    # print(i)
    print(i[0], ' ~~ ', i[0])

for k, c in datas.items():
    print(k, ' ~~ ', v)

print()
for val in datas.values():
    print(val, end = ' ')




print('다중 for -------------------')
for n in [2, 3]:
    print('--{}단--'.format(n))
    for i in [1,2,3,4,5,6,7,8,9]:
        print('{} * {} = {}'.format(n, i, n * i))

print('continue, break --------')
nums = [1,2,3,4,5]
for i in nums:
    if i == 2:continue
    # if i == 4:break
    print(i, end = ' ')
else:
    print('정상종료')

print('\n정규 표현식 + for')
str = """ 오타니 쇼헤이(32·LA 다저스)가 3월 열리는 월드베이스볼클래식(WBC)에서 마운드에 오르지 않는다. 대회 2연패를 노리는 일본 야구대표팀에 비상등이 켜졌다. 일본 언론에서는 축구·농구 등은 월드컵이나 올림픽에서 세계 최고 선수들이 모두 나오는데 WBC는 그렇지 못하다며 아쉬운 목소리를 냈다.
데이브 로버츠 LA 다저스 감독은 1일 다저스타디움에서 열린 팬 감사 행사 ‘다저페스트’에서 취재진을 만나 “오타니는 WBC에서 투구를 하지 않는다”고 말했다. 그는 “지난 시즌 이닝 수, 그동안의 과정, 올 시즌 투타 겸업을 준비하는 과정을 종합하면 옳은 판단이라고 본다.
완전히 그의 결정”이라고 설명했다."""
import re 
str2 = re.sub(r'[^가-힣\s]','', str)  # 한글과 공백 이외의 문자는 공백처리
print(str2)
str3 = str2.split(' ')  # 공백을 구분자로 문자열 분리
print(str3)

cou = {} 
for i in str3:
    if i in cou:
        cou[i] += 1    # 같은 단어가 있으면 누적
    else:
        cou[i] = 1    # 최초 단어인 경우는 '단어' : 1

print(cou)

print('정규 표현식 좀 더 연습')
for test_ss in ['111-1234', '일이삼-일이삼사', '222-1234', '333&1234']:
    if re.match(r'^\d{3}-\d{4}$', test_ss):
        print(test_ss, '전화번호 맞아요')
    else:
        print(test_ss, '전화번호 아니야')

print('comprehension: 반복문 + 조건문 + 값 생성을 한 줄로 표현')
a = [1,2,3,4,5,6,7,8,9,10]
li = []
for i in a:
    if i % 2 == 0:
        li.append(i)  #append > 참 일때 
print(li)
print(list(i for i in a if i % 2 == 0))

# datas = [1, 2, 'a', True, 3.0]
datas = {1, 2, 'a', True, 3.0}
li2 = [i * i for i in datas if type(i) == int]
print(li2)

id_name = {1:'tom', 2:'oscar'}
name_id = {val: key for key, val in id_name .items()}
print(name_id)
print()
print([1,2,3])
print(*[1,2,3])  # * :unpack 1,2,3
aa = [(1,2),(3,4), (5,6)]
for a, b in aa:
    print(a + b)

print([a + b for a, b in aa])   # [3,7, 11]
print(*[a + b for a, b in aa], sep ='\n')   #sep ='\n' > 다음 줄로 떨어트리기

print('\n수열 생성 : range')
print(list(range(1, 6)))   # [1, 2, 3, 4, 5]
# print(list(range(1, 6, 1)))
print(tuple(range(1, 6, 2)))   # (1, 3, 5)
print(list(range(-10, -100, -20)))
print(set(range(1, 6)))
for i in range(6):           #  0 1 2 3 4 5 > 0부터 출발하고 6 미만
    print(i, end = ' ')

for  _ in range(6):
    print('반복')

tot = 0
for i in range(1, 11):
    tot += i
print('tot : ', tot)
print('tot: ', sum(range(1, 11)))   # sun() : 내장함수  

for i in range(1, 10):
    print(f'2 * {i} = {2 * 1}')

# 문1 : 2 ~ 9 구구단 출력(단은 행 단위 출력)
for n in [2, 3, 4 , 5, 6, 7 , 8, 9]:
    print('--{}단--'.format(n))
    for i in [1,2,3,4,5,6,7,8,9]:
        print('{} * {} = {}'.format(n, i, n * i))
# 문2 : 주사위를 두 번 던져서 나온 숫자들의 합이 4의 배수가 되는 경우만 출력
for i in range(6):
    n1 = i + 1
    for j in range(6):
        n2 = j + 1
        n = n1 + n2
        if n % 4 == 0:
            print(n1, n2)


print()
for i in range(1, 7, 1):
    for j in range(1, 7, 1):
        su = i + j
        if su % 4 == 0: print(i, j)


print('\nend')