from socket    import socket, AF_INET, SOCK_STREAM
from time      import sleep
from threading import Thread
from multiprocessing import Process

class TikTok:
    def __init__(self, sessionid):
        self.sessionid = sessionid
        self.max_time  = 0
        self.socket    = socket(AF_INET, SOCK_STREAM)

    def commit(self, request_user):
        url     = b"/aweme/v1/commit/follow/request/approve/?aid=1233"
        payload = (b"from_user_id={}".format(request_user["uid"]))
        
        headers = (b"Host: api19-va.tiktokv.com\r\n"
                   b"accept-encoding: gzip\r\n"
                   b"cookie: sessionid={}\r\n"
                   b"x-gorgon: 0\r\n"
                   b"content-type: application/x-www-form-urlencoded; charset=UTF-8\r\n"
                   b"user-agent: okhttp/3.12.1\r\n"
                   b"\r\n".format(self.sessionid)
        )

        self.socket.connect(("api19-va.tiktokv.com", 443))
        self.socket.send(b"POST " + url + b" HTTP/1.1\r\n" + headers + payload)

        print("[*] Accepted {}'s follow request.".format(request_user["unique_id"]))
    
    def start(self):
        while True:
            url = b"/aweme/v1/user/following/request/list/?max_time={}&count=20&aid=1233".format(self.max_time)
            
            headers = (b"Host: api19-va.tiktokv.com\r\n"
                       b"accept-encoding: gzip\r\n"
                       b"cookie: sessionid={}\r\n"
                       b"user-agent: okhttp/3.12.1\r\n"
                       b"\r\n".format(self.sessionid)
            )
            self.socket.connect(("api19-va.tiktokv.com", 443))
            self.socket.send(b"GET " + url + b" HTTP/1.1\r\n" + headers)

            response = self.socket.recv(4096)
            response = response.decode().split("\r\n\r\n")[1]

            if "request_users" not in response or not response["request_users"]:
                sleep(1) # Prevent spam and other problems
                continue

            if response["has_more"] != 0:
                self.max_time = response["max_time"]
            else:
                for request_user in response["request_users"]:
                    Thread(target=self.commit, args=(request_user,)).start()
                sleep(1) # Prevent spam and other problems
                continue

            for request_user in response["request_users"]:
                Thread(target=self.commit, args=(request_user,)).start()

tiktok = TikTok(input("[>] Session ID: "))

for i in range(0, 100):
    Process(target=tiktok.start).start()
