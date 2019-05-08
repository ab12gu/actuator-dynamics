close all; clear all; clc;

% create a mimo system and determine the response

% define variables
Jm = 1;
Bm = 1;
Ks = 1;
Jl = 1;
Bl = 1;
N = 1;

tf{s}

num = {1 1 1 [1 1] ;...
        1 1 1 1}
den = {[1 2 2]}
H = tf(num,den,'inputn',{'Motor Angle' 'Spring Angle', 'Load Angle', 'Output Torque'},...
               'outputn',{'Motor Torque' 'Load Torque'},...
               'variable','s')
                
step(H)