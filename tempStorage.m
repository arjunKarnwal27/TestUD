%clear all

info = dicominfo("RSTest1.dcm");
contour = dicomContours(info);


contourList = contour.ROIs;
size(contour);

namList = contourList.Name;
lenNames = size(namList,1);
target = 'Arjun';
targetIndex = 0;

for i=1:lenNames
currName = namList(i);

    if(contains(currName,target) == 1) % finding which structure has 'arjun' in the name
        targetIndex = i;
    end

end

disp('hi')

allContours = contourList.ContourData{targetIndex,1}; % grab arjun at some point, for now 64 (last one) since we know

% finding max/min Z
numLayers = size(allContours);
zList = zeros(numLayers); % to fill with z values

for i=1:numLayers
zVal1 = allContours{i};
zVal2 = zVal1(1,:);
zValActual = zVal2(3);
zList(i) = zValActual;
end

zList(all(zList== 0,1),:) = []; % remove the zeroes 
minZ = min(zList);
maxZ = max(zList);


% grabbing mid layer cuz sphere

c4 = size(allContours,1);

mid = int32(c4/2);

% grab x and y from midth layer

y1 = allContours{mid,1};
xVals = y1(:,1);
yVals = y1(:,2);
newMaxX = max(xVals);
newMinX = min(xVals);
newMaxY = max(yVals);
newMinY = min(yVals);

% REDO BELOW
cenX = (newMaxX + newMinX)/2.0;
cenY = (newMaxY + newMinY)/2.0;
cenZ = (maxZ + minZ)/2.0;
%cenZTEMP = 1095;

% going to do a temporary potList algorithm for now, given the shape is a
% sphere - will work on shrink


% generating list of potential points

c = 0;
B = [];
numPtsUnfiltered = int32((newMaxX-newMinX+1)*(newMaxY-newMinY+1)*(maxZ-minZ+1)); % make absolute 
C = zeros(numPtsUnfiltered,3);
for z=newMinX:newMaxX
    for e = newMinY:newMaxY
        for f = minZ:maxZ

c = c+1;
%b = [z e f];
%B = [B; b]; %try re-assign (using 0s)
C(c,1) = z;
C(c,2) = e;
C(c,3) = f;
        end 
    end
end

% filter out those that are farther than DIST to center - since its 100
% units across, radius is 50, so 30 from center of sphere to center of proposed point will result in - add
% tolerance at some point...
dToCenter = 30;

len = size(C,1); 

tZ = zeros(size(C,1),3);

for i= len:-1:1
    xVal = C(i,1);
    yVal = C(i,2);
    zVal = C(i,3);

    thres = (xVal - cenX)^2 + (yVal - cenY)^2 + (zVal-cenZ)^2;
    sqThres = sqrt(thres);
    if(sqThres > dToCenter) %remove if not instead? 
    tZ(i) = i;
    end
end

%figure;
%plotContour(contour,64);
g = tZ(:,1);
g(all(g== 0,3),:) = []; % remove the zeroes 
testing = zeros(size(C,1),3);
C(g,:) = []; % remove the ones found to be more than dToCenter away from center
disp(size(C))

%plotting
 % add indexes, parse thru and add those to a preset list ^^^ https://www.mathworks.com/help/matlab/math/removing-rows-or-columns-from-a-matrix.html
figure;
hold on
plotContour(contour,targetIndex);
hold off

disp('done')

% guessing time!    


% deleting all within 40 mm 

% remove 0s from newPotList
%newPotList(all(newPotList == 0,2),:) = [];
% 10,000 = ~2 min w/ max 6
numTrials = 10000;
sphereCount = zeros(numTrials,1);
for i=1:numTrials % numTrials random trials
numSphere = 0;
tPotList = C;
again = true;
while(again == true)
randIndex = randi(size(tPotList,1));

tPotList = shrinkPot(tPotList(randIndex,:),tPotList);

if(size(tPotList,1) == 0)
again = false;
end
numSphere = numSphere+1;
end
sphereCount(i) = numSphere;
end

maxSpheres = max(sphereCount);
% Shrinking contour layers
% need function to find center of layer 


function y = getDist(pt1, pt2)

y = sqrt((pt1(1)-pt2(1))^2 + (pt1(2)-pt2(2))^2 + (pt1(3)-pt2(3))^2);

end

function newPotList = shrinkPot(pt,oldList)
newPotList = zeros(size(oldList,1),3);
counter = 0;
for i = 1:size(oldList,1)
v1 = oldList(i,:);
v2 = pt;
if(getDist(v1,v2) > 40) % change the 20
newPotList(i,1) = v1(1);
newPotList(i,2) = v1(2);
newPotList(i,3) = v1(3);
counter = counter + 1;
end

end
newPotList(all(newPotList == 0,2),:) = [];
end
