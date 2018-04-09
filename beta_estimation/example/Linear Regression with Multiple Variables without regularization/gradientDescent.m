function [theta, CostHistory] = gradientDescent(X, theta, y, alpha, numIters)
% Gradient Descent is used to learn the parameters theta in order to fit a
% straight line to the points.

% Initialize values
m = length(y); % number of training examples
CostHistory = zeros(numIters, 1);
thetaLen = length(theta);
tempVal = theta; % Just a temporary variable to store theta values.

for iter=1:numIters
    temp = (X*theta - y);
    
    for i=1:thetaLen
        tempVal(i,1) = sum(temp.*X(:,i));
    end
    
    theta = theta - (alpha/m)*tempVal;
    
    CostHistory(iter,1) = cost(X,y,theta);
 
end
