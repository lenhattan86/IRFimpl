addpath('func');
common_settings;
figIdx = 0;

output_sufix = 'short/'; STEP_TIME = 1.0; 

% fig_path = ['../../EuroSys17/fig/'];

is_printed = true;
numOfNodes = 40;
MAX_CPU = numOfNodes*32;
MAX_MEM = numOfNodes*64;
GB = 1024;
extra='';

num_batch_queues = 8;
num_interactive_queue = 1;
num_queues = num_batch_queues + num_interactive_queue;

workload='BB';

plots = [true false]; %DRF, DRF-W, Strict, SpeedFair

colorBars = cell(num_queues,1);
for i=1:num_queues
  colorBars{i} = colorb8i1{i};
end

%%
if plots(1) 
  START_TIME = 3500; END_TIME = 500+START_TIME;    
  
  queues = cell(1,num_queues);
  lengendQueuesStr = cell(1,num_queues);
  for i=1:num_interactive_queue
      queues{i} = ['bursty' int2str(i-1)];
      lengendQueuesStr{i} = [strLQ '-' int2str(i-1)];
  end
  for j=1:num_batch_queues
      queues{num_interactive_queue+j} = ['batch' int2str(j-1)];
      lengendQueuesStr{num_interactive_queue+j} = [strTQ '-' int2str(j-1)];
  end
  method = '';  
  
memFactor = 1;

%% BB
  server='ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'SpeedFair';method = 'SpeedFair'; memFactor = 2;
%   server='ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'SpeedFair_8x_new'; method = 'SpeedFair';
%   server='ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'DRF';method = 'DRF'; memFactor = 2;
  % server='ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'DRF_2x';method = 'DRF';
