from threading import Thread
import time


class C:
    data = []

d = []
def a():
    c = C()
    c.data = [1, 2, 3]
    global d
    d = c.data
    c.data.append(4)
    print("c.data", c.data)
Thread(target=a).start()
while True:
    print(d)
    time.sleep(0.5)