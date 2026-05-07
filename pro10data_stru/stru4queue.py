from collections import deque

# 놀이공원 대기 줄
queue = deque()
print('놀이공원 기구 대기 시작')

queue.append('철수')
print('첫번째 줄서기 : ', list(queue))
queue.append('영희')
print('두번째 줄서기 : ', list(queue))
queue.append('민수')
print('세번째 줄서기 : ', list(queue))

print()

first_person = queue.popleft()
print(first_person, '놀이기구 탑승 : ')
print('현재 대기줄 : ', list(queue))
print()

first_person = queue.popleft()
print(first_person, '놀이기구 탑승 : ')
print('현재 대기줄 : ', list(queue))
print()

if queue:
    print('탑승 예정자:', queue[0])
else:
    print('대기자 없음')

print('\n----------------------------------------')

# FIFO를 class로 연습
class Queue:
    def __init__(self, iterable=None):
        if iterable is None:
            self._data = deque()
        else:
            self._data = deque(iterable)

    def enqueue(self, x):
        self._data.append(x)
        return x

    def dequeue(self):
        if not self._data:
            raise IndexError('큐 비어 있음')
        return self._data.popleft()

    def front(self):
        if not self._data:
            raise IndexError('큐 비어 있음')
        return self._data[0]

    def is_empty(self):
        return not self._data

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def __repr__(self):
        return f'Queue(front -> back = {list(self._data)})'


def demo1Func():
    imsi1 = Queue()
    imsi2 = Queue([10, 20, 30])

    print(imsi1)
    print(imsi2)
    print('맨 앞 요소:', imsi2.front())
    print('크기:', imsi2.size())
    print('dequeue:', imsi2.dequeue())
    print(imsi2)
    imsi2.clear()
    print(imsi2)
    print('-------------')
    q = Queue()
    for item in ['A','B','C','D']:
        q.enqueue(item)
        print(f'enqueue {item} -> ', q)

    print('FIFO에 따라 하나씩 추출')
    while not q.is_empty():
        print(f'dequeue -> ', q.dequeue(), '|now:', q)

def demo2Func(jobs, ppm=15):
    q = Queue(jobs) # 작업들 큐에 입력
    t_sec = 0.0     # 시뮬레이션 시간 누적
    order = []      # 실제 처리된 문서 저장

    print('프린터로 출력하기')
    while not q.is_empty():
        doc, pages = q.dequeue()
        # 출력시간 계산 : 페이지 수 / 분당 페이지 수 * 60
        duration = (pages / ppm) *  60.0
        t_sec += duration
        order.append(doc)
        print(f't={t_sec:6.1f}초 | 출력 : {doc:10s}({pages}페이지)')

    print('처리순서(FIFO) : ', order)


if __name__ == '__main__':
    demo1Func()
    print('문서 프린터로 출력 시물레이션 - FIFO')
    jobs = [('abc.pdf', 10),('nice.doc', 30),('good.txt', 5),]
    demo2Func(jobs, ppm=20) # 현재 프린터는 1분에 20장 출력