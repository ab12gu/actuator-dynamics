# filename: system_dyanmics.py
#
# by: Abhay Gupta
# date: 05/08/19
#
# description: form plots of system dynamics


import time
from time import sleep
import hebi
import numpy as np
import math as m

def main():
    '''
    description: step function of system

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

    ## Open-loop controller ----------------------------------------------------------------------

    w = -1.0*m.pi*2.0 # frequency
    t0, dt, tf = 0.0, 0.1, 2.0 # initial time & step size
    time_range = np.arange(t0,tf,dt)
    group.command_lifetime = dt # set length of time of command (ms)

    # Initialize all array
    pos, vel, eff = [], [], []
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
        group_command.velocity = 0.5*np.sin(w_t)
        group.send_command(group_command)

        print('input effort:', group_command.effort)

        positions = group_feedback.position
        velocity = group_feedback.velocity
        effort = group_feedback.effort
        print('Position Feedback:\n{0}'.format(positions))

        pos = np.append(pos, positions)
        vel = np.append(vel, velocity)
        eff = np.append(eff, effort)

        sleep(dt)
        t = t + dt

    end_time = time.time()

    print('Time: ', end_time-start_time)

    group_command.velocity = np.nan #0.001*np.cos(w_t)h
    group.send_command(group_command)

    import matplotlib.pyplot as plt

    plt.subplot(311)
    plt.plot(pos)
    plt.ylabel('position')
    plt.subplot(312)
    plt.plot(vel)
    plt.ylabel('velocity')
    plt.subplot(313)
    plt.plot(eff)
    plt.ylabel('torque (N m)')
    plt.xlabel('time')
    plt.show()


if __name__ == '__main__':
    main()



