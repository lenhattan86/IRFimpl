function thetaNormEqn = NormalEquation(XNormEqn,y)
% This calculates the values of theta using the normal equation

thetaNormEqn = pinv((XNormEqn')*XNormEqn)*XNormEqn'*y;
