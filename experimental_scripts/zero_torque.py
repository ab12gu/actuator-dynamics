#!/usr/bin/python

# filename: hebi_test_script.py
#
# by: Abhay Gupta
# date: 05/08/19
#
# description: test various functions described in the documentation

import hebi
from time import sleep, time
import numpy as np
import pdb
import math as m

def check_actuator():
    """
    Check if actuator is connected

    return: none
    """
    all_devices = hebi.Lookup() # shows broadcast number, class containing modules
    sleep(2) # give 2 seconds to discover modules

    print('Modules found on network:')

    for entry in all_devices.entrylist:
        print('{0} | {1}'.format(entry.family, entry.name))

    return all_devices

def call_actuators(all_devices):
    """
    Call actuator used for system. Currently controls all actuators at once.
    
    param all_devices: all actuators connected to computer

    return: actuator being controlled
    """
    grouped_actuators = all_devices.get_group_from_family('*')  # Providing '*' as the family selects all modules

    return grouped_actuators

def command_actuator(group, w, command_time, feedback_freq, tf, step):
    """ 
    Send a command to the motor for a specified time
    
    param group: actuators being commanded
    param w: system frequency

    return position, velocity and effort
    """
    # set feedback
    group.command_lifetime = command_time # set length of time of command (ms)
    group.feedback_frequency = feedback_freq # This effectively limits the loop below to 200Hz

    group_command = hebi.GroupCommand(group.size)   # Commands all modules in a group
    group_feedback = hebi.GroupFeedback(group.size) # Reads feedback
    
    # Open-loop controller commanding sine waves with different frequencies
    t0 = 0.0            
    dt = 0.1
    t = t0

    # Initialize all array
    pos = np.empty(0)
    vel = np.empty(0)
    eff = np.empty(0)
    pwm = np.empty(0)

    start = time()
 
    # Run motor for specified time
    while (t < tf-2.0):

        # measure variables
        group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)
        #w_t = np.multiply(w,t)
        #print('input effort:', group_command.effort)
        #print('Position Feedback:\n{0}'.format(group_feedback.position))

        pos = np.append(pos, group_feedback.position)
        vel = np.append(vel, group_feedback.velocity)
        eff = np.append(eff, group_feedback.effort)
        pwm = np.append(pwm, group_feedback.pwm_command)

        #sleep(dt)
        t = time()-start

    # reset all the pid gains
    #group_command.control_strategy = 'directpwm' 
    print('strategy', group_command.control_strategy)

    # send step response of torque
    group_command.effort = step #0.001*np.cos(w_t)
    #group_command.pwm_command = step #0.001*np.cos(w_t)
    
    group.send_command(group_command)

    # Run motor for specified time
    while (t < tf):

        # measure variables
        group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)
        #w_t = np.multiply(w,t)
        #print('input effort:', group_command.effort)
        #print('Position Feedback:\n{0}'.format(group_feedback.position))

        pos = np.append(pos, group_feedback.position)
        vel = np.append(vel, group_feedback.velocity)
        eff = np.append(eff, group_feedback.effort)
        pwm = np.append(pwm, group_feedback.pwm_command)

        #sleep(dt)
        t = time()-start

    group_command.effort = np.nan #0.001*np.cos(w_t)h
    group.send_command(group_command)

    return pos, vel, eff, pwm

def plot(pos, vel, eff, pwm):
    import matplotlib.pyplot as plt

    plt.subplot(411)
    plt.plot(pos)
    plt.ylabel('position')
    plt.subplot(412)
    plt.plot(vel)
    plt.ylabel('velocity')
    plt.subplot(413)
    plt.plot(eff)
    plt.ylabel('torque (N m)')
    plt.subplot(414)
    plt.plot(pwm)
    plt.ylabel('PWM -  non-dimensionalized')
    plt.xlabel('time')
    plt.show()

    return

def export_data(pwm, eff, vel,  runtime, fn_input):

    import pickle

    file_location = './../data/'
    filename = 'input' + str(fn_input) + '.pkl'

    output_file = file_location + filename
    
    with open(output_file, 'wb') as f:
        pickle.dump([pwm, eff, vel, runtime, fn_input], f)    
    
    return

if __name__ == "__main__":

    # get actuators
    all_devices = check_actuator() # check if actuators are connected
    grouped_actuators = call_actuators(all_devices) # call the actuator 

    space = np.arange(-1.9, 1.2, 0.1)

    for step in space:
        # set variables
        # command_time must be sent in loop at a faster rate than the lifetime in order to remain in effect.

        command_time = 5000.0 # time command is run (ms) (zero time gives inf command)
        feedback_freq = 300.0 # time in hz
        runtime = 4.0
        #step = 2.0

        # set open-loop input
        w = np.array([m.pi*2.0], dtype=np.float64)
        pos, vel, eff, pwm = command_actuator(grouped_actuators, w, command_time, feedback_freq, runtime, step)

        #plot(pos, vel, eff, pwm)

        export_data(pwm, eff, vel, runtime, step)
    

