clc; clear; close all;
%%
load carbig
X = [Horsepower,Weight, Horsepower];
y = MPG;
modelfun = @(b,x)b(1) + b(2)*x(:,1).^b(3) + ...
    b(4)*x(:,2).^b(5) + b(6)*x(:,3).^b(7);
beta0 = [-50 500 -1 500 -1 1 1];
mdl = fitnlm(X,y,modelfun,beta0);

%%
modelfun(ones(2,2))