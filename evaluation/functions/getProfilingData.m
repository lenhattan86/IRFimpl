function [ rcpus, rgpus, cpus, gpus ] = getProfilingData( filename, jobNames, dataLen, rBachtNums, ...
  CPU, MEM, batchSize, NUM_THREADs, kArray, jobPrefix)
rcpus=zeros(length(jobNames), dataLen, length(kArray));
rgpus=zeros(length(jobNames), dataLen, length(kArray));

cpus=zeros(length(jobNames), dataLen, length(kArray));
gpus=zeros(length(jobNames), dataLen, length(kArray));

if exist(filename, 'file')
    text = fileread(filename);  % Open the file
    text = text(5: length(text)-1);
    textArray = strsplit(text);
    
    for iJobName = 1:length(jobNames)
      for iJob = 0:dataLen-1
         for iK = 1:length(kArray)
            commonName = [num2str(CPU) '-' num2str(MEM) '-' num2str(batchSize(iJobName)) '-' num2str(NUM_THREADs) ...
              '-' num2str(kArray(iK)) '-' num2str(iJob) ];
            fNameCpu = [jobPrefix jobNames{iJobName} '-cpu-' commonName ];
            fNameGpu = [jobPrefix jobNames{iJobName} '-gpu-' commonName ];
            str_cpu_rcpu = [fNameCpu '-rcpu' ];            
            str_gpu_rgpu = [fNameGpu '-rgpu' ];
            
            for iElement = 1:length(textArray)
              mText = textArray{iElement};
              mStrs = strsplit(mText,':');
              stDuration = mStrs{2};
              
              hour = 0; min = 0; sec = 0;
              strRemain = stDuration;
              strHour = strsplit(strRemain,'h');
              if length(strHour) > 1
                hour = str2num(strHour{1});
                strRemain = strHour{2};
              else
                strRemain = strHour{1};
              end
              strMin = strsplit(strRemain,'m');
              if length(strMin) > 1
                min = str2num(strMin{1});
                strRemain = strMin{2};
              else
                strRemain = strMin{1};
              end                            
              strSec = strsplit(strRemain,'s');                                          
              sec = str2num(strSec{1});
              
              dur = hour * 3600 + min * 60 + sec;
              
              % cpu
              if strcmp(mStrs{1},str_cpu_rcpu) 
                rcpus(iJobName, iJob+1, iK) = dur;
              elseif strcmp(mStrs{1},str_gpu_rgpu)
                rgpus(iJobName, iJob+1, iK) = dur;
              elseif strcmp(mStrs{1},fNameCpu)
                cpus(iJobName, iJob+1, iK) = dur;
              elseif strcmp(mStrs{1},fNameGpu)              
                gpus(iJobName, iJob+1, iK) = dur;
              end
            end
         end
      end
    end
    
    
else
  disp(['cannot open file ' filename]);   
end

