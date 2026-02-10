# 어딘가에서 필요한 부품 핸들 클래스 작성
class PohamHandle:
    quantity = 0 # 핸들 회전량 (공유자원)

    def leftTurn(self, quentity):
        self.quantity = quentity
        return "좌회전"
    
    def rightTurn(self, quentity):
        self.quantity = quentity
        return "우회전"