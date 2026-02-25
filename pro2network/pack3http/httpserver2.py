#CGIHTTPRequestHandler : SimpleHTTPRequestHandler의 확장 클래스
# CGI(Common Gateway Interface) : 
# 웹서버와 외부 프로그램 사이에서 정보를 주고받는 방법이나 규약
from  http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 8888

class Handler(CGIHTTPRequestHandler):    
    cgi_directories = ['/cgi-bin']

def run():

    serv = HTTPServer(('127.0.0.1', PORT), Handler)  # 상속 Handler
    print('웹 서비스 진행 중...')
    try:
        serv.serve_forever()  # 무한 루핑
    except:
        print('서버 종료')
    finally:
        serv.server_close()

if __name__ == '__main__':
    run()