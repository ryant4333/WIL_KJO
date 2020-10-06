import opensim as osim 

import numpy as np
import os

import scipy as sp
import scipy.io
from scipy.optimize import minimize 
import scipy.optimize as optim
import scipy.stats as stats
from scipy import spatial
import mtuInfo_os4
import types

import vtk
import matplotlib.pyplot as plt
import numpy as np
import gc
##################################################################
# Functions to change
################################################################  
def ROMhip():
	init_hip_flex = -30
	fin_hip_flex = 120

	return init_hip_flex, fin_hip_flex

def dirNames():
	scenario = 6
	modelDir = './OpenSim/WrappingSurfaces/Raja_FAI.osim' #diretory not exact
	if scenario == 2 or scenario == 3 or scenario == 4: #Knee
		litValDir = '/export/home/s5165186/data/Knee/combLitVals.mat'
		ModValDir = '/export/home/s5165186/data/Knee/combModVals.mat'

	elif scenario == 1: # Hip
		litValDir = '/export/home/s5165186/data/Hip/combLitVals.mat'
		ModValDir = '/export/home/s5165186/data/Hip/combModVals.mat'

	elif scenario == 5: #Ankle    
		litValDir = '/export/home/s5165186/data/Ankle/combLitVals.mat'
		ModValDir = '/export/home/s5165186/data/Ankle/combModVals.mat'

	else: 
		litValDir = './OpenSim/WrappingSurfaces/combLitVals.mat'
		ModValDir = './OpenSim/WrappingSurfaces/combModVals.mat'
	
	if scenario == 6:
		HipROMValDir = './OpenSim/WrappingSurfaces/HipROMPenetrationCheck_Comb.mat' 
	else:
		HipROMValDir = '/export/home/s5165186/data/Hip/HipROMPenetrationCheck_Comb.mat'

	return litValDir, ModValDir, HipROMValDir, modelDir

def getInfo():
	_,_,_, modelDir = dirNames()
	model = osim.Model(modelDir)
	state = model.initSystem()
	return model, state

## to visualize penetration function
def addPoint2Ren(ren,point2add):
    ## adds points to renderer
    vtkpoints = vtk.vtkPoints()
    # Create the topology of the point (a vertex)
    vertices = vtk.vtkCellArray()

    id = vtkpoints.InsertNextPoint(point2add)
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(id)

    # Create a polydata object
    point = vtk.vtkPolyData()

    # Set the points and vertices we created as the geometry and topology of the polydata
    point.SetPoints(vtkpoints)
    point.SetVerts(vertices)

    # Visualize
    mapper_p1 = vtk.vtkPolyDataMapper()
    mapper_p1.SetInputData(point)
    actor_p1 = vtk.vtkActor()
    actor_p1.SetMapper(mapper_p1)
    actor_p1.GetProperty().SetPointSize(20)

    ren.AddActor(actor_p1)
    return ren

def visualiseVTK(meshFile, points):
    reader = vtk.vtkXMLPolyDataReader() 
    reader.SetFileName(meshFile)
    reader.Update()
    polydata = reader.GetOutput()

    # transform to a mm CS i/o meters
    transform = vtk.vtkTransform()
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transform.Scale(1000, 1000, 1000)
                
    if vtk.VTK_MAJOR_VERSION <= 5:
        transformFilter.SetInput(polydata)
    else:
        transformFilter.SetInputData(polydata)

    transformFilter.SetTransform(transform)
    transformFilter.Update()
    polydata_scaled = transformFilter.GetOutput() #mesh in PolyData structure

    # visualisation test
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    WIDTH=640
    HEIGHT=480
    renWin.SetSize(WIDTH,HEIGHT)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    meshMapper = vtk.vtkPolyDataMapper()
    meshMapper.SetInputData(polydata_scaled)
    meshActor = vtk.vtkActor()
    meshActor.SetMapper(meshMapper)
    ren.AddActor(meshActor)
    for p in points:
        addPoint2Ren(ren, p)

    iren.Initialize()
    renWin.Render()
    iren.Start()
##################################################################
# Penalty Functions
################################################################    
def nNumDeriv(array, x, y):
	# this code determines the number of derivates required
	# for the derivatve to be 0 and therefore smooth

	################################################################################    
    # Check the order of magnitude to set the threshold
	################################################################################   
    #ordMag, _ = magThreshold(array)
    #ordMag = int(ordMag) + x # add a 2 to allow some variation
    ordMag = x
    inThresh = '0.'
    
    for x in np.array(range(0,int(ordMag))):
        inThresh= inThresh + '0'
    
    if y > 9:
        posThresh = float(inThresh + str(y)) # This is stricter than the findDiscon
    else:
        posThresh = float(inThresh + '0' + str(y))

    meanVal=10
    maxVal=10
    rangeVal=10
    minVal = 10
    #array
    n=0
    
    while meanVal > posThresh and maxVal > posThresh and rangeVal > posThresh and minVal > posThresh:
    		deriv = np.gradient(array)
    		# meanVal,minVal,maxVal,rangeVal = misc.calcDescript(deriv)        
    		# meanVal = abs(meanVal)
    		meanVal = abs(np.mean(deriv))

    		# maxVal = abs(maxVal)
    		maxVal = abs(np.max(deriv))
    		# minVal = abs(minVal)
    		minVal = abs(np.min(deriv))
    		# rangeVal = abs(rangeVal)
    		rangeVal = abs(np.max(deriv)-np.min(deriv))
    		n=n+1

    		array = deriv
        
    return float(n) 

