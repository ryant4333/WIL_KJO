"""
A collection of functions which can be used to assess 
the MTU info from any osim model. Pulls info such as 
MTU moment arms and lengths. 

"""


'''
IMPORT MODS
'''

# import general modules
import os
import numpy as np
from numpy import array
from numpy import linalg as linalg
import scipy.interpolate as si

import copy
import opensim as osm
from os import path
import matplotlib.pyplot as plt


def getMTULengths(currModel, currState, refDOF, muscName, ranges):
##############################################################################   
    #  returns the moment arm for a specifc muscle using OPensim API
    #  Only set up for one muscle across a range of motion and once DOF
    #  Initally written for Knee MA

    #  INPUT
    #  modleDIr= char with model directory
    #  currentModel= opensim object of model
    #  currentState= opensim object of state
    #  referenceCoordinate= the coordainte you want MA taken to
    #  referenceDOI= the DOF you are moving the ROM through
    #  muscName= name of the mtu you want to analyse
    #  rangeOfMotionDeg= array with each angel you want tested in degrees

    # OUTPUT
    # fibrelength , tendonlength and MTU lengths
    
##############################################################################
    
    # reset all coords to zeros / set model in default state - MOVE TO MAIN!! 
    # currState = currModel.initializeState()

    # Call input data 
    # DOF   
    dofOI=currModel.getCoordinateSet().get(refDOF)
    # MTU
    musc=currModel.getMuscles().get(muscName)
    # MA
    MASolver=osm.MomentArmSolver(currModel)

    # range of interest to radians
    if np.size(ranges) < 2: # if 1000 means use the full ROM of the model
        # define range on radians    
        minVal = dofOI.getRangeMin()
        maxVal = dofOI.getRangeMax()
        #radRange= np.linspace(minVal,maxVal,10)
        radRange = np.arange(minVal ,maxVal + np.deg2rad(1) , np.deg2rad(1))
    else:
        radRange = np.deg2rad(ranges)
   
    # initialize empty array of results
    muscleLengths = np.zeros((np.size(radRange)))
    tendonLengths = np.zeros((np.size(radRange)))
    fibreLengths = np.zeros((np.size(radRange)))
    momentarm = np.zeros((np.size(radRange)))

    i=0;
    # Loop through each 
    for rad in radRange:
        # set position / angle of refDOF, enforceContraints = False "set coordinates even if model constraints cannot be hold"
        currModel.updCoordinateSet().get(refDOF).setValue(currState,rad, enforceContraints = False)
        currModel.realizePosition(currState) 

        # pull tendon lengths
        tendonLengths[i] = musc.getTendonLength(currState)
        # pull muscle fibre lengths
        fibreLengths[i]  = musc.getFiberLength(currState)
        # set full MTU lengths
        muscleLengths[i] = musc.getGeometryPath().getLength(currState)
        # moment arm
        momentarm[i] = MASolver.solve(currState, dofOI, musc.getGeometryPath())
        i=i+1


    return muscleLengths, momentarm, tendonLengths, fibreLengths , radRange   
    
def getMomentArms(currModel, currState, referenceCoordinate, referenceDOF, muscName, ranges):
##############################################################################

    # % returns the moment arm for a specifc muscle using OPensim API
    # % Only set up for one muscle across a range of motion and once DOF
    # % Initally written for Knee MA

    # % % INPUT
    # % modleDIr= char with model directory
    # % currentModel= opensim object of model
    # % currentState= opensim object of state
    # % referenceCoordinate= the coordainte you want MA taken to
    # % refernceDOF= the DOF you are moving the ROM through
    # % muscleOIName= name of the mtu you want to analyse
    # % rangeOfMotionDeg= array with each angel you want tested in degrees

    # % % OUTPUT
    #% momentArms= array with all the output MA

##############################################################################

    # reset all coords to zeros / set model in default state
    currState = currModel.initializeState()
    
    # Call input data 
    # COORD
    coordOI = currModel.getCoordinateSet().get(referenceCoordinate)
    # call DOF
    dofOI = currModel.getCoordinateSet().get(referenceDOF)
    # call the geometry path
    muscGeomPath = currModel.getMuscles().get(muscName).getGeometryPath()
    # define ROM
    
    
    if np.size(ranges) < 2:
        minVal = dofOI.getRangeMin()
        maxVal = dofOI.getRangeMax()
        #radRange= np.linspace(minVal,maxVal,50)
        radRange = np.arange(minVal , maxVal + np.deg2rad(1) , np.deg2rad(1))
    else:
        radRange = np.deg2rad(ranges)
    
    
    # initialize empty var for output
    momentArms=np.zeros((np.size(radRange)))
    rads = np.zeros((np.size(radRange)))
    # call the solver
    MASolver=osm.MomentArmSolver(currModel)
    i=0    
    for rad in radRange:
        dofOI.setValue(currState,rad)
        
        momentArms[i]=MASolver.solve(currState,coordOI,muscleGeomPath)
        #rads[i] = dofOI.getValue(currState)
        i=i+1

    return momentArms , radRange   
      
