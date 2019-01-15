import hashlib
import time

def create_key(time_vlue):
    return hashlib.sha1(
        str(((time_vlue * 6.9) + 34241258) * 2.4).encode("utf8")
    ).hexdigest()


def verify_key(key):
    current_time = int(time.time())
    time_list = list(range(current_time - 5, current_time + 5))
    a = list(map(create_key, time_list))
    # print(a)
    if key in a:
        return True
    else:
        return False
