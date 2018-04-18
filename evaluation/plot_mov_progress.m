%%
clear; clc; close all;
addpath('functions');
common_settings;
plots = [1];
extraStr = '';
%% 
% get this data from ./motivation 1 & 2
% use plot_job_completed.m to parse the data.
yValues = [1 1; 6/6 223/120; 40/35 636/583]; 
strUsers = {'alexnet', 'lenet'};
methods = {'DRF','Solution 1', 'Solution 2'};

if plots(1) 
  figure;
  figureSize = figSizeOneCol;

  hBar=bar(yValues', 'group');
  ylabel('norm. progress');
%   xlabel('Users');
  strLegend=methods;
  legend(strLegend, 'Location','northwest');
  xLabels = strUsers;  
  xlim([0.5 length(strUsers)+0.5]);
  
  set(gca, 'xticklabel',xLabels,'FontSize',fontAxis);
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'mov_progress'];        
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

