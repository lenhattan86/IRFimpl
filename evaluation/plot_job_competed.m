clear; clc; close all;

%%
stopTime = 600;
folder  = '.';
methods ={'DRF','FDRF'};
strUsers = {'user1','user2'};

job_completed = zeros(length(strUsers), length(methods));
for iMethod = 1:length(methods)
  method = methods{iMethod};
  filename = [folder '/' method '/pods.csv'];
  [datetimes, steps, users, podnames,statuses] = importUserInfo(filename);  
  
  stepIds = (steps==stopTime);
  steps = steps(stepIds);
  users = users(stepIds);
  statuses = statuses(stepIds);
%   podnames = podnames(stepIds);
  
  for iUser = 1:length(strUsers)
    user = strUsers{iUser};
    ids = strcmp(users, user);
    mStatuses = statuses(ids);
    job_completed(iUser,iMethod) = sum(strcmp(mStatuses,'Completed'));
  end  
end

%%             
bar(job_completed, 'group');
ylabel('job completed');
xlabel('Users');
strLegend={'DRF','FDRF'};
legend(strLegend);
