class ElecProduct:
    volume = 0

    def volumeControl(self, volume):
    # print('볼륨을 조절한다')
        pass

class ElecTv(ElecProduct):
    def tv1(self):
        print('ElecTv 고유 메소드')
    def volumeControl(self, volume):
        print(f'ElecTv볼륨을 조절한다 : {volume}')  # 메소드 오버라이딩


class ElecRadio(ElecProduct):
    def volumeControl(self, volume):
        print('ElecRadio 고유 메소드')
    def volumeControl(self, volume):     # 메소드 오버라이딩
        sori = volume
        print(f'ElecRadio 소리를 조절한다 : {sori} ')

product = ElecProduct()
tv =ElecTv()
product = tv
product.volumeControl(5)
print()
radio = ElecRadio()
product = radio
product.volumeControl(3)

print('-------------')
q1 = [ElecProduct(),ElecTv() ,ElecRadio()]
for a in q1:
    a.volumeControl(2)
    print()



# super
class Animal:

    def move(self):
        print('대부분의 동물들은 4발로 걸어요')

class Dog(Animal):
    
    # Field
    name = '개'

    # Method
    def move(self):
        print('댕댕이')


class Cat(Animal):
    
    # Field
    name = '고양이'

    # Method
    def move(self):
        print('냥냥이')


class Wolf(Dog, Cat):
    pass


class Fox(Cat, Dog):
    
    #Method
    def move(self):
        print('여우')
    
    def foxMethod(self):
        pass

animal = [Animal(), Dog(), Cat(), Wolf(), Fox()]
for a in animal:
    print('-------'*10)
    print(a)      
    a.move()