def checkPenetrationUpd(model, state, muscName):
	# checks whether muscle penetrates the bone, based on distanceRaytoMesh
	# 1) find joints that are spanned by the muscle + geometries related to the joints
	# 3) loop through geometries
	# 4) loop through number of muscle points
	# 5) loop through the x joint positions (max range model OR for which you want to check penetraion - HipROMPenetrationCheck_Comb.mat)
	# 6) check whether line between 2 consecutive points intersects with mesh. 
	# 7) if so, calculate greatest distance between muscle line and mesh. If > threshold (distanceRaytoMesh_Threshold) then penalty
	
	distanceRaytoMesh_in = 0 # inside mesh
	distanceRaytoMesh_in_max = 0 
	# distanceRaytoMesh_max = 0 # outside mesh
	distanceRaytoMesh_Threshold = 3 # Simao 4
	nseg_in = 0
	musc = model.getMuscles().get(muscName) 
	simEng = model.getSimbodyEngine()

	# return the joints spanned by the muscle
	joints_spanned, bodies = mtuInfo_os4.getJointsSpannedByMusc(model, muscName)
	# determine which bodies need to be tested

	# get the set of angles for which penetration needs to be tested
	if 'hip_' + muscName[-1] in joints_spanned: # if crossses hip joint 

		if 'knee_' + muscName[-1] in joints_spanned or 'walker_knee_' + muscName[-1] in joints_spanned: # if also crosses the knee , only use the knee
		
			# because models use angle or flexion , test
			if model.getCoordinateSet().contains('knee_angle_r') == True:
				dof = model.getCoordinateSet().get('knee_angle_' + muscName[-1])
			else:
				dof = model.getCoordinateSet().get('knee_flexion_' + muscName[-1])  
				
		else:
			dof = model.getCoordinateSet().get('hip_flexion_' + muscName[-1])
			# comb include walking, running (data from 1 subject), cut (mean of DS subjects) and squats (1 subject from MDS)
			_,_, HipROMValDir,_ = dirNames()
			# get the positions for which Penetration needs to be checked
			HipROMPenetrationCheck_aux = scipy.io.loadmat(HipROMValDir)
			HipROMPenetrationCheck = HipROMPenetrationCheck_aux['HipROMPenetrationCheck']
			
			dofAA = model.getCoordinateSet().get('hip_adduction_' + muscName[-1])
			dofIE = model.getCoordinateSet().get('hip_rotation_' + muscName[-1])
			
	else: 

		if 'knee_' + muscName[-1] in joints_spanned: # if crosses the knee , only use the knee
			# because models use angle or flexion , test
			if model.getCoordinateSet().contains('knee_angle_r') == True:
				dof = model.getCoordinateSet().get('knee_angle_' + muscName[-1])
			else:
				dof = model.getCoordinateSet().get('knee_flexion_' + muscName[-1])  
				
		else:
			dof = model.getCoordinateSet().get('ankle_angle_' + muscName[-1]) 
		
	# define the angles at which penetration is checked! 
	testAngles = np.arange(np.rad2deg(dof.getRangeMin()), np.rad2deg(dof.getRangeMax()),10) #min and max value Model.Coordinateset steps of 10deg

	# loop through bodies that the muscle could penetrate
	# loop through the different positions - set the model - get the muscle path.
	for b in bodies:	
		GeomMeshFile = getGeometryFile(muscName, b)

		ObbTree, if_distance, vtkpoints, vtkcellIds = RayCastingVTK_OBBTree(GeomMeshFile)
		
		for angle in range(testAngles.shape[0]):
			model.updCoordinateSet().get(dof.getName()).setValue(state, np.deg2rad(testAngles[angle]), enforceContraints = False)
			# model.updCoordinateSet().get(dofAA.getName()).setValue(state, np.deg2rad(testAngles[angle,1]),enforceContraints = False)
			# model.updCoordinateSet().get(dofIE.getName()).setValue(state, np.deg2rad(testAngles[angle,2]),enforceContraints = False)

			model.realizePosition(state)

			pathPoints = musc.getGeometryPath().getCurrentPath(state)
			for k in range(pathPoints.getSize()-1):
				# test whether the muscle points are on wrapping surface (wrap points) or fixed. If on the same wrapping surface, points not taken into account for check bone penetration. 
				# with the idea that muscle sliding over WS is not worst case scenario   
				# p0T = pathPoints.get(k).getWrapObject() == None # if the points are wrap points, the type returned will be opensim.opensim.WrapObject
				# p1T = pathPoints.get(k+1).getWrapObject() == None # if it is not a wrap point, the function will return an array of type NoneType

				pt0LV = osim.Vec3()
				pt1LV = osim.Vec3()
				
				# pt0LV = position MusclePath current state in CS body b  
				simEng.transformPosition(state ,pathPoints.get(k).getParentFrame(), pathPoints.get(k).getLocation(state) , model.getBodySet().get(b) , pt0LV)
				simEng.transformPosition(state ,pathPoints.get(k+1).getParentFrame(), pathPoints.get(k+1).getLocation(state) , model.getBodySet().get(b) , pt1LV)
				
				#3d points of 2 consecutive points of muscle path 
				pt0 = np.array(( pt0LV.get(0), pt0LV.get(1), pt0LV.get(2) )) * 1000 
				pt1 = np.array(( pt1LV.get(0), pt1LV.get(1), pt1LV.get(2) )) * 1000
	
				# checks whether muscle path points are related to wrappingsurface, if consecutive points are related to the same wrappingsurface
				# then these points not taken into account.
				# if p0T == False: 
				# 	# point 1 is a wrap points					
				# 	if p1T == False: 
				# 		# point 1 and 2 are wrap points					
				# 		# now check the name of each of the wrap objects
				# 		p0N = pathPoints.get(k).getWrapObject().getName()
				# 		p1N = pathPoints.get(k+1).getWrapObject().getName()						
				# 		if p0N == p1N:
				# 			# means point 1 and point 2 both belong to the same wrap surface, therefore skip - until wrapLine implemented(?)
				# 			continue # skip this point (back to for loop)
				
				# check whether line between pt0 to pt1 intersects with mesh
				ObbTree.IntersectWithLine(pt0,pt1,vtkpoints,vtkcellIds)
				pointsIntersection = getDataVTKpoints(vtkpoints)

				if pointsIntersection:					
					distanceRaytoMesh_in = distanceRayMesh(pointsIntersection, if_distance, pt0, pt1)

					# if distance in mesh > threshold add up to penalty.					
					if distanceRaytoMesh_in > distanceRaytoMesh_Threshold:
						# if angle > 14:
						# 	print(testAngles[angle])
						# 	points = [pt0,pt1]
						# 	visualiseVTK(GeomMeshFile, points)


						distanceRaytoMesh_in_max = distanceRaytoMesh_in_max + distanceRaytoMesh_in
						nseg_in +=1


	# define penalty function -> exponential increase the more penetration. 
	a = 2 # the higher the steeper the exponential
	c = distanceRaytoMesh_Threshold # cutoff - penalty = 1
	penDistanceRayMesh_in = np.exp(a * (distanceRaytoMesh_in_max - c))


	return penDistanceRayMesh_in
    
