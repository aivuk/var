import numpy
from numpy.random import random_sample
import math

def mkP(p, q):
    if p + q == 1:
        return numpy.array([[p, q, 0], 
                            [p/2.0, (p + q)/2.0, q/2.0], 
                            [0, p, q]])

def advance(s, p, n):
    for i in xrange(0,n):
        s = s.dot(p)
    return s

def adv(p,pop_size,steps):
    pop = []
    for i in pop_size:
        c = numpy.random_sample()
        if c <= p:
            pop.append('A')
        else: 
            pop.append('a')

    for i in xrange(0,steps):
        # AA
        r1,r2 = random_sample(size=2)
        c1 = 'A' if r1 <= p else 'a'
        c2 = 'A' if r2 <= p else 'a'
        g = c1 + c2
        
        for t in phen.keys():
            if t == g: 
                phen[t] += 1 
            else:
                phen[t] -= 1

