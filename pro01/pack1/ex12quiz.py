# 연습문제1) 리스트를 통해 직원 자료를 입력받아 가공 후 출력하기
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

def processfunc(datas):
    # datetime.now().year
    CURRENT_YEAR = 2026  # 고정된 값은 대문자로 표기 

    for data in datas:
        emp_no, name, base_pay, hire_year = data

        work_years = CURRENT_YEAR - hire_year

        if work_years <= 3:
            bonus = 150000
        elif work_years <= 8:
            bonus = 450000
        else:
            bonus = 1000000

        salary = base_pay + bonus

        if salary >= 3000000:
            tax_rate = 0.5
        elif salary >= 2000000:
            tax_rate = 0.3
        else:
            tax_rate = 0.15

        tax = int(salary * tax_rate)
        net_pay = salary - tax

        data.append(work_years)
        data.append(bonus)
        data.append(tax)
        data.append(net_pay)

    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 75)

    for d in datas:
        print(f"{d[0]:<4} {d[1]:<6} {d[2]:<8} {d[4]:<8} {d[5]:<8} {d[6]:<8} {d[7]}")

    print("-" * 75)
    print(f"처리 건수 : {len(datas)} 건")


datas = inputfunc()
processfunc(datas)

print('------------------')
# 문제2)리스트를 통해 상품 자료를 입력받아 가공 후 출력하기

def inputfunc():
    datas = [
        "새우깡,15",   # csv
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas

datas = inputfunc()

result = {}
for d in datas :
    name, num = d.split(",")
    num = int(num)
    
    if name in result:
        result[name] += num
    else:
        result[name] = num

print(result)

def outer2():
    def inner2(qty, price):
        total = qty * price
        return qty * price
    return inner2


q1 = outer2()   

result1 = q1(135, 450)
print(result1)

result2 = q1(115, 300)
print(result2)

result3 = q1(105, 450)
print(result3)

q1 = outer2()

datas = [(135, 450), (115, 300), (105, 450)]

total = 0

for qty, price in datas:
    amt = qty * price
    total += amt
    print(f"수량: {qty}, 단가: {price}, 금액: {amt}")

print("총합 :", total)






