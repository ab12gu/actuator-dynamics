# Abhay Gupta
#
# date: 06-03-19
#
# description: put data into an input output format

import pickle
import glob
import numpy as np

# copied section of system

import numpy as np
import matplotlib.pyplot as plt

def spline(data, p):
    """Spline to add points to data"""

    from scipy import interpolate

    x = np.arange(0,data.shape[0], 1)
    f = interpolate.interp1d(x, data, kind='cubic', axis=0, bounds_error=True)

    xnew = np.arange(0, data.shape[0]-(1-1/p), 1/p)
    ynew = f(xnew)

    #plt.plot(data[:,1], 'ro')
    #plt.plot(ynew[:,0], 'bo')
    #plt.show()

    return ynew

def plot(data,years):
    #plt.plot(years,data[:,0], 'r')
    #plt.plot(years,data[:,1], 'b')
    plt.plot(years,data[:,0], 'yo')
    plt.plot(years,data[:,1], 'go')
    plt.xlabel('time (years)')
    plt.ylabel('Magnitude')
    plt.legend(['Model A', 'Model B', 'Data A', 'Data B']) 
    plt.show()

    return

def bar_plot(x):
    coef = np.arange(0,len(x))

    plt.subplot(211)
    plt.bar(coef, x[:,0])
    plt.subplot(212)
    plt.bar(coef, x[:,1])
    plt.xlabel('Coefficients')
    plt.show()

    return

def trajectory(y, t, coef1, coef2, poly_order, p):
    """
    ODE function

    param y,t:              initial cond, time range
    param coef1, coef2:     weights per equation
    param poly_order, p:    library order, upsample rate

    returns derivative 
    """

    # Create basis matrix  ----------------------------------------------------------- 
    from sklearn.preprocessing import PolynomialFeatures 
    y1, y2 = y

    ### test basis
    #R = np.sin(R)
    #R = np.array([1,1])

    R = np.array([y1,y2])
    Q = np.array([0,0]) # function requires 2+ array input
    S = np.vstack((R,Q))

    poly = PolynomialFeatures(poly_order)
    A = poly.fit_transform(S)
    A = np.delete(A, (1), axis=0)

    # dot basis matrix w/ coefficients
    x1 = np.dot(A,coef1.T)
    x2 = np.dot(A,coef2.T)

    #dydt = [x/(1/p) for x in [x1[0], x2[0]]]
    dydt = [x1[0], x2[0]]
    print('x1', dydt[0], 'x2', dydt[1])

    return dydt

def function(data, years, time_length):

    ## Upsample ----------------------------------------------------------------------
    p = 1.0 # upsample rate
    data = spline(data, p)

    time = np.linspace(0, time_length, len(data[:,1]))
    #plot(data,time)

    ## AX=B SOLVERS ------------------------------------------------------------------
    b = np.gradient(data,axis=0) # take derivative of data

    # Create library function
    from sklearn.preprocessing import PolynomialFeatures
    poly_order = 2
    poly = PolynomialFeatures(poly_order)

    A = poly.fit_transform(data)
    #A = poly.fit_transform(np.sin(data))
    if data.shape[0] < A.shape[1]:
        print("ASSERT: Basis too big")
        return

    # Create artificial ones matrix
    #A = np.ones((A.shape[0], A.shape[1]))

    A_inv = np.linalg.pinv(A)
    x = np.dot(A_inv, b)

    print('x', x)

    #bar_plot(x)

    # LASSO lambda1 > 0 & lambda 2 = 0 ------------------------------------------------
    #from sklearn import linear_model

    #clf = linear_model.Lasso(alpha=0.8, fit_intercept=False)
    #clf.fit(A,b)
    #x = clf.coef_.T

    ## integrate ODE -----------------------------------------------------------------

    return
    t = np.linspace(0, time_length, 400)
    y0 = [data[0,0], data[0,1]]
    from scipy.integrate import odeint

    args = (x[:,0], x[:,1], poly_order, p)
    sol = odeint(trajectory, y0, t, args)

    plt.plot(t, sol[:, 0], 'y')
    plt.plot(t, sol[:, 1], 'g')
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()

    plot(data,time)

    plt.show()

    return

if __name__ == "__main__":
    """ Import data for analysis"""

    # read all pickle files -------------------------------------
    vel = []
    eff = []
    pwm = []
    fn_input = []

    for counter, filepath in enumerate(glob.iglob('./../data/*.pkl')):
        with open(filepath,"rb") as input_file:
            e = pickle.load(input_file)

            pwm.append(e[0][605:1201])
            eff.append(e[1][605:1201])
            vel.append(e[2][605:1201])
    
    pwm = np.vstack(pwm)
    eff = np.vstack(eff)
    vel = np.vstack(vel)

    with open('export_file.pkl', 'wb') as f: # save array -------
        pickle.dump([pwm, eff, vel], f)

    #t = np.linspace(0, 2, len(vel[0]))
       
    # real data
    data = np.vstack((pwm[0], pwm[1])).T
    years = np.vstack((eff[0], eff[1])).T

    # artificial linear data
    time_length = 40
    data = np.vstack((np.linspace(1,7,time_length+1), np.linspace(2,8,time_length+1))).T**3

    #import math as m
    #data[:,1] = [m.sin(x)**2 for x in data[:,1]]
    #data = np.array([[20, 20, 52, 83, 64, 68, 83, 12, 36, 150, 110, 60, 7, 10, 70,                                      
    #                100, 92, 70, 10, 11, 137, 137, 18, 22, 52, 83, 18, 10, 9, 65],                                      
    #                [32, 50, 12, 10, 13, 36, 15, 12, 6, 6, 65, 70, 40, 9, 20,                                           
    #                34, 45, 40, 15, 15, 60, 80, 26, 18, 37, 50, 35, 12, 12, 25]]).T                                     
       

    print(data)

    years = np.arange(1845, 1905, 2)
                                                       
    function(data, years, time_length)

