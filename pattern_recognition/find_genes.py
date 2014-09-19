import pandas as pd
import numpy as np
import pickle
from cvxopt import matrix, solvers

data = pd.read_csv('./data_breast_cancer.csv', header=False).T
braca1, braca2 = data[data[3226] == 'BRACA1'], data[data[3226] == 'BRACA2']
not_braca1, not_braca2 = data[data[3226] != 'BRACA1'][1:], data[data[3226] != 'BRACA2'][1:]
n_genes = 3226
groups = {'braca1_x_braca2': (braca1, braca2),
          'braca1_x_not_braca1': (braca1, not_braca1),
          'braca2_x_not_braca2': (braca2, not_braca2)}

for gname, group_pair in groups.items():
    group1, group2 = group_pair
    lin_sep = []
    for gene1, gene2 in [(gene1, gene2) for gene1 in range(n_genes) for gene2 in range(gene1, n_genes)]:
        d1_a = [-1*float(d) for d in group1[gene1]]
        d1_b = [float(d) for d in group2[gene1]]
        d2_a = [-1*float(d) for d in group1[gene2]]
        d2_b = [float(d) for d in group2[gene2]]
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
    
    output = open('lin_sep.{}'.format(gname), 'wb')
    pickle.dump(lin_sep, output)
