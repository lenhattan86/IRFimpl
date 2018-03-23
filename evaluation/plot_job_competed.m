clear; clc; close all;


%%
job_completed = [26 30;
                30 43];
             
bar(job_completed, 'group');
ylabel('job completed');
xlabel('Users');
strLegend={'DRF','FDRF'};
legend(strLegend);
%%