%   server='ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'Strict';method = 'Strict';
%   server='ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'Strict_8x_new'; method = 'Strict';
%% TPC-DS
%   server = 'ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'DRF_TPC_DS'; method = 'DRF';
%   server = 'ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'Strict_TPC_DS'; method = 'Strict';
%   server = 'ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'SpeedFair_TPC_DS'; method = 'SpeedFair';
%% TPC-H
%   server = 'ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'DRF_TPC_H'; method = 'DRF';
%   server = 'ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'Strict_TPC_H'; method = 'Strict';
%   server = 'ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us'; subFolder = 'SpeedFair_TPC_H'; method = 'SpeedFair';

  
  subfolder = ['b' int2str(num_batch_queues) 'i1_' subFolder]; extra='';
  
  if num_batch_queues==0
      subFolder='';
      subfolder = ['b' int2str(num_batch_queues) 'i1'];
  end
  % subfolder = 'runb2i1'; extra='';
  % method = 'SpeedFair'; subfolder = 'runb3i1_1201_bursty'; extra='';
  % method = 'SpeedFair'; subfolder = 'runb3i1_1203_preemption_speedfair_200'; extra='_preemption';
  % method = 'SpeedFair'; subfolder = 'runb3i1_1204_nonpreemption_speedfair_200'; extra='';
  % method = 'SpeedFair'; subfolder = 'runb3i1_1203_preemption_speedfair'; extra='_preemption';
  % method = 'SpeedFair'; subfolder = 'runb3i1_1203_preemption_speedfair_5x'; extra='_5x';

  % method = '??'; subfolder = 'runb3i1'; extra='';
  % method = 'Strict'; subfolder = 'runb3i1_1201_strict'; extra=''
  % method = 'SpeedFair'; subfolder = 'runb3i1_1201_speedfair'; extra='';
  %method = 'drf'; subfolder = 'runb3i1_1201_drf'; extra='';

  % method = 'SpeedFair'; subfolder = 'runb3i1_1203_preemption'; extra='_preemption';

  result_folder=['/home/tanle/projects/BPFImpl/results/' server '/' subfolder '/users/tanle/SWIM/scriptsTest/workGenLogs/'];

  % result_folder=['/home/tanle//projects/ccra/SWIM/scriptsTest/workGenLogs/']; method=''; MAX_CPU = 16; MAX_MEM = 16; END_TIME=500;
  

  % result_folder = '../0_run_simple/'; workload='simple';
  %result_folder = '../0_run_BB/'; workload='BB';
  % result_folder = '../0_run_BB2/'; workload='BB2';
  % result_folder = '../0_run_TPC-H/'; workload='TPC-H'; % weird
  % result_folder = '../0_run_TPC-DS/'; workload='TPC-DS'; % okay 
  % STEP_TIME = 1.0; output_sufix = '';
  % fig_path = ['figs/' output_sufix]; 
  % is_printed = true;

   start_time_step = START_TIME/STEP_TIME;
  max_time_step = END_TIME/STEP_TIME;
  startIdx = start_time_step*num_queues+1;
  endIdx = max_time_step*num_queues;
  num_time_steps = max_time_step-start_time_step+1;
  linewidth= 2;
  barwidth = 1.0;
  timeInSeconds = (START_TIME:STEP_TIME:END_TIME) - START_TIME;


  % extraStr = '';
  extraStr = ['_' int2str(num_interactive_queue) '_' int2str(num_batch_queues)];

  
   %logFile = [ logfolder 'SpeedFair-output' extraStr '.csv'];
   logFile = [ result_folder 'yarnUsedResources.csv'];
   [datetimes, queueNames, res1, res2, flag] = importRealResUsageLog(logFile); res2=res2./GB;
   if (flag)      
      usedCPUs= zeros(length(queues),num_time_steps);
      usedMEM= zeros(length(queues),num_time_steps);
      queueIdxs = zeros(length(queues),num_time_steps);
      for i=1:length(queues)
        temp = find(strcmp(queueNames, ['root.' queues{i}]));
        len = min(length(temp),max_time_step); 
        endIdx= len-start_time_step+1;
        queueIdxs(i,1:endIdx)=temp(start_time_step:len);
        usedCPUs(i,1:endIdx) = res1(temp(start_time_step:len));
        usedMEM(i,1:endIdx) = res2(temp(start_time_step:len))*memFactor;
      end
      
      figure;
      subplot(2,1,1); 
      hBar = bar(timeInSeconds,usedCPUs',barwidth,'stacked','EdgeColor','none');
%       set(hBar, {'FaceColor'}, colorBars); 
      ylabel('CPUs');xlabel('seconds');
      ylim([0 MAX_CPU]);
      xlim([0 max(timeInSeconds)]);
      legend(lengendQueuesStr,'Location','northoutside','FontSize',fontLegend,'Orientation','horizontal');
      title([method '- CPUs'],'fontsize',fontLegend);
      
      subplot(2,1,2); 
      hBar =bar(timeInSeconds,usedMEM',barwidth,'stacked','EdgeColor','none');
%       set(hBar,{'FaceColor'}, colorBars); 
      ylabel('GB');xlabel('seconds');
      ylim([0 MAX_MEM]);
      xlim([0 max(timeInSeconds)]);
      legend(lengendQueuesStr,'Location','northoutside','FontSize',fontLegend,'Orientation','horizontal');
      title([method '- Memory'],'fontsize',fontLegend);
      localFigSize = [0.0 0 10.0 7.0];
      set (gcf, 'Units', 'Inches', 'Position', localFigSize, 'PaperUnits', 'inches', 'PaperPosition', localFigSize);     
      if is_printed   
          figIdx=figIdx +1;
        fileNames{figIdx} = ['b' int2str(num_batch_queues) '_res_usage_' subFolder '_' workload extra];        
        epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
        print ('-depsc', epsFile);
      end
   end
end
%% total resource usage
%%

if plots(2)
    num_interactive_queue=1;
    num_batch_queues=8;
    queues = cell(1,num_queues);
    for i=1:num_interactive_queue
        queues{i} = ['bursty' int2str(i-1)];
    end
    for j=1:num_batch_queues
        queues{num_interactive_queue+j} = ['batch' int2str(j-1)];
    end    
  
    beginTimeIdx = 1;
    endTimeIdx = 4000;
    subfolder = 'users/tanle/SWIM/scriptsTest/workGenLogs/'; 
    csvFile = 'yarnUsedResources.csv';

    file = [subfolder csvFile];
    
    scaleUpFactorIdx = 4;
    
    drf_yarn_files = {
                    ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRF_1x/' file];
                  ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRF_2x/' file];
                  ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRF_4x/' file];
                  ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRF_8x/' file]
                  };

    drfw_yarn_files = {
            ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRFW' file];
            ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRFW/' file];
            ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRFW/' file];
            ['ctl.yarn-drf.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_DRFW/' file]
          };  

    speedfair_yarn_files = { ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_SpeedFair_1x_new/' file];
                            ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_SpeedFair_2x_new/' file];
                            ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_SpeedFair_4x_new/' file];
                            ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_SpeedFair_8x_new/' file]
                        };

    strict_yarn_files = {
                ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_Strict_1x/' file]; % yarn-drf
              ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_Strict_2x/' file]; % yarn-drf
              ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_Strict_4x/' file];
              ['ctl.yarn-large.yarnrm-pg0.utah.cloudlab.us/' 'b8i1_Strict_8x_new/' file]
              }; 
            
    [ drf_avgRes1, drf_avgRes2, flag] = computeResourceUsage( drf_yarn_files{scaleUpFactorIdx}, queues, beginTimeIdx,  endTimeIdx);
    [ speedfair_avgRes1, speedfair_avgRes2, flag] = computeResourceUsage( speedfair_yarn_files{scaleUpFactorIdx}, queues, beginTimeIdx,  endTimeIdx);
    [ strict_avgRes1, strict_avgRes2, flag] = computeResourceUsage( strict_yarn_files{scaleUpFactorIdx}, queues, beginTimeIdx,  endTimeIdx);    

  
  burstyIdxs = [1:num_interactive_queue];
  batchIdxs = [num_interactive_queue+1:num_queues];
  drf_bursty = sum(drf_avgRes1( burstyIdxs));
  drf_batch = sum(drf_avgRes1( batchIdxs));
  speedFair_bursty = sum(speedfair_avgRes1( burstyIdxs));
  speedFair_batch = sum(speedfair_avgRes1( batchIdxs));
  strict_bursty = sum(strict_avgRes1( burstyIdxs));
  strict_batch = sum(strict_avgRes1( batchIdxs));
  
  avgRes1 = [drf_bursty, drf_batch, MAX_CPU - (drf_bursty+drf_batch) ; ...
    speedFair_bursty, speedFair_batch, MAX_CPU - (speedFair_bursty+speedFair_batch) ;...
    strict_bursty, strict_batch, MAX_CPU - (strict_bursty+strict_batch) ;
    ];
  
  drf_bursty = sum(drf_avgRes2( burstyIdxs));
  drf_batch = sum(drf_avgRes2( batchIdxs));
  speedFair_bursty = sum(speedfair_avgRes2( burstyIdxs));
  speedFair_batch = sum(speedfair_avgRes2( batchIdxs));
  strict_bursty = sum(strict_avgRes2( burstyIdxs));
  strict_batch = sum(strict_avgRes2( batchIdxs));
  
  avgRes2= [drf_bursty, drf_batch, MAX_MEM*GB - (drf_bursty+drf_batch) ; ...
    speedFair_bursty, speedFair_batch, MAX_MEM*GB - (speedFair_bursty+speedFair_batch) ;...
    strict_bursty, strict_batch, MAX_MEM*GB - (strict_bursty+strict_batch) ;
    ];
  
  colorQueueType = {colorBursty, colorBatch, colorWasted};
  stackLabels = {strLQs,strTQs,strUnalloc};
  groupLabels = {strDRF,strProposed,strStrict};
  resGroupBars = zeros([size(avgRes1,1) 2 size(avgRes1,2)]);
  resGroupBars(:,1,:) = avgRes1/MAX_CPU;
  resGroupBars(:,2,:) = avgRes2/(MAX_MEM*GB);
  h = plotBarStackGroups(resGroupBars, colorQueueType);  
  ylim([0 1]);
  ylabel('normalized capacity');
  legend(stackLabels,'Location','northoutside','FontSize',fontLegend,'Orientation','horizontal');  
  set(gca,'XTickLabel',groupLabels, 'FontSize', fontAxis);   
  
  set (gcf, 'Units', 'Inches', 'Position', figSizeOneCol, 'PaperUnits', 'inches', 'PaperPosition', figSizeOneCol);     
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = ['b' int2str(num_batch_queues) '_avg_res_' workload extra];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end   
  
end

%%
fileNames
return;
%%

for i=1:length(fileNames)
    fileName = fileNames{i};
    epsFile = [ LOCAL_FIG fileName '.eps'];
    pdfFile = [ fig_path fileName  '.pdf'];    
    cmd = sprintf(PS_CMD_FORMAT, epsFile, pdfFile);
    status = system(cmd);
end