def distanceRayMesh(pointsIntersection, implicit_function, pSource, pTarget):
    # checks whether the muscle (line between intersection points) penetrates the bone too much (negative value if muscle inside mesh). 
	# If so, distanceRay2Mesh is the distance2mesh of that datapoint
 	# 1) check whether nodes are within the mesh, if so, return without finding max value (- reduce computational time)
	# 2) create multiple test points on the line between the muscle nodes
	# 3) calculate distance between each test point and mesh.
	# 4) find greatest distance muscle (test point) and mesh = distanceRaytoMesh

	# 1): 
	# if implicit_function.FunctionValue(pSource) < -distanceRaytoMesh_Threshold:
	# 	return abs(implicit_function.FunctionValue(pSource))
		
	# elif implicit_function.FunctionValue(pTarget) < -distanceRaytoMesh_Threshold:
	# 	return abs(implicit_function.FunctionValue(pTarget))

	#create array with intersection points muscle with bone mesh
	#####

	pointsIntersectionFinal=[]
	
	numPointsIntersection=range(0,len(pointsIntersection))
	
	if len(pointsIntersection)==1:
		pointsIntersectionFinal.append(pSource)	
		pointsIntersectionFinal.append(np.array(pointsIntersection[0]))
		pointsIntersectionFinal.append(pTarget)		
	else:
		for j in numPointsIntersection:
			pointsIntersectionFinal.append(np.array(pointsIntersection[j]))

	pointInRay=[]

	# to test the distance of muscle (Ray) to bone (mesh) for point of muscle in bone 
	# devide the distance between 2 intersection points (inside mesh) in 10 equal distances,
	# such that distance to mesh of these inbetween points can be tested.

	for n in range(0,len(pointsIntersectionFinal[:-1])):
	
		point1 = pointsIntersectionFinal[n]
		point2 = pointsIntersectionFinal[n+1]

		u = np.arange(0.1,1,0.1)
		sizeU = range(0,len(u))

		#create an array of 10 point between p1 and p2
		# p1 + u[k]*(p2-p1) = (1-u(k))*p1 + u(k)*p2
		for k in sizeU:
			pointInRay.append(np.array(((1-u[k])*point1[0]+u[k]*point2[0],(1-u[k])*point1[1]+u[k]*point2[1],(1-u[k])*point1[2]+u[k]*point2[2])))

	pointInRaySteps=range(0,len(pointInRay))
	distancesRayMesh=[]
	
	#check distance from muscle 2 mesh, for all 10 points within ray (i.e bone)
	for t in pointInRaySteps:
		# distancesRayMesh.append(implicit_function.FunctionValue(pointInRay[t]))
		distancesRayMesh.append(implicit_function.FunctionValue(pointInRay[t]))

	# minimum value - all values within the surface are negative values, outside surface are positive and on surface 0.
	# https://vtk.org/doc/nightly/html/classvtkImplicitPolyDataDistance.html 	


	distanceRaytoMesh = np.amin(distancesRayMesh)

	return abs(distanceRaytoMesh)
    
 	##################################################################
	# Modules to test and edit wrapping surfaces
	################################################################  

def calcNormalizedError(target, test):
    
    # # calculate the RMS 
    numVals = range(0,np.size(target))
    err = np.zeros((1,np.size(target)))
    normErr =  np.zeros((1,np.size(target)))
    
    for x in numVals:
        #err[0,x] = target[x] - test[x] 
        normErr[0,x] = (target[x] - test[x]) / target[x]
        
   
    #errMean = np.mean(abs(err))
    #errMax = np.max(abs(err))
    normErrMean = np.nanmean(abs(normErr))
    normErrMax = np.nanmax(abs(normErr))
    
    simularity = normErrMean + normErrMax
    #simularity = errMean + errMax
    
    return float(simularity)   

def penDistanceWrapMesh(model, state, muscName, Wrap2opt):
	# calculate shortest distance from (center) wrap to mesh - hopefully to avoid the wrap to be fitted to far from the mesh.
	WrapDict = mtuInfo_os4.getMuscWrapObjectInfo(model, muscName)
	wrap_opt = wrap2optimise(muscName, Wrap2opt, WrapDict)

	dWarpMesh = 0
	for y in wrap_opt:
		pWrap = np.zeros(3)
		for x in range(0,3):
			pWrap[x] = wrap_opt[y]['translation'][x]*1000

		pathName = wrap_opt[y]['pathName']

		wrapObj=model.getMuscles().get(muscName).getGeometryPath().getWrapSet().get(pathName).getWrapObject()
		frame = wrapObj.getFrame().getName()

		GeomMeshFile = getGeometryFile(muscName, frame)
		_, iF, _, _ = RayCastingVTK_OBBTree(GeomMeshFile)	
		d = iF.FunctionValue(pWrap) # negative values = inside mesh, positive = outside

		if d > dWarpMesh:
			dWarpMesh = d
	
	# create penalty distance wrap 2 mesh
	a = 4 # the higher the steeper the increase of exponential. 
	c = 4 # threshold 
	penWrapMesh = np.exp(a * (dWarpMesh - c))

	return penWrapMesh

