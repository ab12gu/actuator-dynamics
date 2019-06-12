# filename: motor_model.py
#
# by: Abhay Gupta
# date: 05.15.19
# desc: model of the motor dynamics

from scipy import signal
from control import TransferFunction as tf
import numpy as np

Jm = 1
Bm = 1
Ks = 1
Jl = 1
Bl = 1
N = 1

Pm = tf(1, [Jm,Bm, 0])
Ps = tf(1, Ks)
Pl = tf(1, [Jl, Bl, 0])

D = Pl + N**-2 * Pm + Ks**-1

J = np.array([
    [Pm*(Pl+Ks**-1)/D, N**-1*Pm*Pl/D],
    [N**-1*Pm*Pl/D, Pl*(N**-2*Pm+Ks**-1)/D],
    [N**-1*Pm*Ks/D, Pl*Ks**-1/D],
    [N**-1*Pm/D, Pl/D]])

print('hello', J)


