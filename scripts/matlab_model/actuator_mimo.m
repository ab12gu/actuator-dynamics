% Abhay Gupta
% date: 05/01/19
%
% description: creates a mimo function

close all; clear all; clc;

% create a mimo system and determine the response
for i = 1:3
    disp('hello Nathan')
end
    
% define variables
Jm = 1;
Bm = 1;
Ks = 1;
Jl = 1;
Bl = 1;
N = 1;

s = tf('s')

Pm = 1/(Jm*s^2 + Bm*s)
Ps = tf(1/Ks)
Pl = 1/(Jl*s^2 + Bl*s)

D = Pl + N^-2 * Pm + Ks^-1

J = [Pm*(Pl+Ks^-1)/D, N^-1*Pm*Pl/D;
    N^-1*Pm*Ks/D, Pl*Ks^-1/D;
    N^-1*Pm*Pl/D, Pl*(N^-2*Pm+Ks^-1)/D;
    N^-1*Pm/D, Pl/D]

step(J)