def norcorr(x,y):
    # normalised correlation
    # values between 1 (max corr - simularity) and -1 (no simularity)
    corr = np.dot(x,y)
    scalex = np.sum(x**2)
    scaley = np.sum(y**2)
    scale_tot = np.sqrt(scalex * scaley)
    
    return corr/scale_tot

def Polarity(x,y):
    # counts the samples for which x and y do not have the same sign -> moment arm check model and lit (flx = flx?)
	# make sure both signals have the same x-axis.	
	x_sign = np.signbit(x)
	y_sign = np.signbit(y)
	n_signDiff = len(np.where(x_sign!=y_sign)[0])

	# pen = 2*np.exp(n_signDiff)-2
	return n_signDiff

def calcArcLengthFFTem(signal):
	# calculate the arc length of a discrete FFT
	# measure of smootheness (S.Balasubramanian etal. 2012)
	## apply hanning window:
	fs = len(signal)
	signalW = signal*np.hanning(len(signal)) 

	##  zero-padding (increase speed fft by having a length 2^n)
	K = 2**(np.ceil(np.log2(len(signal))) + 4)
	Kc = int(K/fs * 1/2*fs) #freq res  = fs/K, max freq = 1/2*fs 
	
	signal_zp = np.zeros(int(K))
	signal_zp[0:len(signal)] = signalW

	# FFT (1-directional)
	fft = np.fft.fft(signal_zp)
	freq = np.fft.fftfreq(signal_zp.size)
	i = freq >= 0
	mag = abs(fft[i]) #magnitude
	pw = mag**2 * 1/Kc #power
	phase = np.angle(fft[i]) #phase

	pw_nor = pw/max(pw) # normalise to max, so high power at low frequency removed in smooth signals
	iphase_max = mag == np.max(mag)
	phase_main = phase[iphase_max]

	# # calculate arc length
	z = np.zeros(Kc-1)

	for i in range(0,Kc-1):
		dv = pw_nor[i+1]-pw_nor[i]
		z[i] = np.sqrt((1/(Kc-1))**2 + dv**2)

	n = sum(z)

	return n, phase_main

###########################################################################
### Defintions used ##
###########################################################################
def loadCombLitValsHPC():
	# this function loads MAT files with Literature Data on MA and MTU length

	litValDir,_,_,_ = dirNames()

	litValsMat = scipy.io.loadmat(litValDir)
    
    # seperate into muscs
	litVals = {}
	for keys in litValsMat :
		# test if is MATLAB info
		t= keys[0] == '_'
		# if isn't MATLAB info write to dict
		if t == 0:
			litVals[keys] = {}
			# call the entries in the dict  - the names
			ent = litValsMat[keys].dtype.names
			# loop thorugh each ent
			for e in ent:
				litVals[keys][e] =  litValsMat[keys][e][0,0]
		
	combinedLitVals = litVals['combLitVals']  

	return combinedLitVals  

def loadCombModValsHPC():
	# this loads MAT file data to load 
	_, ModValDir,_,_ = dirNames()

	litValsMat = scipy.io.loadmat(ModValDir)
	
	# seperate into muscs
	litVals = {}
	for keys in litValsMat :
		# test if is MATLAB info
		t= keys[0] == '_'
		# if isn't MATLAB info write to dict
		
		if t == 0: # this returns only for the combModVals key
		
			litVals[keys] = {} # create empty struct for combModVals
			# call the entries in the dict  - the names
			
			ent = litValsMat[keys].dtype.names # returns G2392 and AP
			# loop thorugh each ent
			for e in ent:
				litVals[keys][e] = {} # create an empty dict for G2392 and AP
				muscs = litValsMat[keys][e][0,0].dtype.names # return the full list of muscsle
				
				for m in muscs:
				
					litVals[keys][e][m] = {}
					
					litVals[keys][e][m]['length'] = litValsMat[keys][e][0,0][m][0,0]['length'][0,0]
					litVals[keys][e][m]['momentArm'] = litValsMat[keys][e][0,0][m][0,0]['momentArm'][0,0]

		
	CMV = litVals['combModVals']    
	return CMV 
  
def RayCastingVTK_OBBTree(meshFile):
    # read meshFile and transform to polyData file -> something readable for Python
    # https://pyscience.wordpress.com/2014/09/21/ray-casting-with-python-and-vtk-intersecting-linesrays-with-surface-meshes/
    reader = vtk.vtkXMLPolyDataReader() 
    reader.SetFileName(meshFile)
    reader.Update()
    polydata = reader.GetOutput()

    transform = vtk.vtkTransform()
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transform.Scale(1000, 1000, 1000)
                
    if vtk.VTK_MAJOR_VERSION <= 5:
        transformFilter.SetInput(polydata)
    else:
        transformFilter.SetInputData(polydata)

    transformFilter.SetTransform(transform)
    transformFilter.Update()
    polydata_scaled = transformFilter.GetOutput() #mesh in PolyData structure

    #use vtkOBBTree for ray casting
    obbTree = vtk.vtkOBBTree()
    obbTree.SetDataSet(polydata_scaled)
    obbTree.BuildLocator() #creats OBB tree.
	# create vtk objects for calc intersections
    vtkpoints  = vtk.vtkPoints()
    vtkcellIds = vtk.vtkIdList()
    # create implicit function to calc distance penetrated muscle to mesh
    iF = vtk.vtkImplicitPolyDataDistance()
    iF.SetInput(polydata_scaled)

    return [obbTree, iF, vtkpoints, vtkcellIds]
	
