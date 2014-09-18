import numpy as np
import pylab as pl
import pylab as pl
from formcreator import *
from scipy.integrate import ode

def diff(t, x, i):
    dv = x[0] - (x[0]**3)/3.0 - x[1] + i
    dw = 0.08*(x[0] + 0.7 - 0.8*x[1])

    return np.array([dv, dw])

def integrate(func, v0, t0, tf, dt, *params):
    r = ode(func).set_integrator('dopri5')
    r.set_initial_value(v0, t0).set_f_params(*params)

    series = []
    while r.successful() and r.t < tf:
        r.integrate(r.t + dt)
        series.append(r.y)

    return np.array(series)

def intPlot(v0, w0, i):
    pl.figure()
    x0 = np.array([v0, w0])

    ps = integrate(diff, x0, 0, 1000, 0.1, i)

    pl.plot(ps[:,0], ps[:,1], 'm', linewidth=3)

    x = pl.linspace(-2.5, 2.5, 30)
    y = pl.linspace(-2.5, 2.5, 30)

    x1,y1 = pl.meshgrid(x,y)
    dx1, dy1 = diff(0, [x1,y1], i)
    m = (pl.hypot(dx1, dy1))
    m[m == 0] = 1.
    dx1 /= m
    dy1 /= m

    v0 = x - (x**3)/3.0 + i
    w0 = (x + 0.7)/0.8

    # Desenha grade e vetores de velocidade
    pl.grid()
    pl.quiver(x1, y1, dx1, dy1, m, pivot='mid', cmap=pl.cm.jet)
    pl.rcParams['figure.figsize'] = 13,9

    bd = 0.8
    pl.ylim(ymax=max(ps[:,1]) + bd, ymin=min(ps[:,1]) - bd)
    pl.xlim(xmax=max(ps[:,0]) + bd, xmin=min(ps[:,0]) - bd)

    pl.colorbar()

    pl.plot(x, w0, 'g--', linewidth=3)
    pl.plot(x, v0, 'r--', linewidth=3)

    pl.ylabel("W")
    pl.xlabel("V")

    pl.savefig('/usr/share/nginx/www/neuron/graph.png')

fh_n = Form(intPlot)
fh_n += Float("Corrente")
fh_n += Float("V0")
fh_n += Float("W0")
fh_n += Doc("""
![Plot](http://lem.ib.usp.br/neuron/graph.png)
""")

app = MainApp("FitzHugh-Nagano", [fh_n], host='lem.ib.usp.br')
app.run()
