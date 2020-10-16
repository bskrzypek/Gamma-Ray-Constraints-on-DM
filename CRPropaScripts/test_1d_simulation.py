from crpropa import *

# simulation setup
sim = ModuleList()
sim.add( SimplePropagation(1*kpc, 10*Mpc) )
sim.add( Redshift() )
sim.add( PhotoPionProduction(CMB()) )
sim.add( PhotoPionProduction(IRB_Gilmore12()) )
sim.add( PhotoDisintegration(CMB()) )
sim.add( PhotoDisintegration(IRB_Gilmore12()) )
sim.add( NuclearDecay() )
sim.add( ElectronPairProduction(CMB()) )
sim.add( ElectronPairProduction(IRB_Gilmore12()) )
sim.add( MinimumEnergy( 1 * EeV) )

# observer and output
obs = Observer()
obs.add( ObserverPoint() )
output = TextOutput('events.txt', Output.Event1D)
obs.onDetection( output )
sim.add( obs )

# source
source = Source()
source.add( SourceUniform1D(1 * Mpc, 1000 * Mpc) )
source.add( SourceRedshift1D() )

# power law spectrum with charge dependent maximum energy Z*100 EeV
# elements: H, He, N, Fe with equal abundances at constant energy per nucleon
composition = SourceComposition(1 * EeV, 100 * EeV, -1)
composition.add(1,  1,  1)  # H
composition.add(4,  2,  1)  # He-4
composition.add(14, 7,  1)  # N-14
composition.add(56, 26, 1)  # Fe-56
source.add( composition )

# run simulation
sim.setShowProgress(True)
sim.run(source, 20000, True)
