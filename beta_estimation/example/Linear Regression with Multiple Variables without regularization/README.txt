Jason Joseph Rebello
Carnegie Mellon University (Jan 2012 - May 2013) 
Masters in Electrical & Computer Engineering
 
Linear Regression with Multiple Variables (Without Regularization)
Run LinearRegression.m
This program uses linear regression with multiple variables to predict
housing prices. First feature (Column 1) is the size of the houses in sq
feet. Second feature (Column 2) is no. of bedrooms. Housing prices is in 
(Col 3).

First the data is loaded. The first two columns in dataHousePrices
contain the two features whereas the third column contains the prices.

Theta is first calculated using the normal equation. In general
theta = ((X'X)^-1)X'y.
By calculating theta this way, we can predict the housing prices and compare it to the price obtained via gradient descent.

Before calculating the cost function and gradient descent we need to normalize the features by calling featureNormalize. This is because when we plot the data,do not want skewed contours. The size of the houses are of the order 1000's while the number of bedrooms are of the order 10's.
In featureNormalize we just calculate the mean and standard deviation for each feature using all the training examples. The formula for feature normalization is given by :
particular feature normalized = (feature unnormalized - mean)/(std dev)
In place of standard deviation we can also use (max value - min value).

Use gradientDescent to learn the parameters theta in order to find the best fit line. In order to calculate cost function we need to initialize the parameters theta to 0 and also add a column of 1's to X in order to account for x0. X is now of (m x (d+1)) dimensions where d is the number of features. The learning rate alpha and number of iterations is also provided. Alpha should not be too small or it will take too long to reach the minimum. If Alpha is very large, it will tend to overshoot and not reach the minimum.

The gradient descent is calculated as follows :
For each theta:
thetaNew(i) = thetaOld(i) - (alpha/m)* sum of [(hyp(x)-y)*particular feature corresponding to that theta(i)];
where hyp(x) = theta'X
Update all thetas simultaneously.

Calculate cost using the cost function. The cost should decrease with every iteration.
Formula for cost:
cost = (1/(2m))*sum((X*theta - y).^2);


