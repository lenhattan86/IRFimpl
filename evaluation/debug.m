%%
filename='FDRF/user1.csv';
podName='user1-2';
[datetimes, steps, users, podnames,statuses] = importUserInfo(filename);
[ startTime, startRun, stopTime, conCreateTime, complTime] = obtainPodComplTime(podName, podnames, statuses, steps, datetimes);
[startRun stopTime]
%%
podName='user1-3';
[datetimes, steps, users, podnames,statuses] = importUserInfo(filename);
[ startTime, startRun, stopTime, conCreateTime, complTime] = obtainPodComplTime(podName, podnames, statuses, steps, datetimes);
[startRun stopTime]
%%
podName='user1-8';
[datetimes, steps, users, podnames,statuses] = importUserInfo(filename);
[ startTime, startRun, stopTime, conCreateTime, complTime] = obtainPodComplTime(podName, podnames, statuses, steps, datetimes);
[startRun stopTime]
