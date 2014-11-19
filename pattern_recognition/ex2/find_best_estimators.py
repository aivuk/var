import numpy as np
import pandas as pd
import pickle
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt

data = pd.read_csv('../ex1/data_breast_cancer.csv', header=False).T.convert_objects(convert_numeric=True)
braca1 = data[data[3226] == 'BRACA1']
braca2 = data[data[3226] == 'BRACA2']
not_braca1 = data[data[3226] != 'BRACA1'][1:]
not_braca2 = data[data[3226] != 'BRACA2'][1:]

groups = {'braca1_x_braca2': (braca1, braca2),
          'braca1_x_not_braca1': (braca1, not_braca1),
          'braca2_x_not_braca2': (braca2, not_braca2)}

lin_sep = {'braca1_x_braca2': pickle.load(open('../ex1/lin_sep_braca1_x_braca2', 'r')), 
           'braca1_x_not_braca1': pickle.load(open('../ex1/lin_sep_braca1_x_not_braca1', 'r')),
           'braca2_x_not_braca2': pickle.load(open('../ex1/lin_sep_braca2_x_not_braca2', 'r'))}

dict_label = {'BRACA1': 0, 'BRACA2': 1}

def conv_label(gname, v): 
    label = 'BRACA1' if gname != 'braca2_x_braca2' else 'BRACA2'
    return map(lambda x: 0 if x == label else 1, v)

def create_data(group_name, gene1=2, gene2=19):
    g1, g2 = groups[group_name]
    group_1 = np.vstack([g1[gene1], g1[gene2]]).T
    group_2 = np.vstack([g2[gene1], g2[gene2]]).T
    X_data = np.vstack([group_1, group_2])
    Y_data = np.concatenate([conv_label(group_name, g1[3226]), conv_label(group_name, g2[3226])])
    return X_data, Y_data

def grid_search_estimator(X_data, Y_data, c_min=-3, c_max=3, c_num=6, gamma_min=-2, gamma_max=2, gamma_num=5, n_folds=5):
    C_range= np.logspace(c_min, c_max, c_num)
    gamma_range = np.logspace(gamma_min, gamma_max, gamma_num)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedKFold(y=Y_data, n_folds=n_folds)
    grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
    grid.fit(X_data, Y_data)
    return grid.best_params_, grid.best_estimator_

def calc_errors(X_data, Y_data, estimator, sigma, plot=False, nsamples=50):
    total_points = float(nsamples*X_data.shape[0])
    colors = np.array(['blue', 'red'])
    if plot:
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')
    errors = 0
    for i in range(len(X_data)):
        mu = X_data[i]
        pontos_novos = np.random.multivariate_normal(mu, sigma, size=nsamples)
        if plot:
            plt.scatter(mu[0], mu[1], c=colors[Y_data[i]],alpha=1.0)
            plt.scatter(pontos_novos[:,0], pontos_novos[:,1], c=colors[Y_data[i]],alpha=0.4)
        errors += nsamples - sum(Y_data[i] == estimator.predict(pontos_novos))
    return errors/total_points

s_diag = 0.1
tested_pairs = {gname: set() for gname in lin_sep.keys()}
num_pairs = 1000

output_file = open('svm_rbf_estimator.csv', 'w')
output_file.write("Groups, Gene1, Gene2, Sigmma_diag, C, gamma, errors\n")

for i in range(num_pairs):
    for gname in lin_sep.keys():
        while True:
            rg1 = np.random.randint(3226)
            rg2 = np.random.randint(3226)
            if rg1 != rg2 and (rg1, rg2) not in lin_sep[gname] and (rg1, rg2) not in tested_pairs[gname] and (rg2, rg1) not in tested_pairs[gname] :
                 break

        X_data, Y_data = create_data(gname, rg1, rg2)
        best_params, best_estimator = grid_search_estimator(X_data, Y_data)
        sigma = s_diag*np.identity(2)
        errors = calc_errors(X_data, Y_data, best_estimator, sigma, plot=True)
        tested_pairs[gname].add((rg1, rg2))

        output_file.write("{}, {}, {}, {}, {}, {}, {}\n".format(gname, rg1, rg2, s_diag, best_params['C'], best_params['gamma'], errors))

output_file.close()
