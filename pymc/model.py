import pymc
import numpy as np

data = np.array([0 for i in range(0,500)] + [1] + [2 for i in range(0, 500)])

c0 = len(data[data == 0])
c1 = len(data[data == 1])
c2 = len(data[data == 2])
                                            
p = pymc.Dirichlet('prior', theta=[len(data)/3, len(data)/3, len(data)/3])
choices = pymc.Categorical('choice', p=p, value=data, observed=True)
choices_sim = pymc.Categorical('choice_sim', p=p) 

