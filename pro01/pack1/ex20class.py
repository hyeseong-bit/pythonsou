class Car:
    handle = 1
    speed = 0

    def __init__(self, name, speed):    
        self.name = name        # 현재객체의 name에게 name(지역변수) 인자값 치환 
        self.speed = speed
        

    def showData(self):
        km = "킬로미터"
        msg = "속도:" + str(self.speed) + km
        return msg
    
    def printHandle(self):
        return self.handle
    
print(Car.handle)     # 원형(prototype) 클래스의 멤버 호출
car1 = Car('tot', 10)   # 생성자 호출 후 객체 생성(인스턴스화)
print('car1 객체 주소:', car1)
print('car1 : ', car1.name, ' ',car1.speed, car1.handle)
car1.color = '파랑'
print('car1.color : ', car1.color)


car2 = Car('john', 20)   # 생성자 호출 후 객체 생성(인스턴스화)
print('car2 객체 주소:', car2)
print('car2 : ', car2.name, ' ',car2.speed, car2.handle)
# print(' ', car2.color)
print(Car, car1, car2)
print(id(Car), id(car1), id (car2))
print(car1.__dict__)   
print(car2.__dict__)

print('-----메소드----------')
print('car1 speed : ', car1.showData())  # prototype 으로 찾아가는 방식은 셀프 찍고 없으면 공유자원으로 찾아가는 방식
print('car2 speed : ', car2.showData())
car1.speed = 80
car2.speed = 110
print('car1 handle : ', car1.printHandle())
print('car2 handle : ', car2.printHandle())


