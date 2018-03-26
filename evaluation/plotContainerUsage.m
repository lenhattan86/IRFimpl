clear; clc; close all;
addpath('functions');
common_settings;

%%
userNames = {'user1', 'user2'};
% folder = 'DRF';
folder = 'FDRF';
interval = 1;
stopTime = 1000;
times = interval:interval:stopTime;
userUsages = zeros(stopTime, length(userNames));

for iUser = 1:length(userNames)
  filename = [folder '/' userNames{iUser} '.csv'];
  [datetimes, steps, users, podnames,statuses] = importUserInfo(filename);
  
  start_time_idx = 1;
  for iTime = 1:length(times)
    
    numContainer = 0;
    for timeIdx = start_time_idx:length(steps)-1   
      if steps(timeIdx) > times(iTime)
        end_time_idx = timeIdx;
        break
      end
      if(strcmp(statuses{timeIdx},'Running') ...
        || strcmp(statuses{timeIdx},'ContainerCreating'))
        numContainer = numContainer+ 1;
      end
    end
    
    userUsages(iTime, iUser) = numContainer;
    start_time_idx = end_time_idx;
  end
end
%%
bar(userUsages, 1.0, 'stacked');
xlabel('time steps (each step > 1 secs)');
ylabel('number of containers');
strLegend = {'user1', 'user2'};
legend(strLegend);


