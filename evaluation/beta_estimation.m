clear; close all; clc
common_settings;
plots = [1 1];
extraStr = '';
%% data

%% 
jobNames = {'lenet', 'alexnet'};
% jobNames = {'lenet'};
batchSizes  = [32, 512]
CPU = 16;
MEM = 12;
NUM_THREADs = 16;
% estimate data
dataLen = 11;
rBachtNums = [100, 100];

% data
kArray = [10];
batchNums = rBachtNums*kArray;

% load data from 
folder = '/ssd/projects/IRFimpl/evaluation/beta_estimation/'
[pilotCompls_on_CPU, pilotCompls_on_GPU, compls_on_CPU, compls_on_GPU] = getProfilingData([folder 'logdata.txt'], jobNames, dataLen, rBachtNums, ...
  CPU, MEM, batchSizes, NUM_THREADs, kArray, 'job-');
%
train_start = 1;
train = 7;
% test_start = 1;
test_start = train+train_start;
test = dataLen-test_start+1;

k = (batchNums/rBachtNums);
% model compls=(batchNum/pilotBatchNum) * pilotCompls -
% (batchNum/pilotBatchNum - 1) * cpuOverheads

%% For CPU
cpuOverheads = (k.* pilotCompls_on_CPU(:,train_start:train+train_start-1) - compls_on_CPU(:,train_start:train+train_start-1))./(k - 1) ;
cpuOverheads = mean(cpuOverheads,2);
%% For GPU
gpuOverheads = (k.* pilotCompls_on_GPU(:,train_start:train+train_start-1) - compls_on_GPU(:,train_start:train+train_start-1))./(k - 1) ;
gpuOverheads = mean(gpuOverheads,2);
%% Predict
predict_Compls_on_CPU = k* pilotCompls_on_CPU(:,test_start:test+test_start-1) - (k - 1) * cpuOverheads * ones(1,test);
predict_Compls_on_GPU = k* pilotCompls_on_GPU(:,test_start:test+test_start-1) - (k - 1) * gpuOverheads * ones(1,test);

GPU_errors = 100*(compls_on_GPU(:,test_start:test+test_start-1) - predict_Compls_on_GPU)./compls_on_GPU(:,test_start:test+test_start-1);

CPU_errors = 100*(compls_on_CPU(:,test_start:test+test_start-1) - predict_Compls_on_CPU)./compls_on_CPU(:,test_start:test+test_start-1);

%% Plot prediction errors
if plots(1) 
  figure;
  yValues = GPU_errors;
  figureSize = figSizeOneCol;
    barData = mean(yValues,2);
    hBar=bar(barData, 'group');
    ylabel('errors (%)');
 
  xlim([0 7]);
  xLabels =  jobNames;
  set(gca, 'xticklabel',xLabels,'FontSize',fontAxis);
  
  barLowerErr = barData-min(yValues')';
  barUpperErr= max(yValues')'-barData;
  hold on; 
  numgroups = size(barData, 1); 
  numbars = size(barData, 2); 
  groupwidth = min(0.8, numbars/(numbars+1.5));
  
    
  for i = 1:numbars  
     x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar
        minMaxBarChart = errorbar(x, barData(:,i), barLowerErr(:,i), barUpperErr(:,i), colorBarMinMax, 'linestyle', 'none','linewidth',lineWidthBarMinMax);
%     minMaxBarChart = errorbar(x, barData(:,i), barLowerErr(:,i), barUpperErr(:,i));
  end
  
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_est_gpu'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

if plots(2) 
  figure;
  yValues = CPU_errors;
  figureSize = figSizeOneCol;
    barData = mean(yValues,2);
    hBar=bar(barData, 'group');
    ylabel('errors (%)');
 
  xlim([0 7]);
  xLabels =  jobNames;
  set(gca, 'xticklabel',xLabels,'FontSize',fontAxis);
  
  barLowerErr = barData-min(yValues')';
  barUpperErr= max(yValues')'-barData;
  hold on; 
  numgroups = size(barData, 1); 
  numbars = size(barData, 2); 
  groupwidth = min(0.8, numbars/(numbars+1.5));
  
    
  for i = 1:numbars  
     x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar
        minMaxBarChart = errorbar(x, barData(:,i), barLowerErr(:,i), barUpperErr(:,i), colorBarMinMax, 'linestyle', 'none','linewidth',lineWidthBarMinMax);
%     minMaxBarChart = errorbar(x, barData(:,i), barLowerErr(:,i), barUpperErr(:,i));
  end
  
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta_est_cpu'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

%%
return;
%%

for i=1:length(fileNames)
    fileName = fileNames{i};
    epsFile = [ LOCAL_FIG fileName '.eps'];
    pdfFile = [ fig_path fileName  '.pdf']    
    cmd = sprintf(PS_CMD_FORMAT, epsFile, pdfFile);    
    status = system(cmd);
%     status = system(['rm -rf ' epsFile]);
end