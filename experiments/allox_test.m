clear; close all; clc;

%%

beta = 5;
p_c = 2;
p_g = 20;
cvx_begin
    variables x  y
    maximize(x + beta*y );
    subject to
        x*p_c + y*p_g <= 1;
        x >= 0;
        y >= 0;
cvx_end
% x = 1/p_c & y= 0 if p_g/p_c < beta
% x = 0 & y= 1/p_g if p_g/p_c > beta
%%