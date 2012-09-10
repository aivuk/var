from scipy.stats import *
import sys

"""
Script para geracao dos dados para a tarefa 2 de MAC460. 
Nao tem segredo: eh so rodar. Rode uma vez para o conjunto de treinamento 
e outra para o de testes. 
"""


num = expon.rvs(scale=6, size=20)
for n in num:
    print n, 1

num = uniform.rvs(loc=15, scale=10, size=20)
for n in num:
    print n, 2

num = norm.rvs(loc=12, scale=4, size=20)
for n in num:
    print n, 3
    
        
