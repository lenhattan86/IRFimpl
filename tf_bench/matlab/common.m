clear; close all; clc;

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

%%

barLineWidth=0;
groupBarSize = 0.9;

%%
figIdx=0;
%LOCAL_FIG = 'figs/';
LOCAL_FIG = '';
PS_CMD_FORMAT='ps2pdf -dEmbedAllFonts#true -dSubsetFonts#true -dEPSCrop#false -dPDFSETTINGS#/prepress %s %s';
fig_path = ['../IRF/figs/'];

%%

strLQ = 'LQ';
strTQ = 'TQ';

strLQs = 'LQs';
strTQs = 'TQs';

strUnalloc = 'unallocated';

strDRF = 'DRF';
strDRFW = 'DRF-W';
strStrict = 'SP';
strProposed = 'BPF';
strHard = 'N-BPF'; %

strEstimationErr = 'std. of estimation errors [%]';
strFactorImprove = 'factor of improvement';
strAvgComplTime = 'avg. compl. (secs)';

%% line specs
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

% colorProposed = [0.8500    0.3250    0.0980];
% colorStrict = [0.4660    0.6740    0.1880];
% colorDRF = [0    0.4470    0.7410];
% colorDRFW = [0.9290    0.6940    0.1250];

% colorProposed = [237    125    49]/255;
% colorStrict = [165    165    165]/255;
% colorDRF = [68    71   196]/255;
% colorDRFW = [00    0.0    0.0];
% colorhard = [hex2dec('2c')    hex2dec('7f')    hex2dec('b8')]/255;%2c7fb8


colorDRF = [hex2dec('21')    hex2dec('66')    hex2dec('ac')]/255; % 2166ac
colorStrict = [hex2dec('fd')    hex2dec('db')    hex2dec('c7')]/255; % 67a9cf
% colorhard = [hex2dec('ca')    hex2dec('00')    hex2dec('20')]/255; % ca0020
colorhard = [hex2dec('92')    hex2dec('c5')    hex2dec('de')]/255; % 92c5de
colorProposed = [hex2dec('ef')    hex2dec('8a')    hex2dec('62')]/255; % ef8a62

colorDRFW = [00    0.0    0.0];

colorArraySimulation = [colorDRF colorDRFW colorStrict colorProposed];


colorBarMinMax='k';
lineWidthBarMinMax=1.5;

% colorBursty0 = [0    0.4470    0.7410];
colorBursty0 = [hex2dec('1f')    hex2dec('49')    hex2dec('7d')]/255;

% colorBursty0 = [hex2dec('0c')    hex2dec('2c')    hex2dec('84')]/255;
colorBursty1 = [hex2dec('22')    hex2dec('5e')    hex2dec('a8')]/255;
colorBursty2 = [hex2dec('1d')    hex2dec('91')    hex2dec('c0')]/255; % 1d91c0

% colorBatch0 = [0.8500    0.3250    0.0980];
colorBatch0 = [hex2dec('f7')    hex2dec('96')    hex2dec('46')]/255;
colorBatch1 = [0.9290    0.6940    0.1250];
colorBatch2 = [0.4940    0.1840    0.5560];
colorBatch3 = [0.4660    0.6740    0.1880];
colorBatch4 = [0.3010    0.7450    0.9330];
colorBatch5 = [0.6350    0.0780    0.1840];
colorBatch6 = [0.7500    0.7500         0];
colorBatch7 = [0.2500    0.2500    0.2500];

colorb8i1 = {colorBursty0; colorBatch0; colorBatch1; colorBatch2; colorBatch3; colorBatch4; colorBatch5; colorBatch6; colorBatch7};
colorb1i1 = {colorBursty0; colorBatch0};
colorb1i3 = {colorBursty0; colorBursty1;colorBursty2; colorBatch0};

colorBursty = colorBursty0;
colorBatch = colorBatch0;
colorWasted = [1 1 1];

%  0         0    1.0000
%          0    0.5000         0
%     1.0000         0         0
%          0    0.7500    0.7500
%     0.7500         0    0.7500
%     0.7500    0.7500         0
%     0.2500    0.2500    0.2500

