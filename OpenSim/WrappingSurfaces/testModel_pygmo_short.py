import WS_objectives as objfun
import numpy as np
import matplotlib.pyplot as plt
import pygmo as pg
import opensim as osim 
import time
import mtuInfo_os4

osim2Lit = {'glmed3_r' : 'litGMed3' , 'quad_fem_r' : 'litQF' , 'piri_r' : 'litPIRI','obt_externus_r' : 'litOE', 'obt_internus1_r' : 'litOI', 'gemelli_sup_r' : 'litOI', 'gemelli_inf_r' : 'litOI', 
    'addmagDist_r':'litADDMAG', 'addmagIsch_r': 'litADDMAG','addmagProx_r': 'litADDMAG'} 
Wrap2opt = {'piri_r':['PIRI_at_Ischium3_r'], 'obt_internus1_r': ['pelvisOITorus1_r'], 'gemelli_sup_r':['GEMsup_at_Ischium_r'], 'obt_externus_r':['OE_at_Ischium_r']} # surfaces that you want to optimise (only if you don't want to optimise all)

Optim_Thresholds = {'GLUTMED3_at_Ischium_r':[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 10, 0.7, 1.5],
	'PIRI_at_Ischium3_r':[0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 20, 0.7, 1.5],
	'GLUTMED3_at_femshaft_r':[0.05, 0.05, 0.05, 0.05, 0.01, 0.01, 10, 0.7, 1.5], 
	'pelvisOITorus1_r':[0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 10, 0.01, 0.06, 0.001, 0.005, 0.001],
    'OE_at_Ischium_r':[0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 20, 0.7, 1.5],
    'GEMsup_at_Ischium_r': [0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 20, 0.7, 1.5]}
	#'femHeadOISphere_r':[0.001,0.001,0.001,0.001,0.001,0.001,0,01]} #'OI_at_Ischium':[0.01,0.01,0.01,0.01,0.01,0.01,5,1,1.2]

global_gModel, global_InitState = objfun.getInfo() 

class my_problem ():
    "multi objective problem to optimise position/size WS"

    def __init__(self, dim, muscName, dof):
        self.dim = dim
        self.muscName = muscName
        self.dof = dof

        gMA, gMA_range, litMA, litMA_range = objfun.getNderivGenModel(self.muscName, self.dof, osim2Lit)
        
        litMAx4 = np.concatenate((np.gradient(litMA), np.flip(np.gradient(litMA)),np.gradient(litMA), np.flip(np.gradient(litMA))))
        gMAx4 = np.concatenate((np.gradient(gMA), np.flip(np.gradient(gMA)),np.gradient(gMA), np.flip(np.gradient(gMA))))

        litMAsmooth, litPhase = objfun.calcArcLengthFFTem(np.gradient(litMAx4)) 
        gMAsmooth, gPhase = objfun.calcArcLengthFFTem(np.gradient(gMAx4)) 

        self.litMA = litMA
        self.litMA_range = litMA_range        
        self.litSmooth = litMAsmooth
        self.litPhase = litPhase
        self.gMA = gMA
        self.gMA_range = gMA_range
        self.gSmooth = gMAsmooth
        self.gPhase = gPhase

    def get_nobj(self):
        return 5

    def fitness(self, vals):
        # change wrapping surfaces
        muscName = self.muscName
        gModel = osim.Model('./OpenSim/WrappingSurfaces/Raja_FAI.osim')
        gModel.initSystem()
        wrapDict = mtuInfo_os4.getMuscWrapObjectInfo(gModel, muscName)
        updModel = objfun.editMuscWraps(vals, gModel, muscName, wrapDict, Wrap2opt) 
        updState = updModel.initSystem()

        # updState = updModel.getWorkingState()

		# # get new model information: mtulenght, ma. 
        muscLen, optMA, optMA_litrange, _ = objfun.getModelInformation(updModel, updState, self.dof, muscName, self.litMA_range)

        ## similarity MA model and literature
        corrMA = objfun.norcorr(np.gradient(self.litMA), np.gradient(optMA_litrange))
        OPTcorrMA = 1-corrMA #corrMA = 1 if signals identical & -1 if signals not at all similar

		## check moment arm model/lit have same sign 
        pol = objfun.Polarity(self.litMA, optMA_litrange)
		
        ## smootheness
        optMAx4 = np.concatenate((np.gradient(optMA), np.flip(np.gradient(optMA)), np.gradient(optMA), np.flip(np.gradient(optMA)))) # create periodic signal to improve fft (move multiple times through ROM)
        MAsmooth, _ = objfun.calcArcLengthFFTem(np.gradient(optMAx4)) 
        # rel2Lit_smooth = MAsmooth/self.litSmooth 
        rel2g_smooth = MAsmooth/self.gSmooth 

		## wrap too far from bone? - exponential penalty
        # penWrap2Mesh = objfun.penDistanceWrapMesh(updModel, updState, muscName, Wrap2opt) 

		## muscle path through bone? - exponential penalty
        penMuscInMesh = objfun.checkPenetrationUpd(updModel, updState, muscName) 
        # # del gModel, updModel, updState 
        return [OPTcorrMA, pol, rel2g_smooth, penMuscInMesh, np.max(muscLen)] #, ,  , 

    def get_bounds(self):
        # get boundaries ws
        lb, ub = objfun.getBoundaries(global_gModel, self.muscName, Optim_Thresholds, Wrap2opt)
		
        return (lb,ub)

