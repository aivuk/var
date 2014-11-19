from multiprocessing import Pool
import time

def f(x):
    time.sleep(10)
    return 1

#p = Pool(processes=40)

if __name__ ==	'__main__': 
    result = map(f, [range(0,10000000)])
    
    print result
