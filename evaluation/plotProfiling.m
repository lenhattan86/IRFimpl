clear all; clc; close all;
common_settings;
%% parameters
plots=[1 1];
is_printed=true;
LOCAL_FIG='';
extraStr='';
figureSize=figSizeOneCol;

%% load data
csv_file = 'profiling.csv';
CPU = '16';
MEM = '12';
NUM_THREAD = 16;
NUM_JOBS = 12;
MODEL_NAMES   = {'vgg16', 'googlenet', 'alexnet',  'inception3'};
BATCH_SIZEs    =  [32     ,  16        ,        64,         16];
% TAR_FILE      = 'profiling_3.tar.gz';
TAR_FILE      = 'profiling.tar.gz';
MAIN_FOLDER   = 'awscloudlab/profiling';
subfolder     = 'profiling';
%%
try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
catch fileIO
   
end

untar([MAIN_FOLDER '/' TAR_FILE], [MAIN_FOLDER]);
FOLDER = [MAIN_FOLDER '/' subfolder];

%%
[datetimes,steps,users,podnames,statuses] = importUserInfo([MAIN_FOLDER '/' subfolder '/' csv_file]);

uniquePodnames = cell(1,0);
iPod = 0;
cpuComplTimes = [];
cpuOverheadTimes = [];
gpuComplTimes = [];
gpuOverheadTimes = [];

cpuCmplOverhead = zeros(length(MODEL_NAMES), NUM_JOBS);
gpuCmplOverhead = zeros(length(MODEL_NAMES), NUM_JOBS);

strJob = 'job-';
for iModel = 1:length(MODEL_NAMES)
  for iJob = 0:NUM_JOBS-1
    strCommon = [num2str(CPU) '-' num2str(MEM) '-' num2str(BATCH_SIZEs(iModel)) '-' num2str(NUM_THREAD) '-' num2str(iJob)];
    % read cpu    
    cpuPodName = [strJob MODEL_NAMES{iModel} '-cpu-' strCommon ];
    [ startTime, startRunTime, stopTime, conCreateTime, complTime ] = ...
        obtainPodComplTime(cpuPodName,  podnames,  statuses,  steps, datetimes );
    cpuCmplOverhead(iModel, iJob+1) = complTime;
    
    % read gpu
    gpuPodName = [strJob MODEL_NAMES{iModel} '-gpu-' strCommon ];
    [ startTime, startRunTime, stopTime, conCreateTime, complTime ] = ...
        obtainPodComplTime(gpuPodName,  podnames,  statuses,  steps, datetimes );
    gpuCmplOverhead(iModel, iJob+1) = complTime;    
  end
%   if min(cpuCmplOverhead(iModel, :)) < 0
%     cpuCmplOverhead(iModel, :) = 0;
%   end
end
betasWithOverheads = mean(cpuCmplOverhead,2)./mean(gpuCmplOverhead,2);

%%
try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
catch fileIO
   error('no directories to be deleted');
end

%%
if plots(1) 
  figure;
  
  xLabels = MODEL_NAMES;  
  %https://github.com/minimaxir/deep-learning-cpu-gpu-benchmark
  
  hBar=bar(betasWithOverheads, 0.5, 'EdgeColor','none');  
  %barColors={colorBursty0};   set(hBar,{'FaceColor'},barColors);   
  xlim([0.5 length(betasWithOverheads)+0.5]);
%   xlabel('workloads'); 
  ylabel('speedup rates ');
  set(gca,'xticklabel',xLabels,'FontSize',fontAxis);
%   set(gca,'YScale','log');
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_mov_wOverhead'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

%%
mean(cpuCmplOverhead,2)
mean(gpuCmplOverhead,2)
return;
%%
for i=1:length(fileNames)
    fileName = fileNames{i};
    epsFile = [ LOCAL_FIG fileName '.eps'];
    pdfFile = [ fig_path fileName  '.pdf']    
    cmd = sprintf(PS_CMD_FORMAT, epsFile, pdfFile);    
    status = system(cmd);
    status = system(['rm -rf ' epsFile]);
end
