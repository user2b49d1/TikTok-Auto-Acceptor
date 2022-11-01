from requests  import post, get
from time      import sleep
from threading import Thread

sessionid = input("[>] Session ID: ")
max_time  = 0

def commit(request_user, sessionid):
    url     = "https://api19-va.tiktokv.com/aweme/v1/commit/follow/request/approve/?aid=1233"

    payload = "from_user_id={}".format(request_user["uid"])
    
    headers = {
        "Host"            : "api19-va.tiktokv.com",
        "accept-encoding" : "gzip",
        "cookie"          : "sessionid={}".format(sessionid),
        "x-gorgon"        : "0", # Bypass "403 Forbidden"
        "content-type"    : "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent"      : "okhttp/3.12.1"
    }
    
    post(url, headers=headers, data=payload)

    print("[*] Accepted {}'s follow request.".format(request_user["unique_id"]))

while True:
    url      = "https://api19-va.tiktokv.com/aweme/v1/user/following/request/list/?max_time={}&count=20&aid=1233".format(max_time)
    
    headers  = {
        "Host"            : "api19-va.tiktokv.com",
        "accept-encoding" : "gzip",
        "cookie"          : "sessionid={}".format(sessionid),
        "user-agent"      : "okhttp/3.12.1"
    }
    
    response = get(url, headers=headers).json()

    if "request_users" not in response or not response["request_users"]:
        sleep(1) # Prevent spam and other problems
        continue

    if response["has_more"] != 0:
        max_time = response["max_time"]
    else:
        for request_user in response["request_users"]:
            Thread(target=commit, args=(request_user, sessionid,)).start()
        sleep(1) # Prevent spam and other problems
        continue

    for request_user in response["request_users"]:
        Thread(target=commit, args=(request_user, sessionid,)).start()