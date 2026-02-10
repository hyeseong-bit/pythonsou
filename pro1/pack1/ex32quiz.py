from abc import *

class Employee(metaclass=ABCMeta):
    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai


    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self):
        pass

    def irumnai_print(self):
        print('이름:' + self.irum +', 나이:' + str(self.nai), end=' ')

class Temporary(Employee):
    lisu = 0
    lidang = 0

    def __init__(self, irum, nai, lisu, lidang):
        Employee.__init__(self, irum, nai)
        self.lisu = lisu
        self.lidang = lidang
        
    def pay(self):
        self.irumnai_print()
        return self.lisu * self.lidang
    
    def data_print(self):
        print('월급 :', str(self.pay()))

    def irumnai_print(self):
        print('이름:' + self.irum +', 나이:' + str(self.nai),'' , end='  ' )


t = Temporary('홍길동 :', 25, 20, 15000)
t.data_print()

class Regular(Employee):
    salary = "급여"

    def __init__(self, irum, nai, salary):
        self.salary = salary
        self.irum = irum
        self.nai = nai

    def pay(self):
        return self.salary

    def data_print(self):
        super().irumnai_print()
        print(' 월급 : ', str(self.pay()))

r = Regular('한국인 :',27 ,3500000)
r.data_print()

class salesrnan(Regular):
    sales = '실적'
    commission = '수수료'
    def __init__(self, irum, nai, salary, sales, commission):
        Regular.__init__(self, irum, nai, salary)
        self.sales = sales
        self.commission = commission

    def pay(self):
        return self.sales * self.commission + self.salary
        
    def data_print(self):
        super().irumnai_print()
        print('수령액 :', int(self.pay()))

s = salesrnan('손오공 :',29, 120000,500000,0.25)
s.data_print()