def getDataVTKpoints(points):
    # read the intersection points obtained using vtkObbTree
    pointsIntersectionVTK = points.GetData()
    noPointsVTKIntersection = pointsIntersectionVTK.GetNumberOfTuples()
    pointsIntersection = []
    for idx in range(noPointsVTKIntersection):
        _tup = pointsIntersectionVTK.GetTuple3(idx)
        pointsIntersection.append(_tup)
        
    return pointsIntersection

def editMuscWraps(vals, model, muscName, wrapDict, Wrap2opt):    
	# function to change the position of the wrappingsurfaces associated with the muscle
	
	# global currTorusTranslation	
	# currTorusTranslation=np.array([])
	# muscObj = model.getMuscles().get(muscName)
	# >> loop through each of the wrapping surfaces 
	# need to be generic when updating the properties of the 
	# surface

	#check whether all wrapping surfaces need to be optimised - defined in Wrap2opt
	# if Wrap2opt is empty, then all wrapping surfaces related to muscle optimised.
	wrap_opt = wrap2optimise(muscName, Wrap2opt, wrapDict)

	# nShape=int(np.size(objs,0))
	# n=range(0,nShape)
	# define an index where to start for the next wrapping surfaces
	startInd = 0 #?

	for x in wrap_opt:
		# call the opensim object
		pathName=wrap_opt[x]['pathName']
		wrapObj=model.getMuscles().get(muscName).getGeometryPath().getWrapSet().get(pathName).getWrapObject()
		
		# what type of surfaces ?
		type = wrap_opt[x]['type']
		
		if type == 'sphere':
			# Tx Ty Tz R
			# adjust Translation
			myWrap = osim.WrapSphere.safeDownCast(wrapObj)

			# vals - values of the optimiser (within the given boundaries) 
			myWrap.set_translation(osim.Vec3(vals[startInd+0],vals[startInd+1],vals[startInd+2]))

			# adjust radius				
			if vals[startInd+3] > 0:
				myWrap.set_radius(vals[startInd+3])
			else:
				radVal = wrap_opt[x]['radius']
				myWrap.set_radius( radVal , radProp , 0)

			# adjust the starting index for the next object
			startInd = startInd + 4
			model.updWorkingState()

		if type == 'cylinder':
			# Tx Ty Tz R Ox Oy Oz
			# adjust Translation
			myWrap = osim.WrapCylinder.safeDownCast(wrapObj)
			myWrap.set_translation(osim.Vec3(vals[startInd+0],vals[startInd+1],vals[startInd+2]))
			# adjust radius
			if vals[startInd+3] > 0:
    				myWrap.set_radius(vals[startInd+3])
			else:
				radVal = wrap_opt[x]['radius']
				myWrap.set_radius( radVal , radProp , 0)

			# adjust Orientation
			myWrap.set_xyz_body_rotation(osim.Vec3(vals[startInd+4],vals[startInd+5],myWrap.get_xyz_body_rotation().get(2)))
			
			# adjust the starting index for the next object
			startInd = startInd + 6
			model.updWorkingState()
			
		if type == 'ellipsoid':
			# Tx Ty Tz Ox Oy Oz Dx Dy Dz
			# adjust Translation
			myWrap = osim.WrapEllipsoid.safeDownCast(wrapObj)
			myWrap.set_translation(osim.Vec3(vals[startInd+0],vals[startInd+1],vals[startInd+2]))
		
			# adjust Orientation
			myWrap.set_xyz_body_rotation(osim.Vec3(vals[startInd+3],vals[startInd+4],vals[startInd+5]))

			# adjust Dimensions
			myWrap.set_dimensions(osim.Vec3(vals[startInd+6],vals[startInd+7],vals[startInd+8]))
			
			# adjust the starting index for the next object
			startInd = startInd + 9
			# state = model.updWorkingState()
			
		if type == 'torus':
			# Tx Ty Tz Ox Oy Oz Rin Rout
			# adjust Translation

			myWrap = osim.WrapTorus.safeDownCast(wrapObj)
			myWrap.set_translation(osim.Vec3(vals[startInd+0],vals[startInd+1],vals[startInd+2]))
		
			# adjust Orientation
			myWrap.set_xyz_body_rotation(osim.Vec3(vals[startInd+3],vals[startInd+4],myWrap.get_xyz_body_rotation().get(2)))
			
			# inner radius is determined as outer_radius - difference between outer and inner radius
			# done to avoid inner radius > outer radius during optimization
			myWrap.set_inner_radius(vals[startInd+6] - vals[startInd+5])

			# adjust Outer radius
			myWrap.set_outer_radius(vals[startInd+6])

			# adjust the starting index for the next object
			startInd = startInd + 7
			model.updWorkingState()	
	# model.initSystem()
	# gc.collect()
	return model

