clear; close all; clc;
addpath('functions');

fontSize=10;

fontAxis = fontSize;
fontTitle = fontSize;
fontLegend = fontSize;
LineWidth = 1.5;
FontSize = fontSize;
is_printed = true;
axisWidth = 1.5;

%%

legendSize = [0.0 0 5 0.3];
figSizeOneCol = [0.0 0 5 3];
figSizeOneColHaflRow = [1 1 1 0.5].* figSizeOneCol;
figSizeTwoCol = 2*figSizeOneCol;
figSizeOneThirdCol = 1/3*figSizeOneCol;
figSizeHalfCol = 1/2*figSizeOneCol;
figSizeTwothirdCol = 2/3*figSizeOneCol;
figSizeFourFifthCol = 4/5*figSizeOneCol;

figSize2ColWidth = [1 1 2.5 1].*figSizeOneCol;

%%

barLineWidth=0;
groupBarSize = 0.9;

%%

figIdx=0;

LOCAL_FIG = 'figs/';

%PS_CMD_FORMAT='ps2pdf -dEmbedAllFonts#true -dSubsetFonts#true -dEPSCrop#true -dPDFSETTINGS#/prepress %s %s';
PS_CMD_FORMAT='ps2pdf -dEmbedAllFonts#true -dSubsetFonts#true -dEPSCrop#false -dPDFSETTINGS#/prepress %s %s';

fig_path = ['figs/'];
% fig_path = ['/home/tanle/Dropbox/Papers/IRF/InterchangeableResources/OSDI2018/figs/'];

%%

strBatchSize = 'batch size';
strSpeedUpRate = 'speed-up rate';
strEstimationErr = 'std. of estimation errors [%]';
strFactorImprove = 'factor of improvement';
strAvgComplTime = 'avg. compl. (secs)';


%% line specs
lineSolid = '-';
lineProposed = '-';
lineStrict = '+:';
lineDRF = '-.';
lineDRFW = '--';

lineBB = '-';
lineTPCDS = '--';
lineTPCH = '-.';
workloadLineStyles = {lineBB, lineTPCDS, lineTPCH};

%%

%http://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3


