from pylab import *

figure(figsize=(6,6))

a = loadtxt("photon_electron_output.txt")
E = logspace(16,23,71)
idx = a[:,1] == 22
photons = a[idx,2] * 1e18
idx = fabs(a[:,1]) == 11
ep = a[idx,2] * 1e18
data,bins = histogram(photons,E)
bincenter = (E[1:] -E[:-1])/2 + E[:-1]
plot(bincenter, data,label="photons")
data,bins = histogram(ep,E)
plot(bincenter, data, label="electrons / positrons")
grid()
loglog()
xlim(1e16, 1e21)
ylim(1e2, 1e4)
legend(loc="lower right")
xlabel("Energy [eV]")
ylabel("Number of Particles")
show()
