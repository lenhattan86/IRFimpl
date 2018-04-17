clear; clc; close all;
addpath('functions');
common_settings;


%%
userNames = {'user1', 'user2'};
%% 
%% 
% folder = 'FDRF';
% folder = '.';
MAIN_FOLDER = 'motivation';
subfolder = 'naiveDRF';
TAR_FILE = [subfolder '.tar.gz'];
folder = [MAIN_FOLDER '/' subfolder];
try
   rmdir(folder,'s');
catch fileIO   
end
untar([MAIN_FOLDER '/' TAR_FILE], [MAIN_FOLDER]);

%%
interval = 1;
stopTime = 1000;
times = interval:interval:stopTime;
userUsages = zeros(stopTime, length(userNames));

filename = [folder '/pods.csv'];
[datetimes, steps, users, podnames,statuses] = importUserInfo(filename);
  
for iUser = 1:length(userNames) 
  ids = find(strcmp(users(1:length(users)-1),userNames{iUser}));
  mSteps = steps(ids);
  mUsers = users(ids);
  mDatetimes = datetimes(ids);
  mPodNames=podnames(ids);
  mStatuses=statuses(ids);
  
  [mSteps,sortedIds] = sort(mSteps,'ascend');
  mUsers = mUsers(sortedIds);
  mDatetimes = mDatetimes(sortedIds);
  mPodNames = mPodNames(sortedIds);
  mStatuses = mStatuses(sortedIds);
  
  start_time_idx = 1;
  for iTime = 1:length(times)
    numContainer = 0;
    for timeIdx = start_time_idx:length(mSteps)-1   
      if mSteps(timeIdx) > times(iTime)
        end_time_idx = timeIdx;
        break
      end
      if(strcmp(mStatuses{timeIdx},'Running') ...
        || strcmp(mStatuses{timeIdx},'ContainerCreating'))
        numContainer = numContainer+ 1;
      end
    end

    userUsages(iTime, iUser) = numContainer;
    start_time_idx = end_time_idx;
  end
end

%%
try
   rmdir(folder,'s');
catch fileIO
   error('no directories to be deleted');
end
%%
bar(userUsages, 1.0, 'stacked');
xlabel('seconds');
ylabel('number of containers');
strLegend = {'user1', 'user2'};
legend(strLegend);


