clear; clc; close all;
common_settings;
%%
folder = 'cpu_on_gpu';
job_name = 'alexnet';

figureSize = [1 1 4/5 4/5].* figSizeOneCol;

%% 

cpus=[0.1, 0.2, 0.4, 0.8, 1.0, 1.5, 2.0, 3.0];
NORM_Idx = 5;
numExperiments= 5;
complTimes = zeros(length(cpus), numExperiments);

for iCpu = 1:length(cpus)
  for i=0:(numExperiments-1)
    cpu = cpus(iCpu);
    file_name = [folder '/' job_name '/' job_name '-' sprintf('%0.1f',cpu) '-' num2str(i) '.log'];
    cmpl = -1;
    % read file to get the completion time
    fid = fopen(file_name);  % Open the file
    while(1)
      line_ex = fgetl(fid);
      if(line_ex < 1)        
        break;
      end
      if (strfind(line_ex,'Total time taken:'))
        strArr = strsplit(line_ex);
        cmpl = str2double(strArr(4));
        complTimes(iCpu,i+1) = cmpl;
        break;
      end
    end    
    fclose(fid);
  end
end
avgCompls = mean(complTimes,2);

%% plots
figure;

plot(cpus, (avgCompls/avgCompls(NORM_Idx)), lineSolid ,'LineWidth', LineWidth);
ylabel('norm. compl. vs. 1 core');
xlabel(strCpuCores); 
% legend(lengendStr,'Location','northoutside','FontSize',fontLegend,'Orientation','horizontal');
title('Impact of cpu on GPU jobs','fontsize',fontLegend);

set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);
if is_printed     
    figIdx=figIdx +1;
  fileNames{figIdx} = ['cpu_on_gpu'];       
  epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
  print ('-depsc', epsFile);
end

%%
return
%% convert to PDF
fileNames
for i=1:length(fileNames)
    fileName = fileNames{i}
    epsFile = [ LOCAL_FIG fileName '.eps'];
    pdfFile = [ fig_path fileName '.pdf'];    
    cmd = sprintf(PS_CMD_FORMAT, epsFile, pdfFile);
    status = system(cmd);
end
