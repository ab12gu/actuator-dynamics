close all; clc; clear all

m = 1;
k = 1;
b = 0.2;
F = 1;

A = [0 1; -k/m -b/m];
B = [0 1/m]';
C = [1 0];
D = [0];

sys = ss(A,B,C,D)



t = 0:0.1:2;
u = zeros(1,size(t,2))+1
x0 = [0,0];
figure(3)
lsim(sys,u,t, x0)
