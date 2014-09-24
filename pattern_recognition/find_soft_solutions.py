import pandas as pd
from cvxopt import matrix, solvers
import numpy as np
import pickle

data = pd.read_csv('./data_breast_cancer.csv', header=False).T
braca1 = data[data[3226] == 'BRACA1']
braca2 = data[data[3226] == 'BRACA2']
not_braca1 = data[data[3226] != 'BRACA1'][1:]
not_braca2 = data[data[3226] != 'BRACA2'][1:]
groups = {'braca1_x_braca2': (braca1, braca2),
          'braca1_x_not_braca1': (braca1, not_braca1),
          'braca2_x_not_braca2': (braca2, not_braca2)}
C = 1000
d = 2

for gname, group_pair in groups.items():
    group1, group2 = group_pair
    genes = pickle.load(open('lin_sep_{}'.format(gname), 'rb'))
    solutions = {}
    for gene1, gene2 in genes:
        group1, group2 = groups[gname]
        group1 = group1[[gene1, gene2]].convert_objects(convert_numeric=True)
        group2 = group2[[gene1, gene2]].convert_objects(convert_numeric=True)
        n_data = group1.shape[0] + group2.shape[0]
        h = matrix([-1.0] * n_data + [0] * n_data)
        q = matrix([0.0] * (d + 1) + [C] * n_data)
        P = matrix(np.diag(d*[1.0] + (n_data + 1)*[0.0]))
        ones = np.array([1.0]*group1.shape[0] + [-1.0]*group2.shape[0]).reshape((n_data, 1))
        V1 = np.hstack([np.vstack([group1, -1*group2]), ones, -1*np.identity(n_data)])
        V2 = np.hstack([np.zeros([n_data, d + 1]),-np.identity(n_data)])
        G = matrix(np.vstack([V1,V2]))

        try:
            sol = solvers.qp(P, q, G, h)
        except:
            pass

        solutions[(gene1, gene2)] = sol

    pickle.dump(solutions, open('solutions_soft.{}'.format(gname), 'wb'))
