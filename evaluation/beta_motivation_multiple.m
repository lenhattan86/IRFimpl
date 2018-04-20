clear all; clc; close all;
common_settings;
%% parameters
plots=[1 1];
is_printed=true;
extraStr='';
figureSize=figSizeOneCol;

%% load data
csv_file = 'beta_mov.csv';
CPU = '16';
MEM = '12';
NUM_THREAD = 16;
%%
NUM_JOBS = 3;
MODEL_NAMES = {'vgg16', 'lenet', 'googlenet', 'alexnet',  'resnet50', 'inception3'};
TAR_FILEs    = {'beta_motivation_b16.tar.gz', ...
                'beta_motivation_b32.tar.gz',...
                'beta_motivation_b64.tar.gz',...
                'beta_motivation_b128.tar.gz',...
                'beta_motivation_b256.tar.gz',...
                'beta_motivation_b512.tar.gz',...
                'beta_motivation_b1024.tar.gz',...
                'beta_motivation_b2048.tar.gz',...
                'beta_motivation_b4096.tar.gz',...
                'beta_motivation_b8192.tar.gz',...
                'beta_motivation_b16384.tar.gz',... 
                };
BATCH_SIZEs = 2.^[4:14];
MAIN_FOLDER = 'beta_sensitivity';
subfolder   = 'beta_motivation';
betas = zeros(length(TAR_FILEs), length(MODEL_NAMES));
betasWithOverheads = zeros(length(TAR_FILEs), length(MODEL_NAMES));
%%
try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
catch fileIO
   
end

for iFile = 1: length(TAR_FILEs)
  TAR_FILE = TAR_FILEs{iFile};
  untar([MAIN_FOLDER '/' TAR_FILE], [MAIN_FOLDER]);
  FOLDER = [MAIN_FOLDER '/' subfolder];

  cpuCmpl = zeros(length(MODEL_NAMES), NUM_JOBS);
  gpuCmpl = zeros(length(MODEL_NAMES), NUM_JOBS);

  for iModel = 1:length(MODEL_NAMES)
    for iJob = 0:NUM_JOBS-1
      strCommon = [num2str(CPU) '-' num2str(MEM) '-' num2str(BATCH_SIZEs(iFile)) '-' num2str(NUM_THREAD) '-' num2str(iJob)];
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
  betas(iFile,:) = mean(cpuCmpl,2)./mean(gpuCmpl,2);

%
  [datetimes, steps, users, podnames, statuses] = importUserInfo([MAIN_FOLDER '/' subfolder '/' csv_file]);
  if length(datetimes) <=0
    break;
  end

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
      strCommon = [num2str(CPU) '-' num2str(MEM) '-' num2str(BATCH_SIZEs(iFile)) '-' num2str(NUM_THREAD) '-' num2str(iJob)];
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
  betasWithOverheads(iFile,:) = mean(cpuCmplOverhead,2)./mean(gpuCmplOverhead,2);
  
  try
   rmdir([MAIN_FOLDER '/' subfolder],'s');
  catch fileIO
     error('no directories to be deleted');
  end
end

%% plots
close all;
if plots(1) 
  figure;
  
  strLegend = MODEL_NAMES;
  for iModel = 1:length(MODEL_NAMES)
    subIds = find(betas(:,iModel) > 0);   
    beta = betas(:,iModel)
    plot(BATCH_SIZEs(subIds),beta(subIds),'LineWidth', LineWidth);
    hold on;
  end
  
  set(gca,'XScale','log');
  ylabel(strSpeedUpRate);
  xlabel(strBatchSize);
  legend(strLegend, 'Location', 'northeast', 'FontSize', fontLegend);
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_sensitivity'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

%
if plots(2) 
  figure;
  
  strLegend = MODEL_NAMES;
  for iModel = 1:length(MODEL_NAMES)
    subIds = find(betasWithOverheads(:,iModel) > 0);   
    beta = betasWithOverheads(:,iModel);
    plot(BATCH_SIZEs(subIds),beta(subIds),'LineWidth', LineWidth);
    hold on;
  end
  
  set(gca,'XScale','log');
  ylabel(strSpeedUpRate);
  xlabel(strBatchSize);
  legend(strLegend, 'Location','northeast','FontSize',fontLegend);
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_w_overh'];        
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
