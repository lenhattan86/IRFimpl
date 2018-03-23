import sched, time
from time import sleep

from threading import Timer

xyz = 1000
def print_time(a):    
    print "From print_time "+str(xyz), time.time()

def print_some_times():
    print time.time()
    for i in range(10): 
        Timer(i, print_time, (str(i))).start()

print_some_times()

# import sched, time
# s = sched.scheduler(time.time, time.sleep)
# def print_time(a):
#     print("From print_time " + str(a), time.time(), a)

# def print_some_times():
#     print(time.time())
#     for i in range(10):    
#         s.enter(i, 1, print_time, argument=(i))    
#         s.run()
#     print(time.time())
# print_some_times()