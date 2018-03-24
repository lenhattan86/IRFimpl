%% init
clear; close all; clc;
addpath('functions');
common_settings;
%% parameters
folder = 'profiling';
% csv_file =  'alexnet_3.26.csv';
csv_file =  'alexnet_1.14.csv';
%% download the csv file
% system('scp cc@p100:~/IRFimpl/experiments/profiling/alexnet/alexnet.csv /home/tanle/projects/IRFimpl/evaluation/profiling/' );
%% 

[datetimes,steps,users,podnames,statuses] = importUserInfo([folder '/' csv_file]);

uniquePodnames = cell(1,0);
iPod = 0;

cpuComplTimes = [];
cpuOverheadTimes = [];
gpuComplTimes = [];
gpuOverheadTimes = [];

%%
% str = '2018-03-22 21:27:47.549922';
% dt = datetime(str(1:length(str)-7),'InputFormat','yyyy-MM-dd HH:mm:ss');
%%
[ startTime, startRunTime, stopTime, conCreateTime, complTime ] = obtainPodComplTime('job-alexnet-cpu-0', podnames, statuses, steps, datetimes);
%%
for i = 1:length(steps)
  podName = podnames{i};
  if (~any(strcmp(uniquePodnames,podName)))
    iPod=iPod + 1;
    uniquePodnames{iPod} = podName;
    [ startTimes(iPod), startRuns(iPod), stopTimes(iPod), conCreateTimes(iPod), complTimes(iPod) ] ...
      = obtainPodComplTime(podName, podnames, statuses, steps, datetimes);
    
    if ~isempty(strfind(podName,'cpu'))
       id = length(cpuComplTimes)+1;
      cpuComplTimes(id) = complTimes(iPod);
      cpuOverheadTimes(id) = conCreateTimes(iPod);
    end
    if ~isempty(strfind(podName,'gpu'))
      id = length(gpuComplTimes)+1;
      gpuComplTimes(id) = complTimes(iPod);
      gpuOverheadTimes(id) = conCreateTimes(iPod);
    end
  end
end

%%
mean(cpuComplTimes)
mean(gpuComplTimes)
speedUpRate = mean(cpuComplTimes)/mean(gpuComplTimes)
mean(cpuOverheadTimes);
mean(gpuOverheadTimes);