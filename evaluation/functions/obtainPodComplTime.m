function [ startTime, startRun, stopTime, conCreateTime, complTime ] = obtainPodComplTime(givenPodName,  podnames,  statuses,steps )
  
  PENDING = 'Pending';
  RUNNING = 'Running';
  COMPLETED = 'Completed';
  
  complTime = -1;
  startTime = -1;
  startRun = -1;
  conCreateTime = -1;
  stopTime = -1;

  for iTime = 1:length(steps)
    if strcmp(givenPodName, podnames{iTime}) && ~strcmp(statuses{iTime}, PENDING)
      if (startTime < 0)
        startTime = steps(iTime);
      end
      if startRun < 0 && strcmp(statuses{iTime}, RUNNING)
        startRun = steps(iTime);
        conCreateTime = startRun - startTime;
      end

      if stopTime< 0 && strcmp(statuses{iTime}, COMPLETED)
        stopTime = steps(iTime);
        complTime = stopTime - startTime;
      end
    end
  end

end

