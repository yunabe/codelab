import time

count = 0

def method():
    global count
    print 'reload.py: method (%02d)' % count
    count += 1
    time.sleep(1)
