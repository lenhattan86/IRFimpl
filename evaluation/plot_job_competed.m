clear; clc; close all;
common_settings;
addpath('functions');
extraStr ='';
plots = [1 1];
%%
stopTime = 3000;
TAR_FILEs ={'naiveDRF2','static2'};
% stopTime = 660;
% TAR_FILEs ={'naiveDRF1','static1'};

MAIN_FOLDER = 'motivation';

% methods ={'DRF','FDRF','Pricing'};
UserIds = {'user1','user2'};
strUsers   = {'alexnet','lenet'};
OUT_FOLDERS ={'naiveDRF','static'};
methods = {'DRF', 'Optimal'};

job_completed = zeros(length(UserIds), length(methods));

for iMethod = 1:length(methods)
  folder = [MAIN_FOLDER '/' OUT_FOLDERS{iMethod}];
  TAR_FILE = [TAR_FILEs{iMethod} '.tar.gz'];
  try
   rmdir(folder,'s');
  catch fileIO   
  end  
  untar([MAIN_FOLDER '/' TAR_FILE], [MAIN_FOLDER]);
%%
  filename = [folder '/pods.csv'];
  [datetimes, steps, users, podnames,statuses] = importUserInfo(filename);  
  
  stepIds = (steps==stopTime);
  steps = steps(stepIds);
  users = users(stepIds);
  statuses = statuses(stepIds);
%   podnames = podnames(stepIds);
  
  for iUser = 1:length(UserIds)
    user = UserIds{iUser};
    ids = strcmp(users, user);
    mStatuses = statuses(ids);
    job_completed(iUser,iMethod) = sum(strcmp(mStatuses,'Completed'));
  end  
%%  
  try
    rmdir(folder,'s');
  catch fileIO
     error('no directories to be deleted');
  end
end

%%

if plots(1) 
  figure;
  figureSize = figSizeOneCol;
  hBar=bar(job_completed, 'group', 'EdgeColor','none');
  ylabel('job completed');
  xlabel('Users');
  strLegend=methods;
  legend(strLegend, 'Location','northwest');
  xLabels = strUsers;  
  
  xlim([0.5 length(strUsers)+0.5]);
  set(gca, 'xticklabel',xLabels,'FontSize',fontAxis);
  set (gcf, 'Units', 'Inches', 'Position', figureSize, 'PaperUnits', 'inches', 'PaperPosition', figureSize);  
  if is_printed   
    figIdx=figIdx +1;
    fileNames{figIdx} = [extraStr 'num_job_completed'];        
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


