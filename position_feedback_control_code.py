#!/usr/bin/env python3
# written by Karthik Subramanya Karvaje
# date: 1st July 2019

''' This code will keep the position
of the shaft at a constant level
with respect to the ground no matter
what orientation the actuator has'''

import hebi
import math
from time import sleep, time

lookup = hebi.Lookup()

# Wait 2 seconds for the module list to populate
sleep(2.0)

family_name = "X5-9"
module_name = "Actuator1"

group = lookup.get_group_from_names([family_name], [module_name])

if group is None:
  print('Group not found! Check that the family and name of a module on the network')
  print('matches what is given in the source file.')
  exit(1)

# This is by default 100 Hz.
#group.feedback_frequency = 1000.0
group_command  = hebi.GroupCommand(group.size)
group_feedback = hebi.GroupFeedback(group.size)

# Start logging in the background
group.start_log('logs')

print('  Move the module to make the output move...')

duration = 60.0 # [sec]
start = time()
t = time() - start

while t < duration:
  # Even though we don't use the feedback, getting feedback conveniently
  # limits the loop rate to the feedback frequency
  group.get_next_feedback(reuse_fbk=group_feedback)
  t = time() - start

  acc=group_feedback.accelerometer
  myacc=acc[0].tolist()
  g=myacc[1]
  h=myacc[0]
  #print(g)
  if -9.8<g<9.81:
      theta=math.acos(g/9.81)
      print(math.acos(g/9.81))
      # Command a position that counters the rotation of actuator around the z-axis (same axis as the output)
      if h>=0:
          group_command.position = -theta
          group.send_command(group_command)
      if h<0:
          group_command.position = theta
          group.send_command(group_command)
  else:
      print ('g>9.8')

# Stop logging. `log_file` contains the contents of the file
log_file = group.stop_log()
