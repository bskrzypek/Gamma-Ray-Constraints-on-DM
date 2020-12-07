import numpy as np
import scipy as sp
import scipy.interpolate as interpolate
import scipy.integrate as integrate
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

from crpropa import *

def MakePhotons(nsample = 100, include_cmb = True, include_irb = True):
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
    sim.add(MinimumEnergy(100*GeV))
    obs = Observer()
    obs.add(ObserverPoint())
    obs.add(ObserverInactiveVeto())

    output_filename = "photon_electron_output_cmb_{include_cmb}_irb_{include_irb}_StarFormation_1.txt".format(include_cmb=include_cmb,
                                                                                                                include_irb=include_irb
                                                                                                               )
    t = TextOutput(output_filename,Output.Event1D)
    obs.onDetection(t)
    sim.add(obs)
    #define the source(s)
    #here, the source is located 2 Mpc away from the observer along the x-axis and emission from the source follows a power law spectrum with a redshift evolution
    # m = 3.4 for 0.001 < z < 1 and -0.3 for 1.001 < z < 4
    source = Source()
    source.add(SourceUniformSphere(Vector3d(2, 0, 0) * Mpc,0*Mpc))
    source.add(SourceIsotropicEmission())
    source.add(SourceParticleType(22))
    source.add(SourcePowerLawSpectrum(1e3 * GeV, 1e5 * GeV, -1))
    source.add(SourceRedshiftEvolution(3.4, 0.001, 1))
    source.add(SourceRedshiftEvolution(-0.3, 1.001, 4))
    source.add(SourceRedshift1D())
    sim.setShowProgress(True)
    sim.run(source,nsample,True)
    return output_filename    

files_all = MakePhotons(include_cmb=True,include_irb=True)
#files_cmb_only = MakePhotons(include_cmb=True,include_irb=False)  
