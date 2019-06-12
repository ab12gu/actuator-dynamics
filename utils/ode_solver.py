###############
## filename: ode_solver.py
#
# by: Abhay Gupta
# date: 06-10-19
#
# desc: need to test out some ode solvers in python...
#
######


import pickle
import glob
import numpy as np
import math as m
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from scipy.integrate import odeint

def plot(data,time):
    """ Plot the data"""

    plt.plot(time,data[:,0], 'yo')
    plt.plot(time,data[:,1], 'go')
    plt.xlabel('time')
    plt.ylabel('Magnitude')
    plt.legend(['Exact A', 'Exact B', 'Model A', 'Model B', 'Data A', 'Data B']) 
    plt.show()

    return

def traj(y, t, coef1, coef2, poly_order):
    """
    ODE function

    param y,t:              initial cond, time range
    param coef1, coef2:     weights per equation
    param poly_order, p:    library order, upsample rate

    returns derivative 
    """

    # Create basis matrix   
    y1, y2 = y
    R = np.array([y1,y2])
    Q = np.array([0,0])
    S = np.vstack((R,Q))

    poly = PolynomialFeatures(poly_order)
    A = poly.fit_transform(S)
    A = np.delete(A, (1), axis=0)

    # Dot basis matrix w/ coefficients
    x1 = np.dot(A,coef1.T)
    x2 = np.dot(A,coef2.T)

    dydt =  [x1[0], x2[0]]

    return dydt

def ode_solve(data, ode_length, time_length, poly_order, x):
    """
    Solve ODE with given weights
    """

    ## integrate ODE -----------------------------------------------------------------
    t = np.linspace(0, time_length, ode_length)
    y0 = [data[0,0], data[0,1]]

    args = (x[:,0], x[:,1], poly_order)
    sol = odeint(traj, y0, t, args)

    return sol, t

def find_weights(data, time_length, poly_order):
    """
    Find values of weights corresponding to the system dynamics. 
    """

    ## AX=B SOLVERS ------------------------------------------------------------------
    b = np.gradient(data,axis=0) # take derivative of data

    poly = PolynomialFeatures(poly_order)

    A = poly.fit_transform(data)

    if data.shape[0] < A.shape[1]:
        print("ASSERT: Basis too big")
        return

    A_inv = np.linalg.pinv(A)
    x = np.dot(A_inv, b)

    return x

def bar_plot(x):
    coef = np.arange(0,len(x))

    plt.subplot(211)
    plt.bar(coef, x[:,0])
    plt.subplot(212)
    plt.bar(coef, x[:,1])
    plt.xlabel('Coefficients')
    plt.show()

    return
 
    
if __name__ == "__main__":

    import random

    # read all pickle files -------------------------
    time_length = 20
    poly_order = 2 # Create library function
    ode_length = 20
    noise = 5
    data = np.vstack((np.linspace(1,7,time_length+1), np.linspace(2,8,time_length+1))).T
    model = np.array(data, copy = True)

    model[:,0] = [x**2 for x in model[:,0]]
    data[:,0] = [x**2+noise*(random.random()-0.5) for x in data[:,0]]
    model[:,1] = [m.sin(x) for x in model[:,1]]
    data[:,1] = [m.sin(x)+noise*(random.random()-0.5) for x in data[:,1]]

    ## Filter data
    from scipy.signal import savgol_filter
    data[:,0] = savgol_filter(data[:,0], 19, 2)
    data[:,1] = savgol_filter(data[:,1], 19, 2)
    #plt.plot(data[:,0])
    #plt.show()
    
    ## Find and solve model of system
    x = find_weights(data, time_length, poly_order) # find the weights of the system 
    bar_plot(x)
    sol, t = ode_solve(data, ode_length, time_length, poly_order, x) # solve ode

    time = np.linspace(0, time_length, len(data[:,1]))
    plt.plot(time,model[:,0], 'r')
    plt.plot(time,model[:,1], 'b')

    plt.plot(t, sol[:, 0], 'y')
    plt.plot(t, sol[:, 1], 'g')


    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()

    ## Plot the data -----------------------------------------------------------------
    plot(data,time)
    plt.show()




   
