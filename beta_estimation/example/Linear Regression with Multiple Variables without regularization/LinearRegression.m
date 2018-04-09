% Jason Joseph Rebello
% Carnegie Mellon University (Jan 2012 - May 2013) 
% Masters in Electrical & Computer Engineering
% Linear Regression with Multiple Variables (Without Regularization)

% This program uses linear regression with multiple variables to predict
% housing prices. First feature (Column 1) is the size of the houses in sq
% feet. Second feature (Column 2) is no. of bedrooms. Housing prices is in 
% (Col 3). Please read the 'README.txt' file while executing the code. 

clear all;
clc;
close all;

%% Load Data and Initialize Variables
fprintf('Loading data and initializing variables');
t = cputime;
data = load('dataHousePrices.txt');
X = data(:, 1:2); % Features
y = data(:, 3); % Housing Prices
m = length(y); % Number of training examples
d = size(X,2); % Number of features.
theta = zeros(d+1,1); % Initialize thetas to zero.
alpha = 0.03; % Learning rate
numIters = 1000; % How long gradient descent should run for
fprintf('...done\n');

%% Calculate Theta from Normal Equation
% This serves as a good reference to make sure that you are getting the
% right price in the end. Note for Normal equation we need to add
% the column of 1's to X. However we do not need to normalize the features.
% I will be using XNormEqn to store X in order to avoid it replacing
% the X used in gradient descent.
fprintf('Calculating theta via normal equation');
XNormEqn = [ones(m,1) X];
thetaNormEqn = NormalEquation(XNormEqn,y);
fprintf('...done\n');

%% Feature Normalization
fprintf('Normalizing Features for gradient descent');
[X, mu, stddev] = featureNormalize(X);
fprintf('...done\n');

%% Compute the Cost Function
fprintf('Calculating theta via gradient descent');
X = [ones(m,1) X]; % Add a col of 1's for the x0 terms

[theta, CostHistory] = gradientDescent(X, theta, y, alpha, numIters);
fprintf('...done\n');

%% Prdeiction of house prices

fprintf('Predicting the price of the following house\n');
fprintf('Sq ft = , No of bedrooms = \n');
eg1 = [1 1320 2];
disp(eg1(:,2:end))
fprintf('Price via Normal Equation:');
price = (eg1)*thetaNormEqn;
disp(price);
clear price;
fprintf('\n');
fprintf('Price via Gradient Descent:');
price = predictPrice(theta,eg1,mu,stddev);
disp(price);
fprintf('Total time in seconds taken to run program\n');
disp(cputime-t);