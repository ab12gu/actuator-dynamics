# filename: system_dyanmics.py
#
# by: Abhay Gupta & Karthik Subramanya Karvaje
# date: 07/12/19
#
# description: form plots of system dynamics

import time
from time import sleep
import hebi
import numpy as np
import math as m
import csv
import random

def main():
    '''
    description: step function of system
    position of actuator shaft follows a sine wave path
    parameters: none
    returns: none
    '''

    # Look up actuator
    lookup = hebi.Lookup()
    group = lookup.get_group_from_family('*') # '*' selects all modules

    # Command all modules in a group with this zero force or effort command
    group_command = hebi.GroupCommand(group.size)
    group_feedback = hebi.GroupFeedback(group.size)

    group.feedback_frequency = 200.0    # This effectively limits the loop below to 200Hz
    #group.feedback_frequency = 50.0    # This effectively limits the loop below to 200Hz

    ## Open-loop controller ----------------------------------------------------------------------

    w = -1*m.pi*5.0 # frequency (to control the velocity)

    #setting initial positipon to 0
    group_command.position = 0
    time.sleep(2)
    #t0, dt, tf = 0.0, 0.1, 2.0 # initial time & step size
    t0, dt, tf = 0.0, 0.03, 15.0 # initial time & step size
    time_range = np.arange(t0,tf,dt)
    group.command_lifetime = dt # set length of time of command (ms)

    # Initialize all array
    pos, vel, defl, eff, pwm = [], [], [], [], []
    stop_loop = 0
    t = t0
    
    # First restart poistion
    while(0):
        group.command_lifetime = 200.0 # set length of time of command (ms)
        group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)
        group_command.effort == 1.0
        group.send_command(group_command)
        sleep(2)


    group.command_lifetime = dt # set length of time of command (ms)

    sleep(10)

    start_time = time.time()

    # Run motor for specified time
    for i in time_range:
        
        group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)
        w_t = np.multiply(w,t)
        #group_command.velocity = 2*np.sin(w_t)
        #I am generating a random input signal (random gaussian input)
        #group_command.velocity =  random.gauss(0,0.6)
        #group_command.velocity =  random.gammavariate(0.2, 1.8)
        group_command.velocity =  random.uniform(-3,3)
        group.send_command(group_command)

        print('input effort:', group_command.effort)

        positions = group_feedback.position
        velocity = group_feedback.velocity
        deflection = group_feedback.deflection
        effort = group_feedback.effort
        pwm_command = group_feedback.pwm_command
        print('Position Feedback:\n{0}'.format(positions))

        pos = np.append(pos, positions)
        vel = np.append(vel, velocity)
        defl = np.append(defl, deflection)
        eff = np.append(eff, effort)
        pwm = np.append(pwm, pwm_command)

        '''with open('motor.csv', 'w') as csvfile:
            fieldnames = ['pos', 'vel', 'eff']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'pos': pos, 'vel': vel, 'eff':eff})'''
            
        row = [ pos, vel, defl, eff, pwm]
        #print ('row:', row)
        sleep(dt)
        t = t + dt
        
    end_time = time.time()

    print('Time: ', end_time-start_time)
    print ('pos', pos)
    print ('vel', vel)
    print ('deflection', defl)
    print ('eff', eff)
    print ('pwm', pwm)

    
    with open('motor.csv', 'w') as csvfile:
        fieldnames = ['pos', 'vel','defl', 'eff', 'pwm']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'pos': pos, 'vel': vel, 'defl':defl, 'eff':eff, 'pwm':pwm})
    
    group_command.velocity = np.nan #0.001*np.cos(w_t)h
    group.send_command(group_command)

    import matplotlib.pyplot as plt

#    row = []
#I am also importing the deflection data to look for any correlations.

    plt.subplot(511)
    plt.plot(pos)
    plt.ylabel('position')
    plt.subplot(512)
    plt.plot(vel)
    plt.ylabel('velocity')
    plt.subplot(513)
    plt.plot(eff)
    plt.ylabel('torque (N m)')
    plt.subplot(514)
    plt.plot(defl)
    plt.ylabel('deflection')
    plt.subplot(515)
    plt.plot(pwm)
    plt.ylabel('pwm')
    plt.xlabel('time')
    plt.show()


if __name__ == '__main__':
    main()

