# -*- coding: utf-8 -*- 

from scipy.stats import expon, uniform, norm

def max_idx(xs):
    """ Função para retornar índice do maior elemento 
        em uma lista 'xs' """
    vi, ci = 0, 0
    for c,v in enumerate(xs):
        if v > vi:
            vi, ci = v, c
    return ci
 
def test_nb(data_size):
    dists = [ expon(scale=6)
            , uniform(loc=15, scale=10)
            , norm(loc=12, scale=4) ] 
    
    dp = [ d.pdf for d in dists ]
    data = [ d.rvs(size=data_size) for d in dists ]
                        
    lk = [map(lambda x:(dp[0](x), dp[1](x), dp[2](x)), data[i]) 
                        for i in xrange(0,3)]
    
    d = {i:[map(max_idx, lk[i]).count(j) for j in xrange(0,3)] 
                        for i in xrange(0,3)}

    return d[0][0] + d[1][1] + d[2][2]

for n in xrange(200, 1000, 20):
    corretos = test_nb(n)
    print "{} corretos de {}. Razão: {}".format(corretos, 3*n,
            corretos/(3.0*n))