def collectOptimVals(x0, sol, model, muscName, wrapDict, Wrap2opt):

	#muscObj = model.getMuscles().get(muscName)
	muscDict = {}

	# now loop through each of the wrapping surfaces 
	# need to be generic when updating the properties of the 
	# surface

	objs=wrapDict.items()

	if Wrap2opt.has_key(muscName) == True: 
		objs_aux=[]
		nObj_aux=int(np.size(Wrap2opt[muscName]))
		nObj=range(0,nObj_aux)

		nShape=int(np.size(objs,0))
		n=range(0,nShape)
		for k in nObj:
			for kk in n:
				if objs[kk][0]==Wrap2opt[muscName][k]:
					objs_aux.append(objs[kk])
		objs=[]
		objs=objs_aux
		
	nShape=int(np.size(objs,0))
	n=range(0,nShape)
	# define an index where to start for the next wrapping surfaces
	startInd = 0

	muscDict[muscName] = {}

	for i in n :

		tempObj=objs[i]
		tempName=tempObj[0]
	   
		# call the opensim object
		pathName=wrapDict[tempName]['pathName']
		wrapObject=model.getMuscles().get(muscName).getGeometryPath().getWrapSet().get(pathName).getWrapObject()

		# what type of surfaces ?
		type = wrapDict[tempName]['type']
		wrapName = wrapObject.getName()


		muscDict[muscName][pathName] = {}
		muscDict[muscName][pathName]['wrapObject'] = wrapName
		muscDict[muscName][pathName]['wrapType'] = type

		if type == 'sphere':
		# Tx Ty Tz R
		# Translation
			
			if np.isnan(sol[startInd+0]) == False:
				trans = ( sol[startInd+0] , sol[startInd+1] , sol[startInd+2] )
			else : 
				trans = ( x0[startInd+0] , x0[startInd+1] , x0[startInd+2] )     
				
			muscDict[muscName][pathName]['translation'] = trans
				
		# Radius
			if np.isnan(sol[startInd+3]) == False:
				rad = sol[startInd+3] 
			else:
				rad = x0[startInd+3] 
				
			muscDict[muscName][pathName]['radius'] = rad
			
		# adjust the starting index for the next object
			startInd = startInd + 4
			
			
		if type == 'cylinder':
			# Tx Ty Tz R Ox Oy Oz
			# adjust Translation
		   
			if np.isnan(sol[startInd+0]) == False:
				trans = ( sol[startInd+0] , sol[startInd+1] , sol[startInd+2] )
			else : 
				trans = ( x0[startInd+0] , x0[startInd+1] , x0[startInd+2] )   
				
			muscDict[muscName][pathName]['translation'] = trans
			
			# Radius
			if np.isnan(sol[startInd+3]) == False:
				rad = sol[startInd+3] 
			else:
				rad = x0[startInd+3] 
				
			muscDict[muscName][pathName]['radius'] = rad
				
			# adjust Orientation
		   
			if np.isnan(sol[startInd+4]) == False:
				# orient =( sol[startInd+4] , sol[startInd+5], sol[startInd+6] )
				orient =( sol[startInd+4] , sol[startInd+5])
			else:
				# orient =( x0[startInd+4] , x0[startInd+5], x0[startInd+6] )
				orient =( x0[startInd+4] , x0[startInd+5])

			muscDict[muscName][pathName]['orientation'] = orient
				
			# adjust the starting index for the next object
			startInd = startInd + 6
			
		if type == 'ellipsoid':
		# Tx Ty Tz Ox Oy Oz Dx Dy Dz
		# adjust Translation
		   
			if np.isnan(sol[startInd+0]) == False:
				trans = ( sol[startInd+0] , sol[startInd+1] , sol[startInd+2] )
			else : 
				trans = ( x0[startInd+0] , x0[startInd+1] , x0[startInd+2] )   
				
			muscDict[muscName][pathName]['translation'] = trans
				
		# adjust Orientation
			
			if np.isnan(sol[startInd+4]) == False:
				orient =( sol[startInd+4] , sol[startInd+5], sol[startInd+6] )
			else:
				orient =( x0[startInd+4] , x0[startInd+5], x0[startInd+6] )

			muscDict[muscName][pathName]['orientation'] = orient
			
		# adjust Dimensions
			
			if np.isnan(sol[startInd+6]) == False:
				dim = ( sol[startInd+6] , sol[startInd+7] , sol[startInd+8])
			else:
				dim = ( x0[startInd+6] , x0[startInd+7] , x0[startInd+8])
				
			muscDict[muscName][pathName]['dimensions'] = dim
			
				
		# adjust the starting index for the next object
			startInd = startInd + 9
				   
		if type == 'torus':
		# Tx Ty Tz Ox Oy Oz Rin Rout
		# adjust Translation
		   
			if np.isnan(sol[startInd+0]) == False:
				trans = ( sol[startInd+0] , sol[startInd+1] , sol[startInd+2] )
			else : 
				trans = ( x0[startInd+0] , x0[startInd+1] , x0[startInd+2] )   
				
			muscDict[muscName][pathName]['translation'] = trans
				
		# adjust Orientation
		   
			if np.isnan(sol[startInd+3]) == False:
				# orient =( sol[startInd+3] , sol[startInd+4], sol[startInd+5] )
				orient =( sol[startInd+3] , sol[startInd+4])
			else:
				# orient =( x0[startInd+3] , x0[startInd+4], x0[startInd+5] )
				orient =( x0[startInd+3] , x0[startInd+4])

			muscDict[muscName][pathName]['orientation'] = orient
			
		# adjust inner Radius
		
			if np.isnan(sol[startInd+5]) == False:
				rad = sol[startInd+6] - sol[startInd+5] 
				# rad = 0.0009
			else:
				rad = x0[startInd+6] - x0[startInd+5]
				# rad = 0.0009				
				
			muscDict[muscName][pathName]['inner_radius'] = rad			
		
		# adjust outer Radius
		
			if np.isnan(sol[startInd+6]) == False:
				rad = sol[startInd+6] 
			else:
				rad = x0[startInd+6] 
				
			muscDict[muscName][pathName]['outer_radius'] = rad			
			
		# adjust the starting index for the next object
			startInd = startInd + 7	
				   
	return muscDict 

def bounds_WS(initCond, bounds):
	# calculates lower and upper bounds for the WS. 
	# InitCond = initial condition of wrapping surface [array 3], 
	# bounds is the deviation in x-, x+, y-,y+, z-, z+ [array 6]
	
	minX = initCond[0] - bounds[0]
	maxX = initCond[0] + bounds[1]

	minY = initCond[1] - bounds[2]
	maxY = initCond[1] + bounds[3]
	
	minZ = initCond[2] - bounds[4]
	maxZ = initCond[2] + bounds[5]
	
	b0 = ( minX , maxX )
	b1 = ( minY , maxY )
	b2 = ( minZ , maxZ ) 

	return b0, b1, b2

