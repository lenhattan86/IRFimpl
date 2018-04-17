function [ startTime, startRunTime, stopTime, conCreateTime, complTime ] = ...
  obtainPodComplTime(givenPodName,  podnames,  statuses,  steps, datetimes )
  
  PENDING = 'Pending';
  RUNNING = 'Running';
  COMPLETED = 'Completed';
  OOM = 'OOMKilled';
  
  complTime = -1;
  startStep = -1;
  startRunStep = -1;
  conCreateTime = -1;
  stopStep = -1;
  
  startTime = -1;
  stopTime = -1;
  startRunTime = -1;

  for iTime = 1:length(steps)
    if strcmp(givenPodName, podnames{iTime}) && ~strcmp(statuses{iTime}, PENDING)
      dt = datetimes{iTime}; 
      if (startStep < 0)
        startStep = steps(iTime);        
        startTime = datetime(dt(1:length(dt)-7),'InputFormat','yyyy-MM-dd HH:mm:ss');
      end
      if startRunStep < 0 && strcmp(statuses{iTime}, RUNNING)
        startRunStep = steps(iTime);
        startRunTime = datetime(dt(1:length(dt)-7),'InputFormat','yyyy-MM-dd HH:mm:ss');
        conCreateTime = seconds(startRunTime - startTime);
      end

      if stopStep< 0 && strcmp(statuses{iTime}, COMPLETED)
        stopStep = steps(iTime);
        stopTime = datetime(dt(1:length(dt)-7),'InputFormat','yyyy-MM-dd HH:mm:ss');
        complTime = seconds(stopTime - startTime);
      end
    end
  end

end

