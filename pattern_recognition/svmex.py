import pandas as pd
from cvxopt import matrix, solvers
import numpy as np
import pickle
import pprint
import pylab as plt
from formcreator import *

pp = pprint.PrettyPrinter()
data = pd.read_csv('./data_breast_cancer.csv', header=False).T
braca1 = data[data[3226] == 'BRACA1']
braca2 = data[data[3226] == 'BRACA2']
not_braca1 = data[data[3226] != 'BRACA1'][1:]
not_braca2 = data[data[3226] != 'BRACA2'][1:]
groups = {'braca1_x_braca2': (braca1, braca2),
          'braca1_x_not_braca1': (braca1, not_braca1),
          'braca2_x_not_braca2': (braca2, not_braca2)}

def find_soft_hyperplane(group1, group2, C=1000):

    is_separable = test_linear_separability(group1, group2)

    if not is_separable:
        return "Not linearly separable"

    d = 2
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

    plot_hyperplane(group1, group2, sol['x'])

    w = pp.pformat(list(sol['x']))
    margin = 2/np.sqrt(np.sum(sol['x'][0:2]**2))

    output = '<img src="/imgs/plot.png?{}"><p/><pre>{}</pre>'.format(np.random.random(), 
		pp.pformat(sol) + '\n\nw = {}\n\nMargin = {}'.format(w, margin))

    return output

def plot_hyperplane(group1, group2, w):
    plt.figure()
    plt.scatter(group1.icol(0), group1.icol(1), c='red')
    plt.scatter(group2.icol(0), group2.icol(1))
    xmin, xmax = plt.xlim()
    sol = w[0:3]
    sol_w = np.sqrt(sum(sol**2))
    xspace = np.linspace(xmin, xmax)
    a = - sol[0] / sol[1]
    b = - sol[2] / sol[1]
    yspace = a * xspace + b 
    yspace_a = a * xspace + b + (1/sol_w)
    yspace_b = a * xspace + b - (1/sol_w)
    plt.plot(xspace,yspace, 'k--')
    plt.plot(xspace,yspace_a, 'k-')
    plt.plot(xspace,yspace_b, 'k-')
    plt.savefig('imgs/plot.png')

def find_hard_hyperplane(group1, group2):

    is_separable = test_linear_separability(group1, group2)

    if not is_separable:
        return "Not linearly separable"

    P = matrix(np.diag([1.0,1,0]))
    q = matrix([0.0]*3)
    h = matrix(-1*np.ones(group1.shape[0] + group2.shape[0]))
    G1 = np.column_stack([group1, np.ones(group1.shape[0])])
    G2 = -1.0*np.column_stack([group2, np.ones(group2.shape[0])])
    G = matrix(np.vstack([G1, G2]))

    try:
        sol = solvers.qp(P, q, G, h)
    except:
        return "No optimal solution" 
    
    plot_hyperplane(group1, group2, sol['x'])
    output = '<img src="/imgs/plot.png?{}"><p/><pre>{}</pre>'.format(np.random.random(), pp.pformat(sol) + '\n\nw = {}'.format(pp.pformat(list(sol['x']))))

    return output

def test_linear_separability(group1, group2):
    d1_a = list(-1*group1.icol(0))
    d1_b = list(group2.icol(0))
    d2_a = list(-1*group1.icol(1))
    d2_b = list(group2.icol(1)) 
    b = matrix(-1*np.ones(len(d1_a + d1_b)))
    A = matrix([d1_a + d1_b,
                d2_a + d2_b,
                list(np.concatenate((-1*np.ones(len(d1_a)), np.ones(len(d1_b)))))])
    c = matrix(np.zeros(3))
    
    try:
        s = solvers.lp(c, A, b)
    except:
        return False
    
    if s['x']:
        return True
    else:
        return False

def params_find_soft(gene1, gene2, groups_name='braca1_x_braca2', c=1000):
    print groups_name
    group1, group2 = groups[groups_name]
    group1 = group1[[gene1, gene2]].convert_objects(convert_numeric=True)
    group2 = group2[[gene1, gene2]].convert_objects(convert_numeric=True)
   
    return find_soft_hyperplane(group1, group2)

def params_find_hard(gene1, gene2, groups_name='braca1_x_braca2'):
    group1, group2 = groups[groups_name]
    group1 = group1[[gene1, gene2]].convert_objects(convert_numeric=True)
    group2 = group2[[gene1, gene2]].convert_objects(convert_numeric=True)
   
    return find_hard_hyperplane(group1, group2)

soft = Form(params_find_soft, dirs=['imgs'], name="Soft Margin", output_type='html')
soft += Integer("Gene 1")
soft += Integer("Gene 2")
soft += Radio("Grupos", default='braca1_x_braca2', choices=[('braca1_x_braca2', 'Braca 1 com Braca 2'),
                                                            ('braca1_x_not_braca1', 'Braca 1 com Diferente de Braca 1'),
				                                            ('braca2_x_not_braca2', 'Braca 2 com Diferente de Braca 2')])

hard = Form(params_find_hard, name="Hard Margin", output_type='html')
hard += Integer("Gene 1")
hard += Integer("Gene 2")
hard += Radio("Grupos", default='braca1_x_braca2', choices=[('braca1_x_braca2', 'Braca 1 com Braca 2'),
                                                            ('braca1_x_not_braca1', 'Braca 1 com Diferente de Braca 1'),
                  				                            ('braca2_x_not_braca2', 'Braca 2 com Diferente de Braca 2')])

app = MainApp('SVM', [soft, hard], host='0.0.0.0')

app.run()
