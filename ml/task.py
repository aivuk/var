# -*- coding: utf-8 -*-

from scipy.stats import expon, uniform, norm
from math import sqrt
from functools import partial
import pylab
import numpy

# índices dos tipos das funções utilizadas nos modelos
ptypes = ['e', 'u', 'n']
# Tamanho total dos dados de uma classe
data_size = 400
# Tamanho do conjunto de treinamento dos dados de uma
# classe. Necessariamente menor que 'data_size'
training_size = 200
dx = 0.10

def max_idx(xs):
   """ Função para retornar índice do maior elemento 
       em uma lista 'xs' """
   vi, ci = 0, 0
   for c,v in enumerate(xs):
       if v > vi:
           vi, ci = v, c
   return ci

def mkU(data):
    """ Retorna pdf uniforme com parâmetros encontrados
        por Maximum Likelihood a partir de 'data' """
    a, b = min(data), max(data) 
    return uniform(loc=a, scale=b-a).cdf

def mkE(data):
    """ Retorna pdf exponencial com parâmetros encontrados
        por Maximum Likelihood a partir de 'data' """
    return expon(scale=sum(data)/len(data)).cdf

def mkN(data):
    """ Retorna pdf normal com parâmetros encontrados
        por Maximum Likelihood a partir de 'data' """
    m = sum(data)/len(data)
    sd = sqrt(sum(map(lambda xi: (xi - m)**2, data))/len(data))
    return norm(loc=m, scale=sd).cdf

# Matriz com dados de treinamento e teste.
# data[c] possui os dados da distribuição da classe c
data = numpy.array([ expon.rvs(scale=6, size=data_size)
                   , uniform.rvs(loc=15, scale=10, size=data_size)
                   , norm.rvs(loc=12, scale=4, size=data_size) ])

# Funções com parâmetros encontrados pelo método de 
# Máxima Verossimilhança.
# models_func[c][t] possui função do tipo t cálculada a 
# partir dos dados da classe c 
models_func = numpy.array([[mkE(data[i][0:training_size]),
                            mkU(data[i][0:training_size]),
                            mkN(data[i][0:training_size])] 
                                for i in xrange(0, 3)])

# Verossimilhanças calculadas a partir das funções ajustadas
# em models_func.
# likelihoods[dc][c][t] possui verossimilhanças dos dados da
# classe dc calculadas utilizando função do tipo t com 
# parâmetros encontrados com os dados da classe c.

likelihoods = []
for i in xrange(0,3):
    likelihoods.append([])
    for j in xrange(0,3):
        def prob_int(f, dx, x):
            return f(x + dx) - f(x - dx)
        likelihoods[i].append({t: map(partial(prob_int,
            models_func[j][t], dx/2.0),
            data[i][training_size:]) for t in xrange(0,3)})

likelihoods_a = numpy.array(likelihoods)
# Dicionário que possuirá todas as matrizes de confusão.
# conf_mats[(t1, t2, t3)] possuirá matriz de confusão
# quando o modelo é classe 1 com função de distribuição
# do tipo t1, classe 2 do tipo t2 e classe 3 do tipo t3
conf_mats = {}

# Laço para calcular matrizes de confusão para todos
# possíveis modelos
for t1, t2, t3 in [(t1, t2, t3) for t1 in xrange(0,3)
                                for t2 in xrange(0,3)
                                for t3 in xrange(0,3)]:
    conf_mats[(t1,t2,t3)] = {} 
    for i in xrange(0,3):
        c_guesses = []
        lk_i = zip(likelihoods[i][0][t1],
                   likelihoods[i][1][t2],
                   likelihoods[i][2][t3])
        c_guesses = map(max_idx, lk_i)
        count_classes = [c_guesses.count(c) for c in [0,1,2]]
        conf_mats[(t1,t2,t3)][i] = count_classes
 
# (funcs, erros) possui as funções (funcs) e o número 
# de erros (erros) do melhor modelo
best_model = ((), 0)
mod_corrects = {}
for m, mat in conf_mats.items():
    corrects = mat[0][0] + mat[1][1] + mat[2][2]
    mod_corrects[m] = corrects
    if corrects > best_model[1]:
        best_model = (m, corrects)

def make_report(conf_mats):
    for m, mat in conf_mats.items():
        print("================================================")
        for c,t in enumerate(m):
            print("Distribuição Classe {}:\t{}".format(c,t))
        print("\nMatriz de confusão:")
        print("\tc=0\tc=1\tc=2")
        for i in xrange(0, len(mat)):
            print("c={}\t{}\t{}\t{}".format(i, mat[i][0],mat[i][1],mat[i][2]))
        print("\nClassificações corretas: {}".format(mod_corrects[m]))

    print("================================================")
    print("Melhor modelo: {}\t Corretos: {}".format(best_model[0],
        best_model[1]))

make_report(conf_mats)

def plot_dists(cs):
   """ Plota funções exponencial, uniforme e normal ajustadas
       a partir de 'data' para classe 'c'. Na cor preta é 
       plotado a função de distribuição real da classe 'c'. """
   t = numpy.arange(0, 30, 0.01) 
   lf = [expon(scale=6).pdf,
         uniform(loc=15, scale=10).pdf,
         norm(loc=12, scale=4).pdf]
   for c in cs:
       # Pontos da função real da classe c
       p = map(lf[c], t)
       # Pontos das funções ajustadas para a classe c
       pg = [map(models_func[c][dt], t) for dt in ptypes]
       pylab.plot(t,p,c="black") 
       for i in xrange(0,3):
           pylab.plot(t, pg[i])


