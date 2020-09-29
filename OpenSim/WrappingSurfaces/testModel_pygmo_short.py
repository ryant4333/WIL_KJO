import WS_objectives as objfun
import numpy as np
import matplotlib.pyplot as plt
import pygmo as pg
import opensim as osim 
import time
from myMods.muscleWrappings import mtuInfo_os4

osim2Lit = {'glmed3_r' : 'litGMed3' , 'quad_fem_r' : 'litQF' , 'piri_r' : 'litPIRI', 'obt_internus1_r' : 'litOI'} 
Wrap2opt = {'piri_r':['PIRI_at_Ischium3_r'], 'obt_internus1_r': ['pelvisOITorus1_r']} # surfaces that you want to optimise (only if you don't want to optimise all)

Optim_Thresholds = {'GLUTMED3_at_Ischium_r':[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 10, 0.7, 1.5],
	'PIRI_at_Ischium3_r':[0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 10, 1, 1.5],
	'GLUTMED3_at_femshaft_r':[0.05, 0.05, 0.05, 0.05, 0.01, 0.01, 10, 0.7, 1.5], 
	'pelvisOITorus1_r':[0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 10, 0.01, 0.06, 0.001, 0.005, 0.001]}
	#'femHeadOISphere_r':[0.001,0.001,0.001,0.001,0.001,0.001,0,01]} #'OI_at_Ischium':[0.01,0.01,0.01,0.01,0.01,0.01,5,1,1.2]

global_gModel, global_InitState = objfun.getInfo() 

class my_problem ():
    "multi objective problem to optimise position/size WS"

    def __init__(self, dim, muscName, dof):
        self.dim = dim
        self.muscName = muscName
        self.dof = dof

        gLenN, gMaN, litMA, litMA_range = objfun.getNderivGenModel(self.muscName, self.dof, osim2Lit)
        litMAx4 = np.concatenate((np.gradient(litMA), np.flip(np.gradient(litMA)),np.gradient(litMA), np.flip(np.gradient(litMA))))

        litMAsmooth = objfun.calcArcLengthFFTem(np.gradient(litMAx4)) 

        self.gMaN = gMaN
        self.gLenN = gLenN
        self.litMA = litMA
        self.litMA_range = litMA_range        
        self.litSmooth = litMAsmooth

    def get_nobj(self):
        return 2

    def fitness(self, vals):
        # change wrapping surfaces
        muscName = self.muscName
        gModel = osim.Model(global_gModel)
        InitState = osim.State(global_InitState)
        wrapDict = mtuInfo_os4.getMuscWrapObjectInfo(gModel, muscName, InitState)
        updModel, updState = objfun.editMuscWraps(vals, gModel, muscName, wrapDict, Wrap2opt)

		# get new model information: mtulenght, ma. 
        _, optMA, optMA_litrange, _ = objfun.getModelInformation(updModel, updState, self.dof, muscName, self.litMA_range)

        ## similarity MA model and literature
        corrMA = objfun.norcorr(np.gradient(self.litMA), np.gradient(optMA_litrange))
        OPTcorrMA = 1-corrMA #corrMA = 1 if signals identical & -1 if signals not at all similar

		## check moment arm model/lit have same sign 
        pol = objfun.Polarity(self.litMA, optMA_litrange)
		
        optMAx4 = np.concatenate((np.gradient(optMA), np.flip(np.gradient(optMA)), np.gradient(optMA), np.flip(np.gradient(optMA)))) # create periodic signal to improve fft (move multiple times through ROM)
        MAsmooth, _ = objfun.calcArcLengthFFTem(np.gradient(optMAx4)) 

		## wrap too far from bone? - exponential penalty
        penWrap2Mesh = objfun.penDistanceWrapMesh(updModel, updState, muscName, Wrap2opt) 
        
		## muscle path through bone? - exponential penalty
        penMuscInMesh = objfun.checkPenetrationUpd(updModel, updState, muscName) 

        return [OPTcorrMA, pol, MAsmooth, penMuscInMesh, penWrap2Mesh] 

    def get_bounds(self):
        # get boundaries ws
        lb, ub = objfun.getBoundaries(global_gModel, self.muscName, global_InitState, Optim_Thresholds, Wrap2opt)
		
        return (lb,ub)


d1 = objfun.penDistanceWrapMesh(global_gModel, global_InitState, 'piri_r', Wrap2opt)
model2 = osim.Model('Raja_FAI_opt.osim')
d2 = objfun.penDistanceWrapMesh(model2, model2.initSystem(), 'piri_r',Wrap2opt)

# optimise WS
muscNames ={'piri_r'} #, 'glmed3_r', 'piri_r'}

vals_opt = {musc:[] for musc in muscNames}
time_opt = {musc:[] for musc in muscNames}

for musc in muscNames:
	dof = 'hip_flexion_r'
	t = time.time()
	prob = pg.problem(my_problem(1, muscName = musc, dof = dof))

	print(prob)
	# algo = pg.algorithm(pg.nsga2(gen=100))  
	algo = pg.algorithm(pg.nspso(gen=10))  

	algo.set_verbosity(2)

	pop = pg.population(prob, 80)
	# use of island archipelago - parallelisation

	pop = algo.evolve(pop)
	uda = algo.extract(pg.nspso)
	log = uda.get_log()

	plt.figure()
	fnds = pg.fast_non_dominated_sorting(pop.get_f())	

	vals_opt[musc]= pop.get_x()[fnds[0][0]][0] #choose one of the solution on pareto front !! need to find a good way to choose 'best' solution.

## update model
model, state = objfun.getInfo() 

for musc1 in muscNames:
	wrapDict = mtuInfo_os4.getMuscWrapObjectInfo(model, musc1, state)
	model, updstate = objfun.editMuscWraps(vals_opt[musc1], model, musc1, wrapDict, Wrap2opt)

# save model
model.printToXML('Raja_FAI_opt.osim')
model3 = osim.Model('Raja_FAI.osim')

# plot moment arm literature, generic model and optimised model.
for musc2 in muscNames:
	gLenN, gMaN, litMA, litMA_range = objfun.getNderivGenModel(musc2, 'hip_flexion_r', osim2Lit)
	len_optmodel,_, MA_optmodel, radRange = objfun.getModelInformation(model, state, dof, musc2, litMA_range)
	len_osimmodel,_, MA_osimmodel, _ = objfun.getModelInformation(model3, model3.initSystem(), dof, musc2, litMA_range)
	plt.figure()
	plt.subplot(2,1,1)
	plt.plot(MA_optmodel)
	plt.plot(MA_osimmodel)
	plt.plot(litMA)
	plt.legend(('model_opt','osim','lit'))
	plt.ylabel('moment arm[m]')
	plt.subplot(2,1,2)
	plt.plot(radRange, len_optmodel)
	plt.plot(radRange, len_osimmodel)
	plt.ylabel('mtu length[m]')
	plt.xlabel(dof)
	plt.legend(('model_opt','osim'))

	plt.suptitle(musc2)
	plt.savefig('./plots/' + musc2 + '.png')
	## o_functions
	print('inmesh? opt: ' + str(objfun.penDistanceWrapMesh(model, state, musc2, Wrap2opt) ))
	print('inmesh? gen: ' + str(objfun.penDistanceWrapMesh(model3, model3.initSystem(), musc2, Wrap2opt) ))

	print(objfun.calcArcLengthFFTem(MA_optmodel))
	print(objfun.calcArcLengthFFTem(MA_osimmodel))
	
plt.show()


