from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# CONFIG: choose condition here
# -----------------------------
# "control", "hypo", or "nicotine"
condition = "nicotine"

print(f"Running PFC microcircuit in condition: {condition}")

# -----------------------------
# Load basic NEURON stuff & templates
# -----------------------------
h.load_file("stdrun.hoc")
h.load_file("glu_neuron.hoc")   # your pyramidal cell template
# (we don't strictly need dopa/chol here, this is standalone PFC)

# -----------------------------
# Create cells
# -----------------------------
# Pyramidal neuron = your glutamatergic template
pyr = h.glutamatergic()

# Simple SOM interneuron (single compartment)
som = h.Section(name='som_cell')
som.L = som.diam = 20
som.Ra = 150
som.cm = 1
som.insert('hh3')  # if hh3.mod exists
# SOM somewhat fast-spiking: tweak if needed
try:
    som.gnabar_hh3 = 0.05
    som.gkhhbar_hh3 = 0.5
except:
    pass

# Simple VIP interneuron (single compartment)
vip = h.Section(name='vip_cell')
vip.L = vip.diam = 15
vip.Ra = 150
vip.cm = 1
vip.insert('hh3')
try:
    vip.gnabar_hh3 = 0.03
    vip.gkhhbar_hh3 = 0.3
except:
    pass

# -----------------------------
# Helper: make AMPA and GABA synapses
# -----------------------------
def make_ampa(sec, loc=0.5):
    syn = h.Exp2Syn(sec(loc))
    syn.tau1 = 0.5
    syn.tau2 = 3.0
    syn.e = 0.0
    return syn

def make_gaba(sec, loc=0.5):
    syn = h.Exp2Syn(sec(loc))
    syn.tau1 = 1.0
    syn.tau2 = 8.0
    syn.e = -70.0
    return syn

# -----------------------------
# External excitatory input to Pyr (thalamic / other cortical)
# -----------------------------
ext_stim = h.NetStim()
ext_stim.start = 200
ext_stim.interval = 50     # ms between inputs
ext_stim.number = 1e9
ext_stim.noise = 0.2

ext_ampa_pyr = make_ampa(pyr.soma, 0.5)
nc_ext_pyr = h.NetCon(ext_stim, ext_ampa_pyr)
nc_ext_pyr.delay = 1.0

if condition == "control":
    nc_ext_pyr.weight[0] = 0.0008
elif condition == "hypo":
    nc_ext_pyr.weight[0] = 0.00035  # weaker external drive → hypofrontality
else:  # nicotine
    nc_ext_pyr.weight[0] = 0.00035  # start from hypo-like input, rescue via nAChR

# -----------------------------
# PFC connectivity: Pyr, SOM, VIP
# -----------------------------
# Pyr -> SOM (excitatory)
ampa_pyr_som = make_ampa(som, 0.5)
nc_pyr_som = h.NetCon(pyr.soma(0.5)._ref_v, ampa_pyr_som)
nc_pyr_som.threshold = -20
nc_pyr_som.delay = 1.0
nc_pyr_som.weight[0] = 0.0006

# Pyr -> VIP (excitatory)
ampa_pyr_vip = make_ampa(vip, 0.5)
nc_pyr_vip = h.NetCon(pyr.soma(0.5)._ref_v, ampa_pyr_vip)
nc_pyr_vip.threshold = -20
nc_pyr_vip.delay = 1.0
nc_pyr_vip.weight[0] = 0.0004

# SOM -> Pyr (inhibitory)
gaba_som_pyr = make_gaba(pyr.soma, 0.5)
nc_som_pyr = h.NetCon(som(0.5)._ref_v, gaba_som_pyr)
nc_som_pyr.threshold = -20
nc_som_pyr.delay = 1.0
if condition == "hypo":
    nc_som_pyr.weight[0] = 0.0012   # stronger inhibition in hypofrontality
else:
    nc_som_pyr.weight[0] = 0.0008

# VIP -> SOM (inhibitory, disinhibition)
gaba_vip_som = make_gaba(som, 0.5)
nc_vip_som = h.NetCon(vip(0.5)._ref_v, gaba_vip_som)
nc_vip_som.threshold = -20
nc_vip_som.delay = 1.0
nc_vip_som.weight[0] = 0.0008

# -----------------------------
# Nicotinic receptors and ACh/nicotine pulse
# -----------------------------
ach = None
a7_vip = None
a4b2_pyr = None

if condition == "nicotine":
    # ACh / Nicotine pulse generator
    ach = h.AChPulse(0.5)
    # parameters inside AChPulse.mod: pulse_amp[], pulse_dur, pulse_isi, num_pulses, condition
    # we use condition = 1 (e.g. higher concentration)
    ach.condition = 1
    ach.pulse_dur = 20     # ms
    ach.pulse_isi = 200    # ms
    ach.num_pulses = 40

    # α7 on VIP interneuron
    a7_vip = h.a7()
    try:
        a7_vip.loc(vip(0.5))
    except:
        # if a7 is a POINT_PROCESS without loc(), instantiate at vip(0.5)
        a7_vip = h.a7(vip(0.5))
    h.setpointer(ach._ref_ACh_out, 'C_in', a7_vip)

    # α4β2 on Pyramidal soma
    a4b2_pyr = h.a4b2()
    try:
        a4b2_pyr.loc(pyr.soma(0.5))
    except:
        a4b2_pyr = h.a4b2(pyr.soma(0.5))
    h.setpointer(ach._ref_ACh_out, 'C_in', a4b2_pyr)

# -----------------------------
# Recording
# -----------------------------
t = h.Vector().record(h._ref_t)
v_pyr = h.Vector().record(pyr.soma(0.5)._ref_v)
v_som = h.Vector().record(som(0.5)._ref_v)
v_vip = h.Vector().record(vip(0.5)._ref_v)

# Spike detectors for Pyr
pyr_spikes = h.Vector()
nc_pyr_spike = h.NetCon(pyr.soma(0.5)._ref_v, None, sec=pyr.soma)
nc_pyr_spike.threshold = 0.0
nc_pyr_spike.record(pyr_spikes)

# -----------------------------
# Run simulation
# -----------------------------
h.tstop = 3000
h.dt = 0.025
h.v_init = -65
h.finitialize(h.v_init)
h.run()

# -----------------------------
# Analyze Pyr firing (rough Hz)
# -----------------------------
# ignore first 500 ms as transient
spike_times = np.array(pyr_spikes)
spike_times = spike_times[spike_times > 500.0]
sim_time_s = (h.tstop - 500.0) / 1000.0
if sim_time_s > 0:
    pyr_rate = len(spike_times) / sim_time_s
else:
    pyr_rate = 0.0

print(f"Pyramidal firing rate ({condition}): {pyr_rate:.2f} Hz")

# -----------------------------
# Plot
# -----------------------------
os.makedirs("PFC_plots", exist_ok=True)

tt = np.array(t)
vp = np.array(v_pyr)
vs = np.array(v_som)
vv = np.array(v_vip)

plt.figure(figsize=(10,6))
plt.plot(tt, vp, label='Pyr')
plt.plot(tt, vs, label='SOM', alpha=0.6)
plt.plot(tt, vv, label='VIP', alpha=0.6)
plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
plt.legend()
plt.title(f"PFC microcircuit: {condition}, Pyr firing {pyr_rate:.2f} Hz")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"PFC_plots/pfc_micro_{condition}.png", dpi=300)
plt.show()
