import pandas as pd
import numpy as np
import pickle
from cvxopt import matrix, solvers

data = pd.read_csv('./data_breast_cancer.csv', header=False)
da = data.T

lin_sep = []
braca1 = da[da[3226] == 'BRACA1']
braca2 = da[da[3226] == 'BRACA2']
not_braca1 = da[da[3226] != 'BRACA1'][1:]
not_braca2 = da[da[3226] != 'BRACA2'][1:]
n_genes = 3226

for gene1, gene2 in [(gene1, gene2) for gene1 in range(n_genes) for gene2 in range(gene1, n_genes)]:

    d1_a = [-1*float(d) for d in braca2[gene1]]
    d1_b = [float(d) for d in not_braca2[gene1]]
    d2_a = [-1*float(d) for d in braca2[gene2]]
    d2_b = [float(d) for d in not_braca2[gene2]]

    b = matrix(-1*np.ones(len(d1_a + d1_b)))
    A = matrix([d1_a + d1_b,
                d2_a + d2_b,
                list(np.concatenate((-1*np.ones(len(d1_a)), np.ones(len(d1_b)))))])
    c = matrix(np.zeros(3))

    try:
        s = solvers.lp(c, A, b)
    except:
        continue

    if s['x']:
        lin_sep += [(gene1, gene2)]


output = open('line_sep_braca2_x_not_braca2', 'wb')
pickle.dump(lin_sep, output)
