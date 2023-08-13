clear all;
close all;
fclose all;

site_coordinate = "Z:\\Greenbelt\\RAS_Model_Working\\Observation\\CPPJ_site_coordinate.txt";
coord = readtable(site_coordinate); 
StationID = table2array(coord(:,1));
x_model = table2array(coord(:,2));
y_model = table2array(coord(:,3));
Number_Station = length(StationID);

[filename_temp,PathName] = uigetfile('*.hdf*','Select Time Series File');
filename = sprintf('%s\\%s',PathName,filename_temp);

% load in flow area names
FA_Att = h5read(filename,'/Geometry/2D Flow Areas/Attributes'); 
FA_Name = transpose(FA_Att.Name);
for i = 1:size(FA_Name,1)
    FlowAreas(i,1) = deblank(convertCharsToStrings(FA_Name(i,:))); 
end

% find the nearest grid cell and save the water surface elevation 
for i = 1:Number_Station
    
    x_modeli = x_model(i);
    y_modeli = y_model(i);
    
    best = 1;
    bestDist = 9999;
    
    for k = 1:length(FlowAreas)
        temp = ['/Geometry/2D Flow Areas/',convertStringsToChars(FlowAreas(k)),'/Cells Center Coordinate'];
        
        cellctrs = h5read(filename,temp);
   
        for j =1:size(cellctrs,2)
            dist = ((x_modeli-cellctrs(1,j))^2 + (y_modeli-cellctrs(2,j))^2 )^0.5;
            if dist < bestDist
                best = j;
                bestDist = dist;
                FA_found = FlowAreas(k);
            end
        end        
    end
    
    if bestDist==9999
        fprintf('Point %d not found in the model domain. Please Check.',i);
        return;
    end
    
    bestCell(i,:) = {i, x_modeli, y_modeli, bestDist, best, FA_found};

    valuePath1 = ['/Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/',convertStringsToChars(FA_found),'/Water Surface'];
    value = h5read(filename,valuePath1);
    tsi(:,i) = transpose(value(best,:));  % uncommented this line
    % tsi(i,:) = value(best,:);  % commented this line
end
Date_start = datetime(h5readatt(filename,'/Plan Data/Plan Information','Simulation Start Time'),'InputFormat','ddMMMyyyy HH:mm:ss');
Date_end = datetime(h5readatt(filename,'/Plan Data/Plan Information','Simulation End Time'),'InputFormat','ddMMMyyyy HH:mm:ss');
T_Interval_model = h5readatt(filename,'/Plan Data/Plan Information','Base Output Interval');
T_Interval_unit = regexprep(T_Interval_model,'[\d"]','');
T_Inverval_value = str2double(regexp(T_Interval_model,'[\d.]+','match'));
% transpose(tsi);  % commented this line