def getSplinedMomentArms(currModel, currState, referenceDOF, muscleOIName, ranges):
##############################################################################   
    #  returns the moment arm for a specifc muscle using OPensim API
    #  Only set up for one muscle across a range of motion and once DOF
    #  Initally written for Knee MA

    #  INPUT
    #  modleDIr= char with model directory
    #  currentModel= opensim object of model
    #  currentState= opensim object of state
    #  referenceCoordinate= the coordainte you want MA taken to
    #  refernceDOI= the DOF you are moving the ROM through
    #  muscleOIName= name of the mtu you want to analyse
    #  rangeOfMotionDeg= array with each angel you want tested in degrees

	# OUTPUT
	# fibrelength , tendonlength and MTU lengths

##############################################################################

	# reset all coords to zeros
	currState = currModel.initializeState()

	# Call input data 
	# DOF
	dofOI=currModel.getCoordinateSet().get(referenceDOF)
	minVal = dofOI.getRangeMin()
	maxVal = dofOI.getRangeMax()
	#radRange= np.linspace(minVal,maxVal,5)
	radRange= np.linspace(minVal,maxVal, 10)

	# initialize empty array of results
	muscleLengths = np.zeros((np.size(radRange)))
	i=0
	# Loop through each 
	for rad in radRange:
		# set position / angle
		currModel.updCoordinateSet().get(referenceDOF).setValue(currState,rad, enforceContraints = False)
		currModel.realizePosition(currState) 
		# set full MTU lengths
		muscleLengths[i] = currModel.getMuscles().get(muscleOIName).getGeometryPath().getLength(currState)
		i=i+1

	################## FIRST - define a spline for the lengths
	spline = si.splrep(radRange , muscleLengths)
	# Now reconstruct using the RANGES from input
	reconRanges = np.deg2rad(ranges)

	reconLens = si.splev(reconRanges,spline)

	################ NEXT - use dl/dt to derive the moment arm
	dl = np.gradient(reconLens)
	# adjsut the polarity of the angle to be positive (only knee)

	# if referenceDOF[0:-1] == 'hip_flexion_':
		# dt = np.gradient(reconRanges)
	# else:
	
	dt = np.gradient(reconRanges*-1)

	
	momentArms = dl/dt
	
	# print(reconRanges*-1)
	# # plt.plot(np.rad2deg(reconRanges),momentArms, 'k', linewidth =3.0 )
	# # plt.show()
	# pause()

	return momentArms , reconLens, reconRanges, radRange

def calcMAsplined(muscleLengths,radRange, ranges):   
    # added by EM to see whether getSplinedMomentArms can be avoided -> speed up analysis
    # small differences between calculation calcMAsplined and getSplinedMomentArms. 
    # getSplinedMomentArms splines over 10 data points instead of 150.. faster? 
    # radRange = range over which muscleLengths. ranges = range of interest in deg.

    # radRange = np.deg2rad(radRangeDeg) 
    spline = si.splrep(radRange , muscleLengths)
    # Now reconstruct using the RANGES from input
    reconRanges = np.deg2rad(ranges)

    reconLens = si.splev(reconRanges,spline)

    ################ NEXT - use dl/dt to derive the moment arm
    dl = np.gradient(reconLens)
    dt = np.gradient(reconRanges*-1)

    momentArms = dl/dt

    return  momentArms, reconLens 
    
def getJointsSpannedByMusc(currModel, muscName):

    # call osim muscle
    musc = currModel.getMuscles().get(muscName)
    
    # call (muscle path) path point set
    muscPathPointSet = musc.getGeometryPath().getPathPointSet()
    # get size path point set (how many points represent muscle path?)
    ppSize = muscPathPointSet.getSize()
    
    #########################################################################    
    # get muscle attachment points
    # get first point = origo
    origo = muscPathPointSet.get(0)
    # get last point = insertion
    insertion = muscPathPointSet.get(ppSize-1)
    
    #########################################################################    
    # get physical frames muscles are attached to
    # get first point body
    originBody=origo.getParentFrame().getName()
    # get end point body
    insertBody=insertion.getParentFrame().getName()
    # get joint set
    jointSet = currModel.getJointSet()
    i = 0
    joints_spanned = []
    # find joints spanned by muscle by matching joint's childframe and physical frames muscle is attachment to - moving distal to proximal 
    while insertBody not in originBody and insertBody not in originBody + '_offset':
        for joint in jointSet:
            if insertBody in joint.getChildFrame().getName():
                break
        joints_spanned.append(joint.getName())
        insertBody = joint.getParentFrame().getName()

        i = i+1
    
    #find bodies related to the joints.
    bodyspan=list()
    for j in joints_spanned:
        if j[:-2] == 'hip':
            bodyspan.append('pelvis')
            bodyspan.append('femur_' + j[-1] )
        elif j[:-2] == 'knee':
            bodyspan.append('femur_' + j[-1] )
            bodyspan.append('tibia_' + j[-1] )
        elif j[:-2] == 'ankle':    
            bodyspan.append('tibia_' + j[-1] )
    bodies_spanned = list(set(bodyspan)) # remove duplicates

    return joints_spanned, bodies_spanned   
    
