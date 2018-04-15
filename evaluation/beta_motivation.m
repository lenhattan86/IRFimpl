clear all; clc; close all;
common_settings;
%% parameters
plots=[1];
is_printed=true;
LOCAL_FIG='';
extraStr='';
figureSize=figSizeOneCol;

%% load data
CPU = '16';
MEM = '12';
NUM_THREAD = 16;
MODEL_NAMES = {'vgg11', 'vgg16', 'vgg19', 'lenet', 'googlenet', 'overfeat', 'alexnet', 'trivial', 'inception3', 'inception4', 'resnet50', 'resnet101', 'resnet152'};
BATCH_NUMS = [32,      32,      32,      32,      32,          32,         512,       32,        32,           64,           64,         64,          64];

% BATCH_NUMS = 512*ones(1,length(MODEL_NAMES));

NUM_JOBS = 5;
MAIN_FOLDER = 'beta_motivation';
TAR_FILE    = 'beta_motivation_20180414a.tar.gz';
subfolder   = 'beta_motivation';
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
    strCommon = [num2str(CPU) '-' num2str(MEM) '-' num2str(BATCH_NUMS(iModel)) '-' num2str(NUM_THREAD) '-' num2str(iJob)];
    % read cpu    
    cpuLogFile = [FOLDER '/' MODEL_NAMES{iModel} '-cpu-' strCommon '.log'];
    cpuCmpl(iModel, iJob+1) = getComplFromLog(cpuLogFile);
    % read gpu
    gpuLogFile = [FOLDER '/' MODEL_NAMES{iModel} '-gpu-' strCommon '.log'];
    gpuCmpl(iModel, iJob+1) = getComplFromLog(gpuLogFile);
  end
end
betas = mean(cpuCmpl,2)./mean(gpuCmpl,2);

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
  
  hBar=bar(betas, 0.4, 'EdgeColor','none');  
  %barColors={colorBursty0};   set(hBar,{'FaceColor'},barColors);   
  
  xlabel('workloads'); ylabel('speedup rates ');
  set(gca,'xticklabel',xLabels,'FontSize',fontAxis);
%   set(gca,'YScale','log');
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

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
