# 일회용 서버 
from socket import *

serversock= socket(AF_INET, SOCK_STREAM)   # address family의 종류 중 일반적으로 쓰는게 INET 소켓 객체를 만드는 코드
# socket을 특정 컴과 바인딩
serversock.bind(('127.0.0.1',8888))     
serversock.listen(5)   # client와 연결 정보 수. 리스너 설정(1부터 5까지 설정 가능)
print('서버 서비스 중...')

conn, addr = serversock.accept()  # 수동적으로 연결을 받아들임
print('client addr : ', addr)
print('from client message : ', conn.recv(1024).decode())
conn.close()
serversock.close()