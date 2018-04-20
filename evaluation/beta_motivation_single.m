clear all; clc; close all;
common_settings;
%% parameters
plots=[1 1];
is_printed=true;
LOCAL_FIG='';
extraStr='';
figureSize=figSizeOneCol;

%% load data
csv_file = 'beta_mov.csv';
CPU = '16';
MEM = '12';
NUM_THREAD = 16;
%%
NUM_JOBS = 5;
% MODEL_NAMES = {'vgg11', 'vgg16', 'vgg19', 'lenet', 'googlenet', 'overfeat', 'alexnet', 'trivial', 'inception3', 'inception4', 'resnet50', 'resnet101', 'resnet152'};

% TAR_FILE    = 'beta_motivation_20180414a.tar.gz';
% BATCH_NUMS = [32,      32,      32,      32,      32,          32,         512,       32,        32,           64,           64,         64,          64];

% TAR_FILE    = 'beta_motivation_20180414b.tar.gz';
% BATCH_NUMS = 512*ones(1,length(MODEL_NAMES));
% 

% TAR_FILE   = 'beta_motivation_20180414c.tar.gz'; NUM_THREAD = 1;
% BATCH_NUMS = [32,      32,      32,      32,      32,          32,         512,       32,        32,           64,           64,         64,          64];

% GPU_CPU = 16;
% TAR_FILE   = 'beta_motivation_20180415_gcpu16.tar.gz'; NUM_THREAD = 1;
% BATCH_NUMS = [32,      32,      32,      32,      32,          32,         512,       32,        32,           64,           64,         64,          64];

%%
% MODEL_NAMES   = {'vgg16', 'lenet', 'googlenet', 'alexnet', 'trivial',
% 'resnet50', 'inception3'}; %remove trivial 32
MODEL_NAMES   = {'vgg16', 'lenet', 'googlenet', 'alexnet',  'resnet50', 'inception3'};

% TAR_FILE    = 'beta_motivation_good.tar.gz';
% BATCH_NUMS  = [32     ,     32,         32,      512,               64,           64];

% TAR_FILE    = 'beta_motivation.tar.gz';
% BATCH_NUMS  = [32     ,     32,         32,      512,                64,           64];


% TAR_FILE    = 'beta_motivation_m3G.tar.gz';
% MEM = '3';
% BATCH_NUMS  = [32     ,     32,         32,      512,                64,           64];

TAR_FILE    = 'beta_motivation_512.tar.gz';
BATCH_NUMS  = [512     ,     512,         512,      512,                512,           512];

NUM_JOBS = 3;
MAIN_FOLDER = 'beta_motivation';
subfolder   = 'beta_motivation';
%%
try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
catch fileIO
   
end

untar([MAIN_FOLDER '/' TAR_FILE], [MAIN_FOLDER]);
FOLDER = [MAIN_FOLDER '/' subfolder];

cpuCmpl = zeros(length(MODEL_NAMES), NUM_JOBS);
gpuCmpl = zeros(length(MODEL_NAMES), NUM_JOBS);

betas = zeros(length(MODEL_NAMES), NUM_JOBS);

for iModel = 1:length(MODEL_NAMES)
  for iJob = 0:NUM_JOBS-1
    strCommon = [num2str(CPU) '-' num2str(MEM) '-' num2str(BATCH_SIZEs(iModel)) '-' num2str(NUM_THREAD) '-' num2str(iJob)];
    % read cpu    
    cpuLogFile = [FOLDER '/' MODEL_NAMES{iModel} '-cpu-' strCommon '.log'];
    cpuCmpl(iModel, iJob+1) = getComplFromLog(cpuLogFile);
    % read gpu
    gpuLogFile = [FOLDER '/' MODEL_NAMES{iModel} '-gpu-' strCommon '.log'];
    gpuCmpl(iModel, iJob+1) = getComplFromLog(gpuLogFile);
  end
  if min(cpuCmpl(iModel, :)) < 0
    cpuCmpl(iModel, :) = 0;
  end
end
betas = mean(cpuCmpl,2)./mean(gpuCmpl,2);

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
  if min(cpuCmplOverhead(iModel, :)) < 0
    cpuCmplOverhead(iModel, :) = 0;
  end
end
betasWithOverheads = mean(cpuCmplOverhead,2)./mean(gpuCmplOverhead,2);
%%
try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
catch fileIO
   error('no directories to be deleted');
end
%% plots
if plots(1) 
  figure;
  
  xLabels = MODEL_NAMES;
  
  %https://github.com/minimaxir/deep-learning-cpu-gpu-benchmark
  
  hBar=bar(betas, 0.5, 'EdgeColor','none');  
  %barColors={colorBursty0};   set(hBar,{'FaceColor'},barColors);   
  xlim([0.5 length(betas)+0.5]);
%   xlabel('workloads'); 
  ylabel('speedup rates ');
  set(gca,'xticklabel',xLabels, 'FontSize',fontAxis-1);
%   set(gca,'YScale','log');
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_mov'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

%%
if plots(2) 
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
cpuOverheads  = cpuCmplOverhead - cpuCmpl;
gpuOverheads = gpuCmplOverhead - gpuCmpl;

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
