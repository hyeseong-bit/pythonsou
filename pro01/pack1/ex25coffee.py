class CoinIn:

    def __init__(self):    
        self.cupPrice = 200

    def calc(self, cupcount, coin):
        totalPrice = cupcount*self.cupPrice
        if coin < totalPrice:
            return None,None
        else:
            change = coin - totalPrice
            return cupcount, change

class MachineUI:
    def __init__(self):
        self.machine = CoinIn()
    
    def showDate(self):
        coin = int(input('동전을 입력하세요'))
        cup = int(input('몇 잔을 원하세요'))  


        cupcount, change = self.machine.calc(cup, coin)
        if cupcount is None:
            print('요금이 부족합니다.')
        else:
            print(f'커피 {cupcount}잔과 잔돈 {change}원')
if __name__ == '__main__':
    ui = MachineUI()
    ui.showDate()




class CoinIn:
    def __init__(self):
        self.cupPrice = 200

    def calc(self, cupCount, coin):
        totalPrice = cupCount*self.cupPrice
        if coin < totalPrice:
            return None, None
        
class MachineUI:
    def __init__(self):
        self.Machine = CoinIn


