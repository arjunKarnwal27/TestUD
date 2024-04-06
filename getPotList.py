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
  def __init__(self, x,y,z):
    self.x = x
    self.y = y
    self.z = z

potList = []
zzzList = []
for i in range(0,len(cs[63].ContourSequence)):
    #contourData3 = cs[63].ContourSequence[i].ContourData
    zzzList.append(cs[63].ContourSequence[i].ContourData[2])

for a in range(xMin+20,xMax-20):
    for b in range(yMin+20,yMax-20):
        for c in range(zMin+20,zMax-20):
         s1 = Sphere(x,y,z)
         potList.append(s1)
