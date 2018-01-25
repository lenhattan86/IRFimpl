clear all; clc; close all;
common;
%%
plots=[1];
is_printed=true;
LOCAL_FIG='';
extraStr='';

%% beta
if plots(1) 
  cpuComplTimes=[33810 144900 0 0];
  gpuComplTimes=[161 322 141 150];

  betas = cpuComplTimes./gpuComplTimes;

  xLabels = {'Alexnet','VGG16','inception3','resnet50'};

  bar(betas,0.2);
  set(gca,'xticklabel',xLabels)

  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'beta'];        
    epsFile = [ LOCAL_FIG fileNames{figIdx} '.eps'];
    print ('-depsc', epsFile);
  end
end

%%

%%

for i=1:length(fileNames)
    fileName = fileNames{i};
    epsFile = [ LOCAL_FIG fileName '.eps'];
    pdfFile = [ fig_path fileName  '.pdf']    
    cmd = sprintf(PS_CMD_FORMAT, epsFile, pdfFile);    
    status = system(cmd);
    status = system(['rm -rf ' epsFile]);
end