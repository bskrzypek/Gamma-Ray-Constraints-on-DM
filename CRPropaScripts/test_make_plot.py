import pylab as pl
from crpropa import *
# load events
d = pl.genfromtxt('events.txt', names=True)

# observed quantities
Z = pl.array([chargeNumber(int(id)) for id in d['ID'].astype(int)])  # element
A = pl.array([massNumber(int(id)) for id in d['ID'].astype(int)])  # atomic mass number
lE = pl.log10(d['E']) + 18  # energy in log10(E/eV))

lEbins = pl.arange(18, 20.51, 0.1)  # logarithmic bins
lEcens = (lEbins[1:] + lEbins[:-1]) / 2  # logarithmic bin centers
dE = 10**lEbins[1:] - 10**lEbins[:-1]  # bin widths

# identify mass groups
idx1 = A == 1
idx2 = (A > 1) * (A <= 7)
idx3 = (A > 7) * (A <= 28)
idx4 = (A > 28)

# calculate spectrum: J(E) = dN/dE
J  = pl.histogram(lE, bins=lEbins)[0] / dE
J1 = pl.histogram(lE[idx1], bins=lEbins)[0] / dE
J2 = pl.histogram(lE[idx2], bins=lEbins)[0] / dE
J3 = pl.histogram(lE[idx3], bins=lEbins)[0] / dE
J4 = pl.histogram(lE[idx4], bins=lEbins)[0] / dE

# normalize
J1 /= J[0]
J2 /= J[0]
J3 /= J[0]
J4 /= J[0]
J /= J[0]

pl.figure(figsize=(10,7))
pl.plot(lEcens, J,  color='SaddleBrown')
pl.plot(lEcens, J1, color='blue', label='A = 1')
pl.plot(lEcens, J2, color='grey', label='A = 2-7')
pl.plot(lEcens, J3, color='green', label='A = 8-28')
pl.plot(lEcens, J4, color='red', label='A $>$ 28')
pl.legend(fontsize=20, frameon=True)
pl.semilogy()
pl.ylim(1e-5)
pl.grid()
pl.ylabel('$J(E)$ [a.u.]')
pl.xlabel('$\log_{10}$(E/eV)')
pl.savefig('sim1D_spectrum.png')
