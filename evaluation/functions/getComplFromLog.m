function comptTime = getComplFromLog(filename)


comptTime = -1;
% read file to get the completion time
fid = fopen(filename);  % Open the file
while(1)
  line_ex = fgetl(fid);
  if(line_ex < 1)        
    break;
  end
  if (strfind(line_ex,'Total time taken:'))
    strArr = strsplit(line_ex);
    comptTime = str2double(strArr(4));    
    break;
  end
end    
fclose(fid);