def wrap2optimise(muscName, Wrap2opt, wrapObjModel):
	# input: Muscle name, WrapObj that you want to optimise, Wraps associated with the muscle.
	# Checks which wrapping surfaces to optimise (either all related to the muscle, or the ones specified in Wrap2opt)
	wrap_opt={}

	if Wrap2opt.get(muscName) is not None: 
		for k in Wrap2opt[muscName]: #loop through wrapping surfaces that you want to optimise 
			for kk in wrapObjModel: # loop through wrapping surfaces for each muscle in model
				if kk == k:
					wrap_opt[kk] = wrapObjModel[kk]
	else:
		wrap_opt=wrapObjModel

	return wrap_opt

def checkROM(init, fin, data):
    # check rom model/literature with the rom of interest (defined in ROMhip),
    # to make sure that only the relevant data (around range of interest) is used.

    init = int(init)
    fin = int(fin)
    init_hip_flex, fin_hip_flex = ROMhip()

    if init < init_hip_flex:
        for i in range(init-1,fin+1):
            if data[0,i] == init_hip_flex:
                init_index = i-1
                break
    else:
        init_index = 0
                    
    if fin > fin_hip_flex:
        for i in range(init-1,fin+1):
            if data[0,i] == fin_hip_flex:
                fin_index = i+1
                break	
    else:
        fin_index = len(data[0,:])-1		

    return init_index, fin_index

def getBoundaries(currModel, muscName, Optim_Thresholds, Wrap2opt):
	# previously called "editWrapSurfHPC"
	# This function is used to edit the properties of wrapping surfaces 
	# remove any discontinuties in the MTU length or MA
    
	################################################################################    
    # call wrap objects associated with muscles
	################################################################################
	wrapObjmodel=mtuInfo_os4.getMuscWrapObjectInfo(currModel, muscName)

	# check whether all wrapping surfaces need to be optimised - defined in Wrap2opt
	# if Wrap2opt is empty, then all wrapping surfaces related to muscle optimised.
	wrap_opt = wrap2optimise(muscName, Wrap2opt, wrapObjmodel)

	if np.size(wrap_opt) == 0:
		print(" No wrapping surface associated with this MTU")
		muscWrapDict ={'emptyDict':'NoWraps'}
		return muscWrapDict
	else: print(" Editting wrapping surfaces now ..")
		
	x0 = []    
	bnds = []

	################################################################################
	# loop through each wrapping surfaces and concatenate the inital conditions and bounds into a list
	################################################################################               
	for x in wrap_opt:

		Wraptype =  wrap_opt[x]['type']
		# bounds WS translation (for each type of wrap)
		initTrans = wrap_opt[x]['translation'] 
		
		if Wraptype == 'cylinder' :
		
			initRot = wrap_opt[x]['orientation']
			initRadVal = wrap_opt[x]['radius']
					
			if x in Optim_Thresholds: 
				# Translation: Optim_Thresholds 0:6 contains lb/ub translation xyz.
				bounds_trans = Optim_Thresholds[x][0:6] 
				b0,b1,b2 = bounds_WS(initTrans,bounds_trans)			
				# Rotation: only in x and y, NOT z
				bounds_rot = np.ones(4)*np.deg2rad(Optim_Thresholds[x][6])
				bounds_rot = np.append(bounds_rot,np.zeros(2)) # no z
				initRot.append(0) #doesnt count - bad coding but works
				b4,b5,_   = bounds_WS(initRot,bounds_rot)					
				# radius 	
				minRad=initRadVal*Optim_Thresholds[x][7]
				maxRad=initRadVal*Optim_Thresholds[x][8]
				
			else:	# hard coded
				# translation
				bounds_trans = np.ones(6)*0.025 
				b0,b1,b2 = bounds_WS(initTrans,bounds_trans)
				# orientation 
				bounds_rot = np.ones(4)*np.deg2rad(10)
				bounds_rot = np.append(bounds_rot,np.zeros(2)) # no z
				initRot.append(0) #doesnt count - bad coding but works
				b4,b5,_   = bounds_WS(initRot,bounds_rot)		
				# radius	
				minRad=initRadVal*0.80
				maxRad=initRadVal*1.2

			b3 = ( minRad , maxRad )
			
			x0T = ( initTrans[0] , initTrans[1] , initTrans[2] , initRadVal, initRot[0] , initRot[1])
			bndsT = [b0, b1, b2, b3, b4, b5]
			
		elif Wraptype == 'sphere' :
		
			initRadVal=wrap_opt[x]['radius']
			
			if x in Optim_Thresholds:
				# Translation: Optim_Thresholds 0:6 contains lb/ub translation xyz.
				bounds = Optim_Thresholds[x][0:6] 
				b0,b1,b2 = bounds_WS(initTrans,bounds)		 
				# Radius	
				minRad=initRadVal*Optim_Thresholds[x][6]
				maxRad=initRadVal*Optim_Thresholds[x][7]				
			else:
				# Translation: hard coded translation xyz of 0.025
				bounds_trans = np.ones(6)*0.025 
				b0,b1,b2 = bounds_WS(initTrans,bounds_trans)
				# Radius
				minRad=initRadVal*0.8
				maxRad=initRadVal*1.2
			
			b3 = ( minRad , maxRad )

			x0T = ( initTrans[0] , initTrans[1] , initTrans[2] , initRadVal)
			bndsT = [b0, b1, b2, b3]
			
		elif Wraptype == 'ellipsoid' :    
			# Translation: hard coded translation xyz of 0.025
			bounds_trans = np.ones(6)*0.025 
			b0,b1,b2 = bounds_WS(initTrans,bounds_trans)

			# Rotation: hard coded orientation xyz of  10 degrees
			initRot = wrap_opt[x]['orientation']
			bounds_rot = np.ones(6)*0.174533 # 10 degrees
			b3,b4,b5 = bounds_WS(initRot,bounds_rot)

			# dimensions: hard coded 0.02 - min cannot be < 0 
			initDim = wrap_opt[x]['dimensions']
			bounds_dim = np.ones(6)*0.02 
			b6,b7,b8 = bounds_WS(initDim,bounds_dim)

			if b6[0] < 0:
				b6[0] = initDim[0]
			if b7[0] < 0:
				b7[0] = initDim[1]
			if b8[0] < 0: 
				b8[0] = initDim[2]        
		
			x0T = ( initTrans[0] , initTrans[1] , initTrans[2] , initRot[0] ,  initRot[1] ,  initRot[2] , initDim[0], initDim[1], initDim[2])
			bndsT = [b0, b1, b2, b3, b4, b5, b6 , b7 , b8]

		elif Wraptype == 'torus' :
		 
			initTorusTranslation=np.array([initTrans[0],initTrans[1],initTrans[2]])

			initRot = wrap_opt[x]['orientation']
			
			# Outer and inner radius
			initOutRadVal=wrap_opt[x]['outer_radius']
			
			if x in Optim_Thresholds: 
				# Translation: Optim_Thresholds 0:6 contains lb/ub translation xyz.
				bounds_trans = Optim_Thresholds[x][0:6] 
				b0,b1,b2 = bounds_WS(initTorusTranslation,bounds_trans)

				# Rotation: only in x and y - No rotation in z
				bounds_rot = np.ones(4)*np.deg2rad(Optim_Thresholds[x][6])
				bounds_rot = np.append(bounds_rot,np.zeros(2))

				b3,b4,_ = bounds_WS(initRot,bounds_rot)				
				
				minRad = Optim_Thresholds[x][7]
				maxRad = Optim_Thresholds[x][8]
				# inner radius of torus is set as outer_radius - diff_in_out_radius
				minRadDiff = Optim_Thresholds[x][9]
				maxRadDiff = Optim_Thresholds[x][10]
				initRadDiffVal = Optim_Thresholds[x][11]

			b6 = ( minRad , maxRad )
			b5 = ( minRadDiff , maxRadDiff )

			x0T = ( initTrans[0] , initTrans[1] , initTrans[2] ,initRot[0] ,  initRot[1] , initRadDiffVal , initOutRadVal)
			bndsT = [b0, b1, b2, b3, b4, b5, b6]	
			
		#####################################################################
		# Concatenate the desgin variabels and bounds into single val
		####################################################################
		# loop through x0T and append x0T
		for v in x0T:
			x0.append(v)
		for b in bndsT:
			bnds.append(b)
		print(wrap_opt[x]['type'])

	lb = []
	ub = []

	for x2 in bnds:
		lb.append(x2[0])
		ub.append(x2[1])
		
	return lb, ub

