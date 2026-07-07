from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np

# Load mechanisms and your glutamatergic template
h.load_file("stdrun.hoc")
h.load_file("glu_neuron.hoc")   # <- file name on disk
# Template name inside is: begintemplate glutamatergic

cell = h.glutamatergic()

# Simple somatic current injection
stim = h.IClamp(cell.soma(0.5))
stim.delay = 100    # ms
stim.dur = 500      # ms
stim.amp = 0.1      # nA (tweak later if needed)

# Record
t = h.Vector().record(h._ref_t)
v = h.Vector().record(cell.soma(0.5)._ref_v)

h.tstop = 800
h.dt = 0.025
h.v_init = -65

print("Running GLU test simulation...")
h.finitialize(h.v_init)
h.run()

tt = np.array(t)
vv = np.array(v)

plt.figure(figsize=(8,5))
plt.plot(tt, vv)
plt.xlabel("Time (ms)")
plt.ylabel("V_soma (mV)")
plt.title("Glutamatergic cell – IClamp test")
plt.grid(True)
plt.tight_layout()
plt.show()