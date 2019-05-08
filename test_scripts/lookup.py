#!/usr/bin/python

# filename: hebi_test_script.py
#
# by: Abhay Gupta
# date: 05/08/19
#
# description: test various functions described in the documentation

from time import sleep
import hebi

lookup = hebi.Lookup()
# Give the Lookup process 2 seconds to discover modules
sleep(2)
print('Modules found on network:')
for entry in lookup.entrylist:
	print('{0} | {1}'.format(entry.family, entry.name))


# Create a group from a set of names
group = lookup.get_group_from_names(['Family'], ['name1', 'name2'])

import numpy as np

# Providing '*' as the family selects all modules
group = lookup.get_group_from_family('*')

print(group)

# Create a numpy array filled with zeros
efforts = np.zeros(group.size)+10

# Command all modules in a group with this zero force or effort command
group_command = hebi.GroupCommand(group.size)
group.command_lifetime = 5000.0 # set length of time of command (ms)

#set output
#group_command.effort = efforts #specify effort
#group_command.position = efforts #specify effort
#group_command.velocity = efforts #specify effort


# Command must be sent in loop at a faster rate than the lifetime in order to remain in effect.
stop_loop = 0
while not (stop_loop):
		group.send_command(group_command)
		sleep(0.05)
		stop_loop = 1


# Open-loop controller commanding sine waves with different frequencies
import math as m
w = np.array([m.pi*2.0], dtype=np.float64)
w_t = np.empty(1, dtype=np.float64)

t = 0.0
dt = 0.1
group.command_lifetime = dt # set length of time of command (ms)

# Best practice is to allocate this once, not every loop iteration
group_feedback = hebi.GroupFeedback(group.size)
group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)

# This effectively limits the loop below to 200Hz
group.feedback_frequency = 200.0
output = np.empty(0)

stop_loop = 0
while not (stop_loop):
		
		group_feedback = group.get_next_feedback(reuse_fbk=group_feedback)
		w_t = np.multiply(w,t)
		#group_command.velocity = np.cos(w_t)
		#group_command.velocity = np.sin(w_t)
		group_command.effort = 0.05 #0.001*np.cos(w_t)
		group.send_command(group_command)

		print('input effort:', group_command.effort)

		positions = group_feedback.position
		print('Position Feedback:\n{0}'.format(positions))

		output = np.append(output, positions)


		#sleep(dt)
		t = t + dt
		if t >= 2:
				stop_loop = 1



group_command.effort = np.nan #0.001*np.cos(w_t)h
group.send_command(group_command)

import matplotlib.pyplot as plt

plt.plot(output)
plt.show()

print(output)





