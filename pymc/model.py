import pymc
import numpy as np

n_ind = 100
trials_per_session = 100
sessions = 30

data = []

for i in xrange(0, n_ind):
    data.append(np.random.multinomial(trials_per_session, [1/3.]*3, size=sessions))

ind_params = []
choices = []

for i in xrange(0, n_ind):                                            
    ind_params.append([])
    choices.append([])
    for s in xrange(0, sessions):
        ind_params[-1].append(
                pymc.Dirichlet('prior_ind_{}_session_{}'.format(i,s),
                               theta=[1., 1., 1.]))

        choices[-1].append(pymc.Multinomial('choice_ind_{}_session_{}'.format(i,s), 
                                            n=trials_per_session, 
                                            p=ind_params[-1][-1],
                                            value=data[i][s], 
                                            observed=True))

