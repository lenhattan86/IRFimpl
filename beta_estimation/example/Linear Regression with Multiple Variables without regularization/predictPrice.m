function pr = predictPrice(theta, eg1, mu, stddev)

% This function is used to predict the house price for a particular example
% via the theta's obtained from gradient descent

% First need to normalize the values of the features
eg1 = eg1(:,2:end);
eg1 = ((eg1-mu)./stddev);

eg1 = [ones(size(eg1,1),1) eg1];
pr = eg1*theta;