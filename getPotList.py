import numpy as np
import pydicom as dicom 
import matplotlib.path as mplPath          # Importing necessary functions
import matplotlib.pyplot as plt
import DicomRTTool
from  DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass
import math
import random

print('yo')

# reading path to DICOM file

path = "C:\\Users\\13107\\Downloads\\VSCODE\\RS.1.2.246.352.221.4951640575132688281.10910101943310371728.dcm"
ds = dicom.dcmread(path, force=True)

#print(ds)
# check both
#ds.dir("contour")

# getting only contours from dataset 

cs = ds.ROIContourSequence

# finding where 'arjun is located'
Dicom_path = r'C:\Users\13107\Desktop\Project\ok'

Dicom_reader = DicomReaderWriter(arg_max=True)
Dicom_reader.walk_through_folders(Dicom_path) # This will parse through all DICOM present in the folder and subfolders
all_rois = Dicom_reader.return_rois(print_rois=False) # Return a list of all rois present


def find_Arjun(list):
    print('yo')
    for i in range (0, len(list)):
        if('arjun' in list[i]):
            return i

arj_index = find_Arjun(all_rois)

# arrange the boundary points in (x,y,z) format
xCords = np.array([])
yCords = np.array([])
zCords = np.array([])


for b in range(0, len(cs[arj_index].ContourSequence)):
    contourData1 = cs[arj_index].ContourSequence[b].ContourData
    for x in range(0,len(contourData1),3):
        xCords = np.append(xCords, contourData1[x])
    for y in range(1,len(contourData1),3):
        yCords = np.append(yCords, contourData1[y])
    for z in range(2,len(contourData1),3):
        zCords = np.append(zCords, contourData1[z])


# creating box of max dimensions
xMax = int(max(xCords))
xMin = int(min(xCords))
yMax = int(max(yCords))
yMin = int(min(yCords))
zMax = int(max(zCords))
zMin = int(min(zCords))

print('hi')

class Sphere:
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z

potList = []
zzzList = []
for i in range(0,len(cs[63].ContourSequence)):
    #contourData3 = cs[63].ContourSequence[i].ContourData
    zzzList.append(cs[63].ContourSequence[i].ContourData[2])

for a in range(xMin+20,xMax-20):
    for b in range(yMin+20,yMax-20): # change to shrink?
        for c in range(zMin+20,zMax-20):
         s1 = Sphere(a,b,c)
         potList.append(s1)


def getDist(pt1,pt2):
   return math.sqrt((pt1.x-pt2.x)**2 + (pt1.y-pt2.y)**2 + (pt1.z-pt2.z)**2)
   

#print(getDist(potList[1],potList[200000]))

def changePotList(pt, oldPotList): #update total points list, based on point just added
   newPotList = []
   for i in range(0,len(oldPotList)):
      dist = getDist(pt,oldPotList[i])
      print(dist)
      if(dist > 39): # 40 mm (4 cm) from center to center
         newPotList.append(oldPotList[i])
   return newPotList
    
#nList = changePotList(potList[1],potList)
#print(len(nList))


for target in potList:
    z= target.z
    minZindex = 0
    minDiff = abs(zzzList[0]-z)
    for a in range(1,len(zzzList)):
        if(abs(z-zzzList[a]) < minDiff):
            minDiff = abs(z-zzzList[a])
            minZindex = a # min distance is the ath contour layer
    #
    xCords2DXY = np.array([])
    yCords2DXY = np.array([])
    contourData3 = cs[arj_index].ContourSequence[minZindex].ContourData
    for x in range(0, len(contourData3),3):
        xCords2DXY = np.append(xCords2DXY, contourData3[x])
    for y in range(1, len(contourData3),3):
        yCords2DXY = np.append(yCords2DXY, contourData3[y])
    # 
    bPointsXY = []
    for i in range(0,len(xCords2DXY)):
        bPoint = [xCords2DXY[i],yCords2DXY[i]]
        bPointsXY.append(bPoint)
    
    xy_path = mplPath.Path(bPointsXY)
    
    # distance to edge
    # how far from wall? --> TD: create new contour layer via interpolation 
    nm = 2 # negative margin type
    closeToWall = False
    for e in range(0,len(xCords2DXY)):
        if(math.sqrt(((target.x-xCords2DXY[e])**2 + (target.y-yCords2DXY[e])**2)) < nm): # change to find dist to centroid?
            closeToWall = True
    newPotList1 = []

    center = [target.x,target.y]
    if((xy_path.contains_point(center) == True) and closeToWall == False):
        print('1.0')
        newPotList1.append(target)

print(len(newPotList1)) # yea ok doesn't work at all
