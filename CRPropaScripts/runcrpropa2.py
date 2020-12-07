import numpy as np
import scipy as sp
import scipy.interpolate as interpolate
import scipy.integrate as integrate
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

from crpropa import *

def MakePhotons(nsample = 1000, distance*Mpc, gamma, include_cmb = True, include_irb = True):
    sim = ModuleList()
    #sim.add(SimplePropagation())
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
    sim.add(MinimumEnergy(1e4*GeV))
    obs = Observer()
    obs.add(ObserverPoint())
    obs.add(ObserverInactiveVeto())

    #output_filename = "photon_electron_output_cmb_{include_cmb}_irb_{include_irb}_StarFormation_1.txt".format(include_cmb=include_cmb,
                                                                                                                #include_irb=include_irb
 #                                                                                                              )           
    
    
    output_filename = "photon_electron_output_cmb_{include_cmb}_irb_{include_irb}_PowerLaw_{gamma}.txt".format(include_cmb=include_cmb,
                                                                                                                include_irb=include_irb, gamma=gamma
                                                                                                               ) 
    t = TextOutput(output_filename,Output.Event1D)
    obs.onDetection(t)
    sim.add(obs)
    #define the source(s)
    source = Source()
    #source.add(SourceUniformSphere(Vector3d(4, 0, 0) * Mpc,0.01*Mpc))
    source.add(SourcePosition(Vector3d(distance,0,0)))
    source.add(SourceIsotropicEmission())
    source.add(SourceParticleType(22))
    source.add(SourcePowerLawSpectrum(1e4 * GeV, 1e6 * GeV, gamma))
    #source.add(SourceRedshiftEvolution(3.4, 0.001, 1))
    #source.add(SourceRedshiftEvolution(-0.3, 1.001, 4))
    source.add(SourceRedshift1D())
    sim.setShowProgress(True)
    sim.run(source,nsample,True)
    return output_filename    

files_all = MakePhotons(2,-1,include_cmb=True,include_irb=True)
#files_cmb_only = MakePhotons(include_cmb=True,include_irb=False)  