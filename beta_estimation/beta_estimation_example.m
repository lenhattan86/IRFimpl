clear; clc; close all;
%% 
nFeatures = 1;
nTrain = 3;
XTrain = ones(nTrain, nFeatures+1);
W       = zeros(nFeatures + 1, nTrain);
%% Features
% 
iFeature = 1;


GPUs = [0, 1, 0];




iFeature = iFeature +
1;
XTrain(:,iFeature) = GPUs;

CPUs        =   [1, 2, 3];
iFeature = iFeature + 1;
XTrain(:,iFeature) = CPUs;

Memory      =   [3, 4, 5];
iFeature = iFeature + 1;
XTrain(:,iFeature) = Memory;

num_threads =   [4, 4, 4];
iFeature = iFeature + 1;
XTrain(:,iFeature) = num_threads;

batch_sizes = [16, 32, 64];
iFeature = iFeature + 1;
XTrain(:,iFeature) = batch_sizes;

batch_nums  = [100, 200, 300];
iFeature = iFeature + 1;
XTrain(:,iFeature) = batch_nums;

Models      = ['alexnet', 'vgg16', 'vgg16'];
AllModels   = ['alexnet', 'vgg16', 'vgg16','resnet50'];
iFeature = iFeature + 1;
XTrain(:,iFeature) = batch_nums;

frameworks  = ['Tensorflow', 'Tensorflow', 'Tensorflow'];


YTrain = [10, 20, 30]';

%% compute W
W = XTrain\YTrain;
W_2 = transpose(YTrain) * XTrain*(transpose(XTrain)*XTrain)^(-1);

%% 
YTest= XTrain*W;
%% 

