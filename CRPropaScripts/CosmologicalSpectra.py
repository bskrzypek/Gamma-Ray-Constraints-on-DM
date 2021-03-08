import numpy as np
import scipy as sp
import scipy.interpolate as interpolate
import scipy.integrate as integrate
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

from crpropa import *

def MakePhotons(gamma,distance, nsample = 1000, include_cmb = True, include_irb = True, inverseCompton = True):
    sim = ModuleList()
    sim.add(SimplePropagation())
    sim.add(Redshift())
    if(include_cmb):
        sim.add(EMPairProduction(CMB(),True))
        sim.add(EMDoublePairProduction(CMB(),True))
        sim.add(EMTripletPairProduction(CMB(),True))
        sim.add(EMInverseComptonScattering(CMB(),True))
    if(include_irb):
        sim.add(EMPairProduction(IRB_Dominguez11(),True))
        sim.add(EMDoublePairProduction(IRB_Dominguez11(),True))
        sim.add(EMTripletPairProduction(IRB_Dominguez11(),True))
        sim.add(EMInverseComptonScattering(IRB_Dominguez11(),True))
    #sim.add(EMPairProduction(URB_Protheroe96(),True))
    #sim.add(EMInverseComptonScattering(URB_Protheroe96(),True))
    sim.add(MinimumEnergy(10e1*GeV))
    obs = Observer() #add photon output 
    obs.add(ObserverPoint())
    obs.add(ObserverInactiveVeto())

    #output_filename = "photon_electron_output_cmb_{include_cmb}_irb_{include_irb}_StarFormation_1.txt".format(include_cmb=include_cmb,
                                                                                                                #include_irb=include_irb
 #                                                                                                              )           
    
    
    output_filename = "crpropa_photon_output_PowerLawCosmologicalEvolution_{gamma}_{distance}_{include_irb}_{inverseCompton}.txt".format(gamma=int(-gamma*10),distance = distance/Mpc,include_irb = include_irb, inverseCompton = inverseCompton)
                                                                                                                                   
                                                                                                        
    #with open(output_filename) as myfile:
    #    first_line = myfile.readline()
    #print(f"Output is {first_line}")
    #define the source(s)
    source = Source()
    #source.add(SourceUniformSphere(Vector3d(4, 0, 0) * Mpc,0.01*Mpc))
    source.add(SourceUniform1D(0.0001*Mpc,distance,True))
    #source.add(SourcePosition(Vector3d(distance,0,0)))
    #source.add(SourceIsotropicEmission())
    if(inverseCompton==False):
        source.add(SourceParticleType(22))
    if(inverseCompton==True):
        source.add(SourceParticleType(11))
        source.add(SourceParticleType(-11))
    source.add(SourcePowerLawSpectrum(10e1 * GeV, 10e7 * GeV, -1))
    #source.add(SourceRedshiftEvolution(1.5, 0.001, 1))
    #source.add(SourceRedshiftEvolution(3.4, 0.001, 1))
    #source.add(SourceRedshiftEvolution(-0.3, 1.001, 4))
    #source.add(SourceRedshift1D())
    
    obs = Observer() #add photon output 
    obs.add(ObserverPoint())
    obs.add(ObserverInactiveVeto())
    t = TextOutput(output_filename,Output.Event1D)
    #t.enable(Output.CreatedIdColumn)
    t.enable(Output.CreatedEnergyColumn)
    t.enable(Output.SourcePositionColumn)
    t.enable(Output.SourceEnergyColumn)
    t.enable(Output.CreatedPositionColumn)
    t.enable(Output.RedshiftColumn)
    t.enable(Output.CurrentPositionColumn)
    obs.onDetection(t)
    sim.add(obs) 
    sim.setShowProgress(True)
    sim.run(source,nsample,True)
    #return output_filename    

MakePhotons(-1,0.1*Mpc,include_cmb=True,include_irb=False,inverseCompton =False)
#MakePhotons(-1,include_cmb = True, include_irb = False)
#MakePhotons(4,-1,include_cmb=True, include_irb=False)
#MakePhotons(2,-1.5,include_cmb=True,include_irb=True)
#MakePhotons(2,-1.8,include_cmb=True,include_irb=True)
#MakePhotons(2,-2,include_cmb=True,include_irb=True)
#files_all = MakePhotons(2,-1.5,include_cmb=True,include_irb=False)
#files_all = MakePhotons(2,-1.8,include_cmb=True,include_irb=False)
#files_all = MakePhotons(2,-2,include_cmb=True,include_irb=False)
#files_cmb_only = MakePhotons(include_cmb=True,include_irb=False)  
