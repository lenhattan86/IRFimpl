clear all; clc; close all;
common;
%%
plots=[1];
is_printed=true;
LOCAL_FIG='';
extraStr='';
figureSize=figSizeOneCol;
%% beta
if plots(1) 
  figure;
  %cpuComplTimes=[1 1.5 0.45 581 2415];
  %gpuComplTimes=[32.383 1   1    45.89  52.89]; 
  %xLabels = {'linear', 'LSTM','BLSTM','Alexnet','VGG16'};
  
  cpuComplTimes=[5      250.5     110   5047     65054.7];
  gpuComplTimes=[10.102 13.65     114   45.89   52.89]; 
  xLabels = {'s-linear', 'l-linear','BLSTM', 'Alexnet','VGG16'};
  
  betas = cpuComplTimes./gpuComplTimes;
  
  %https://github.com/minimaxir/deep-learning-cpu-gpu-benchmark
  
  
  
  hBar=bar(betas, 0.4)%,'EdgeColor','none');  
  %barColors={colorBursty0};   set(hBar,{'FaceColor'},barColors);   
  
  xlabel('workloads'); ylabel('speedup rates ');
  set(gca,'xticklabel',xLabels,'FontSize',fontAxis);
  set(gca,'YScale','log');
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
%%
