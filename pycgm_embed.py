#pyCGM

###########
#This file is an example of how to call the pycgm code without a console, or more likely, as a 
# way to integrate the code into your own system/software
#There are a few commented parts that show how to use some pipeline functions such as filtering. 
##########

import sys
import os
import pandas as pd

try: from pyCGM_Single.Pipelines import rigid_fill, filtering, prep,clearMarker
except: print("Could not import Pipelines.py, possibly missing scipy\n Otherwise check the directory locations")

from pyCGM_Single import pycgmStatic
from pyCGM_Single import pycgmIO
from pyCGM_Single import pycgmCalc   
from pyCGM_Single import pyCGM_Helpers
   
def loadData(dynamic_trial,static_trial,vsk_file,var):
    #load the data, usually there is some checks in here to make sure we loaded
    # correctly, but for now we assume its loaded
    motionData  = pycgmIO.loadData(dynamic_trial,var) 
    vsk = pycgmIO.loadVSK(vsk_file,dict=False)
    staticData = pycgmIO.loadData(static_trial,var)
    #The vsk is loaded, if dict=True (default), we combine
    #vsk = pycgmIO.createVskDataDict(vsk[0],vsk[1]) 
    
    return motionData,vsk,staticData

def editData(data,player):
    if player==1:
        for j in range(len(data)):
            list_temp = list(data[j].keys())
            for i in list_temp:
                data[j][i[7:]]=data[j].pop(i)
    if player==2:
        for j in range(len(data)):
            list_temp = list(data[j].keys())
            for i in list_temp:
                data[j][i[9:]]=data[j].pop(i)
    return data
        

def main():
    #Load the filenames
    #pyCGM_Helpers.py contains some sample directory data based on github directories
    args = pyCGM_Helpers.parse_args()
    dynamic_trial,static_trial,vsk_file = args.dynamic_trial,args.static_trial,args.vsk_file
    outputfile = args.outputDir + "/result_" + str(dynamic_trial[-11:-4])
    CoM_output = args.outputDir + "/result_COM_" + str(dynamic_trial[-11:-4])
    output_jc = args.outputDir + "/result_JC_" + str(dynamic_trial[-11:-4])+".csv"
    #Load a dynamic trial, static trial, and vsk (subject measurements)
    motionData,vskData,staticData = loadData(dynamic_trial,static_trial,vsk_file,args.player)
    motionData = editData(motionData,args.player)
    staticData = editData(staticData,args.player)
#     print(motionData)
    #Calibrate the static offsets and subject measurements
    calSM = pycgmStatic.getStatic(staticData,vskData,flat_foot=False)

    # #Load data as a dictionary instead of a frame-by-frame array of dictionary
    # staticDataDict = pycgmIO.dataAsDict(staticData,npArray=True)
    # motionDataDict = pycgmIO.dataAsDict(motionData,npArray=True)    

    # ####  Start Pipeline oeprations 
    # movementFilled = rigid_fill(motionDataDict,staticDataDict) 
    # movementFiltered = filtering(motionDataDict)
    # movementFinal = prep(movementFiltered)
    # motionData = movementFinal
    # ### End pipeline operations

    #hack for changing the global coordinates until finding a proper way    
    # this impacts the global angles, such as pelvis, but not the anatomical angles (e.g., hip)
    #calSM['GCS'] = pycgmStatic.rotmat(x=0,y=0,z=180) 
    #calSM['HeadOffset'] = 0  #example of manually modifying a subject measurement
    
    kinematics,joint_centers=pycgmCalc.calcAngles(motionData,start=None,end=None,vsk=calSM,splitAnglesAxis=False,formatData=False,returnjoints=True)
    kinetics=pycgmCalc.calcKinetics(joint_centers, calSM['Bodymass'])
    df = pd.DataFrame(joint_centers)
    df.to_csv(output_jc)
    
    #Write the results to a csv file, if wanted, 
    # otherwise could just return the angles/axis to some other function
    pycgmIO.writeResult(kinematics,outputfile,angles=True,axis=False)    
    pycgmIO.writeKinetics(CoM_output,kinetics) #quick save of CoM

    return

main()