def choose_best_solution(fnds, pop):
    # order of objective functions: corr, pol, smooth, inmesh, outmesh 
    ndf1 = fnds[0][0] # first non-dominating front
    f_opt = pop.get_f()[ndf1] 
    # make sure not too far from mesh or too far in mesh - assuming that there are low values found 
    # i1 = np.where(f_opt[:, 4] <= 10) # np.median(f_opt[:, 4])) #np.median(f_opt[:, 4])
    i2 = np.where(f_opt[:, 3] <= 1)
    i3 = np.where(f_opt[:, 2] <= 1.1) # as smooth as generic model
    unique,counts = np.unique(np.concatenate((i2[0],i3[0])), return_counts=True)
    i = []
    for n in range(0,len(counts)):
        if counts[n] == 2:
            i.append(unique[n])

    i_best =  i[np.where(f_opt[i,1] == np.min(f_opt[i,1]))[0][0]]
    for ii in i:
        if f_opt[ii, 0] < f_opt[i_best, 0]:
            if f_opt[ii, 1] <= f_opt[i_best, 1]:
                i_best = ii

    return pop.get_x()[ndf1[i_best]], pop.get_f()[ndf1[i_best]]

def randomvals(lb, ub):
    valsrand = []
    for x in range(0,len(lb)):
        valsrand.append(np.random.uniform(low = lb[x], high = ub[x]))

    return valsrand

# lb = [-0.17470000000000002, -0.1028, 0.017699999999999994, 0.022, -1.224532925199433, 0.36546707480056706]
# ub = [0.025300000000000003, -0.002799999999999997, 0.1177, 0.033, -0.8754670748005671, 0.714532925199433]

# for i in range(0, 1000):
#     vals = randomvals(lb,ub)
#     prob = my_problem(1, muscName = 'piri_r', dof = 'hip_flexion_r')
#     x = prob.fitness(vals)
#     print(vals)

# testModel = osim.Model('Raja_FAI_opt.osim')
# testState = testModel.initSystem()

# objfun.checkPenetrationUpd(testModel, testState, 'piri_r')
# # optimise WS
# muscNames = {'piri_r'} #, 'glmed3_r', 'piri_r'}

# vals_opt = {musc:[] for musc in muscNames}
# f_opt = {musc:[] for musc in muscNames}

# for musc in muscNames:
# 	dof = 'hip_flexion_r'
# 	t = time.time()
# 	prob = pg.problem(my_problem(1, muscName = musc, dof = dof))

# 	print(prob)
# 	# algo = pg.algorithm(pg.nsga2(gen=100))  
# 	algo = pg.algorithm(pg.nspso(gen=100))  

# 	algo.set_verbosity(2)

# 	pop = pg.population(prob, 300)
# 	# use of island archipelago - parallelisation

# 	pop = algo.evolve(pop)
# 	uda = algo.extract(pg.nspso)
# 	log = uda.get_log()

# 	plt.figure()
# 	fnds = pg.fast_non_dominated_sorting(pop.get_f())	

# 	vals_opt[musc],f_opt[musc] = choose_best_solution(fnds, pop) #choose one of the solution on pareto front !! need to find a good way to choose 'best' solution.
# 	# vals_opt[musc] = pop.get_x()[fnds[0][0][0]]

