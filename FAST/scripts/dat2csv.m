%Written by Klaus Schroder 5/24/2021

%reads .mat files (dat) and converts them into csv for further processing in python 

%set FAST directory
%put mat files with water level (when dry: bed level) data from Quickplot
%for mask into \mask and for other scenarios into \shapes
wdir = 'C:\Users\kxs4239\Desktop\spring 2021\research\FAST';

%import mask (slr000_w000_na) results
maskDir = [wdir '\mask'];
maskMain = [maskDir '\slr000_na_wlbl.mat'];
maskCanal = [maskDir '\slr000_na_canals_wlbl.mat'];
maskMain_wlmax = dat2array(maskMain);
maskCanal_wlmax = dat2array(maskCanal);

%import scenario results
shapesDir = [wdir '\shapes'];
cd(shapesDir)
shapesList = dir('*canals_wlbl.mat');

%look through all scenarios
for k=1:length(shapesList)
    shapesMain = [shapesDir '\' shapesList(k).name(1:end-15) 'wlbl.mat'];
    shapesCanal = [shapesDir '\' shapesList(k).name];
    shapesMain_wlmax = dat2array(shapesMain);
    shapesCanal_wlmax = dat2array(shapesCanal);
    
    %mask with slr000_w000_na water levels
    %shapesMain_wlmax(~isnan(maskMain_wlmax)) = nan;
    %shapesCanal_wlmax(~isnan(maskCanal_wlmax)) = nan;
    
    %export to csv
    csvwrite([shapesMain(1:end-8) 'wl.csv'],shapesMain_wlmax')
    csvwrite([shapesCanal(1:end-8) 'wl.csv'],shapesCanal_wlmax')
end

%%
function wl_max = dat2array(fileName)

%import water level and bedlevel
wl = load(fileName);
bl = load([fileName(1:end-8) 'bl.mat']);

%rearrange as single column to match shapefile
bedlevel = reshape(bl.data.Val,1,[]);
wl_Val=reshape(wl.data.Val,length(wl.data.Val(:,1,1)),[]);

%remove areas without grid cells
bedlevel(isnan(bedlevel)) = [];
wl_Val = wl_Val(:,~all(isnan(wl_Val)));

%set areas where the water level change is very small to NaN
% for i=1:length(wl_Val(1,:))
%     if length(wl_Val(:,1))==145 %mask for slr000
%         tstart = 1;
%     else %all other scenarios
         tstart = 1;
%     end
%     if abs(max(wl_Val(tstart:end,i))-min(wl_Val(tstart:end,i))) < 0.01
%         wl_Val(:,i) = nan;
%     end
% end

%calculate max water level during simulation
wl_max = max(wl_Val(tstart:end,:),[],1);

%set areas where water level equals bed level (no depth) to NaN
% for i=1:length(wl_max)
%     if wl_max(i) == bedlevel(i)
%         wl_max(i) = nan;
%     end

end