def getModelInformation(model, state, dof, muscName, litMA_range):

	if dof[0:-1] == 'hip_flexion_': 
		init_hip_flex, fin_hip_flex = ROMhip()

		# get muscle length over the range of interest for 'dof' of interest
		MuscLen, MA,_,_, radRange = mtuInfo_os4.getMTULengths(model, state, dof, muscName, np.array(range(init_hip_flex,fin_hip_flex)))
		# calculate momentarm (MA) over range literature data
		MA_litrange,_ = mtuInfo_os4.calcMAsplined(MuscLen, radRange, litMA_range)

	return MuscLen, MA, MA_litrange, radRange

def getGeometryFile(muscName, Geom):
	initDir = 'C:/PhD/FAI/HipMTUOptim/HPC/models/geom/'
	if Geom == 'pelvis':
		GeomMeshFile = initDir + muscName[-1] + '_' + Geom + '.vtp'
	else:
		GeomMeshFile = initDir + muscName[-1] + '_' + Geom[0:-2] + '.vtp'

	return GeomMeshFile

def getNderivGenModel(muscName, dof, osim2Lit):
	modData = loadCombModValsHPC() # generic model data       
	if muscName in modData['G2392']:			
		modelName = 'G2392'
	elif muscName in modData['LLM']:
		modelName = 'LLM'

	if dof[0:-1] == 'hip_flexion_': 
		# extract generic model data
		init = modData[modelName][muscName]['length'][0,0]
		fin = modData[modelName][muscName]['length'][0,-1]       
		init_index, fin_index = checkROM(init,fin, modData[modelName][muscName]['length'])

		g2392MA = modData[modelName][muscName]['momentArm'][1,init_index:fin_index]
		# g2392Len = modData[modelName][muscName]['length'][1,init_index:fin_index]
		gMA_range = np.arange(int(init), int(fin), step = (int(fin)-int(init))/len(g2392MA))

		# gLenN = nNumDeriv(g2392Len, 6, 59)
		# gMaN = nNumDeriv(g2392MA, 5, 3)  

		# extract literature data
		litVals = loadCombLitValsHPC() # literature data

		litName = osim2Lit[muscName]
		targetLitVals = litVals[litName]['polyMeans'][0,0]

		init_Lit = targetLitVals[0,0]
		fin_Lit = targetLitVals[0,-1]
		init_index_Lit, fin_index_Lit = checkROM(init_Lit, fin_Lit, targetLitVals)

		litMA = targetLitVals[1,init_index_Lit:fin_index_Lit]    
		litMA_range = targetLitVals[0,init_index_Lit:fin_index_Lit]    

		return g2392MA, gMA_range, litMA, litMA_range