# ## update model
# model, state = objfun.getInfo() 

# for musc1 in muscNames:
# 	wrapDict = mtuInfo_os4.getMuscWrapObjectInfo(model, musc1)
# 	model  = objfun.editMuscWraps(vals_opt[musc1], model, musc1, wrapDict, Wrap2opt)

# # save model
# model.printToXML('Raja_FAI_opt.osim')
# model3 = osim.Model('Raja_FAI.osim')

# # plot moment arm literature, generic model and optimised model.
# for musc2 in muscNames:
# 	gMa, gMA_range, litMA, litMA_range = objfun.getNderivGenModel(musc2, 'hip_flexion_r', osim2Lit)
# 	len_optmodel,_,MA_optmodel, radRange = objfun.getModelInformation(model, state, dof, musc2, litMA_range)
# 	len_osimmodel,_,MA_osimmodel, _ = objfun.getModelInformation(model3, model3.initSystem(), dof, musc2, litMA_range)
# 	plt.figure()
# 	plt.subplot(2,1,1)
# 	plt.plot(MA_optmodel)
# 	plt.plot(MA_osimmodel)
# 	plt.plot(litMA)
# 	plt.legend(('model_opt','osim','lit'))
# 	plt.ylabel('moment arm[m]')
# 	plt.subplot(2,1,2)
# 	plt.plot(radRange, len_optmodel)
# 	plt.plot(radRange, len_osimmodel)
# 	plt.ylabel('mtu length[m]')
# 	plt.xlabel(dof)
# 	plt.legend(('model_opt','osim'))

# 	plt.suptitle(musc2)
# 	plt.savefig('./plots/' + musc2 + '.png')
# 	## o_functions
# 	print('inmesh? opt: ' + str(objfun.penDistanceWrapMesh(model, state, musc2, Wrap2opt) ))
# 	print('inmesh? gen: ' + str(objfun.penDistanceWrapMesh(model3, model3.initSystem(), musc2, Wrap2opt) ))

# 	print(objfun.calcArcLengthFFTem(MA_optmodel))
# 	print(objfun.calcArcLengthFFTem(MA_osimmodel))
	
# plt.show()


# ## test
# # smootheness
# problem1 = my_problem(1, 'piri_r','hip_flexion_r')
# print(problem1.fitness(vals_opt[musc]))
# print(problem1.fitness(vals_opt[musc]))
# print(problem1.fitness(vals_opt[musc]))
# print(f_opt[musc])

# gMA = problem1.gMA 
# gSmooth = problem1.gSmooth
# gPhase = problem1.gPhase
# anglesMAg = problem1.gMA_range
# anglesMAlit = problem1.litMA_range
# plt.plot(anglesMAg,gMA)
# litMA = problem1.litMA
# litSmooth = problem1.litSmooth
# litPhase = problem1.litPhase
# plt.plot(anglesMAlit, litMA)

# # perturb ma
# pertMA = problem1.gMA
# rnd = np.random.randint(10, high = len(pertMA)-10, size = 1, dtype = int)
# pertMA[rnd] = 0
# pertMAx4 = np.concatenate((np.gradient(MA_optmodel), np.flip(np.gradient(MA_optmodel)), np.gradient(MA_optmodel), np.flip(np.gradient(MA_optmodel)))) # create periodic signal to improve fft (move multiple times through ROM)
# pertMAsmooth, pertPhase = objfun.calcArcLengthFFTem(np.gradient(pertMAx4)) 

# rel2g_smooth = pertMAsmooth /gSmooth - 1
# rel2lit_smooth = pertMAsmooth /litSmooth - 1

# # gradient or phase
# #phase
# rel2g_phase = (gPhase - pertPhase) /np.pi
# rel2lit_phase = (litPhase - pertPhase) /np.pi
# #gradient
# corrMA = objfun.norcorr(np.gradient(litMA), np.gradient(anglesMAg))

# plt.plot(anglesMAg, pertMA)
# plt.legend(('generic model','literature','generic model + perturbation'))
# plt.xlabel('hip flexion')
# plt.ylabel('moment arm [m]')
# print(('{0:.2f}'.format(rel2g_smooth), '{0:.2f}'.format(rel2lit_smooth)))
# plt.show()