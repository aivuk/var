# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Geometric approach for gene selection
# =====================================
# 
# [Geometric approach for gene selection - Marcelo Boareto](files/GeometricApproachMicroarrays.pdf)
# 
# $ D_{ij}^2 = \sum_g w_g \lVert x_{ig} - x_{jg}\rVert$
# 
# $ \sum_g w_g = 1 $
# 
# $ E = \frac{1}{n_c} \sum\limits_{ij \in C} D_{ij}^2  - \frac{1}{n_f} \sum\limits_{ij \in F} D_{ij}^2 $
# 
# E com isso teremos:
# 
# $ w_g = \frac{-\epsilon_g}{\sqrt{\sum_g \epsilon_g^2}} $
# 
# com $ \epsilon_g = \frac{1}{n_c} \sum\limits_{ij \in C}  \lVert x_{ig} - x_{jg}\rVert  - \frac{1}{n_f} \sum\limits_{ij \in F} \lVert x_{ig} - x_{jg}\rVert $ .
# 
# Primeiro vamos importar algumas coisas interessantes como Numpy e Pandas:

# <codecell>

import numpy as np
import pandas as pd
import itertools as i

# <codecell>

genes_expression = pd.read_csv('data/GSE22309_MAS5-processed-data.txt', delimiter='\t')

# <codecell>

ge = pd.DataFrame(genes_expression)

# <codecell>

l = [1,2,3]
list(i.combinations(l, 2))

# <codecell>

r = [1,3,4]; s = [5,4,6]
list(i.product(r,s))

# <markdowncell>

# Bom, vou fazer primeiro uma função que recebe uma matriz bidimensional das expressões gênicas, uma experimento por linha e um dicionário contendo os índices dos genes pertencentes a mesma classe de um determinado gene.

# <codecell>

def calc_metric_tensor(g_exp, classes):
    """
    @type g_exp: double dimensional matrix
    @param g_exp: one experiment per line and one gene per column
    @rtype: one dimensional vector 
    @return: the metric tensor
    """
    n_genes = len(g_exp)
    e_g = np.zeros(n_genes)
    comb_c = i.combinations(classes[0], 2)
    prod_f = i.product(classes[0], classes[1])
    len_c = len(list(comb_c))
    len_f = len(list(prod_f))
    e_g = [1/len_c*np.sum(i.imap(lambda (i,j): np.sqrt(g_exp[i][g]**2 - g_exp[j][g]**2), comb_c) - 1/len_f*np.sum(i.imap(lambda (i,j): np.sqrt(g_exp[i][g]**2 - g_exp[j][g]**2), comb_f)) for g in range(0, n_genes))]
    
    return e_g

# <codecell>

l = range(0,100)
np.random.shuffle(l)
cs = [l[0:50], l[50:]]
gtest = calc_metric_tensor(gr, [l[0:50], l[50:]])

# <codecell>

a = np.zeros(10)
a

# <codecell>

a[3] = 2, np.array(

# <codecell>