def getMuscWrapObjectInfo(currModel, muscName, currState):    
    # initialize info
    muscObj=currModel.getMuscles().get(muscName)
    geomPath=muscObj.getGeometryPath()
    wrapSet=geomPath.getWrapSet()
    nWraps=wrapSet.getSize()   
    i=range(0,nWraps)
    # empty dict
    wrapObjInfo={}
    for x in i: # loop through each path wrap set of muscName
        # RETURN THE NAME
        wrapPathName=wrapSet.get(x).getName()
        wrapObj= wrapSet.get(x).getWrapObject()
        wrapObjName= wrapObj.getName()
        wrapObjInfo[wrapObjName]={}
        
        # RETURN THE TYPE
        type = wrapObj.getWrapTypeName()
##############################################################
##############          WRITE TO DICTIONARY
################################################################   

        if type == 'cylinder': 
            myWrap = osm.WrapCylinder.safeDownCast(wrapObj)

            wrapObjInfo[wrapObjName]['pathName']=wrapPathName
            wrapObjInfo[wrapObjName]['radius']=myWrap.get_radius()
            wrapObjInfo[wrapObjName]['translation']=[myWrap.get_translation().get(0), myWrap.get_translation().get(1), myWrap.get_translation().get(2)]
            wrapObjInfo[wrapObjName]['orientation']=[myWrap.get_xyz_body_rotation().get(0), myWrap.get_xyz_body_rotation().get(1), ]
            wrapObjInfo[wrapObjName]['length']=myWrap.get_length()
            wrapObjInfo[wrapObjName]['type']=type
            
        if type == 'ellipsoid':    
            myWrap = osm.WrapEllipsoid.safeDownCast(wrapObj)

            wrapObjInfo[wrapObjName]['pathName']=wrapPathName
            wrapObjInfo[wrapObjName]['dimensions']=[myWrap.get_dimensions().get(0), myWrap.get_dimensions().get(1), myWrap.get_dimensions().get(2)]
            wrapObjInfo[wrapObjName]['orientation']=[myWrap.get_xyz_body_rotation().get(0), myWrap.get_xyz_body_rotation().get(1), myWrap.get_xyz_body_rotation().get(2)]
            wrapObjInfo[wrapObjName]['translation']=[myWrap.get_translation().get(0), myWrap.get_translation().get(1), myWrap.get_translation().get(2)]
            wrapObjInfo[wrapObjName]['type']=type
            
        if type == 'sphere':  
            myWrap = osm.WrapSphere.safeDownCast(wrapObj)
  
            wrapObjInfo[wrapObjName]['pathName']=wrapPathName
            wrapObjInfo[wrapObjName]['radius']=myWrap.get_radius()
            wrapObjInfo[wrapObjName]['translation']=[myWrap.get_translation().get(0), myWrap.get_translation().get(1), myWrap.get_translation().get(2)]
            wrapObjInfo[wrapObjName]['type']=type
            
        if type == 'torus':   
            myWrap = osm.WrapTorus.safeDownCast(wrapObj)

            wrapObjInfo[wrapObjName]['pathName']=wrapPathName
            wrapObjInfo[wrapObjName]['inner_radius']=myWrap.get_inner_radius()
            wrapObjInfo[wrapObjName]['outer_radius']=myWrap.get_outer_radius()
            wrapObjInfo[wrapObjName]['translation']=[myWrap.get_translation().get(0), myWrap.get_translation().get(1), myWrap.get_translation().get(2)]
            wrapObjInfo[wrapObjName]['orientation']=[myWrap.get_xyz_body_rotation().get(0), myWrap.get_xyz_body_rotation().get(1), myWrap.get_xyz_body_rotation().get(2)]
            wrapObjInfo[wrapObjName]['type']=type
    
    return wrapObjInfo