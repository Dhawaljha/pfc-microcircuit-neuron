from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np
import os

print("Running dopaminergic tonic firing simulation (smooth & stable)...")

# -------------------------------------------------------------
# Load model
# -------------------------------------------------------------
h.load_file("stdlib.hoc")
h.load_file("stdrun.hoc")
h.load_file("dopa_neuron.hoc")

cell = h.dopaminergic()

# -------------------------------------------------------------
# FINAL SMOOTH TONIC FIRING — Stable from start to end
# -------------------------------------------------------------
h.tstop = 4000
h.dt = 0.025
v_init = -65

# Longer pre-equilibration to stabilize intracellular Ca2+ and gating variables
h.finitialize(v_init)
h.continuerun(1000)  # let slow channels & pumps reach steady state

# Steady, low current injection
stim = h.IClamp(cell.soma(0.5))
stim.delay = 1000    # start only after full equilibration
stim.dur   = 3000
stim.amp   = 0.052   # mild depolarization → consistent tonic spikes

# Core conductance balance for stable tonic pattern
try:
    cell.soma.insert('hh3')
except Exception:
    pass

try:
    cell.soma.gbar_nattxr = 0.022   # moderate persistent Na
    cell.soma.gbar_nattxs = 0.07
except Exception:
    pass

try:
    cell.soma.gkhhbar_hh3 = 0.55    # balanced Kdr → smooth ISIs
except Exception:
    pass

try:
    cell.soma.gkcabar_kca = 6e-05   # SK/BK Ca-K coupling — not too strong
except Exception:
    pass

try:
    cell.soma.ghdbar_hd = 0.02      # mild Ih for depolarizing ramp
except Exception:
    pass

# Normalize calcium handling (no drift)
try:
    cell.soma.icapumpmax_capump = 0.05
except Exception:
    pass

# Gentle passive stabilizer
try:
    cell.soma.insert('pas')
    cell.soma.g_pas = 1e-5
    cell.soma.e_pas = -65
except Exception:
    pass

# Re-equilibrate
h.finitialize(v_init)
h.continuerun(500)
# -------------------------------------------------------------


cell.soma.insert('hh3')  # ensure hh3 is present

cell.soma.gbar_nattxr = 0.02    # slightly weaker persistent Na (smooth ramp)
cell.soma.gbar_nattxs = 0.07    # same transient Na
cell.soma.ghdbar_hd   = 0.03    # moderate Ih
cell.soma.gkcabar_kca = 8e-05   # balanced Ca-KAHP
cell.soma.gkhhbar_hh3 = 0.6     # a bit stronger delayed rectifier (smooth AHP)

try:
    cell.soma.gkcabar_skca = 1e-6  # if present, leave minimal
except AttributeError:
    pass

# Add tiny leak if not already present
try:
    cell.soma.el_hh3 = -65
except Exception:
    pass

# -------------------------------------------------------------
# Record voltage
# -------------------------------------------------------------
v_vec = h.Vector().record(cell.soma(0.5)._ref_v)
t_vec = h.Vector().record(h._ref_t)

# -------------------------------------------------------------
# Run simulation
# -------------------------------------------------------------
h.finitialize(h.v_init)
h.continuerun(h.tstop)

# -------------------------------------------------------------
# Analyze and save
# -------------------------------------------------------------
v = np.array(v_vec)
t = np.array(t_vec)

spikes = np.where((v[1:] >= 0) & (v[:-1] < 0))[0]
freq = len(spikes) / (h.tstop / 1000.0)

os.makedirs("Dopa_voltage_plots", exist_ok=True)
np.savetxt("Dopa_voltage_plots/tonic_dopa_voltage_smooth_final.txt", v, fmt="%.3f")

# -------------------------------------------------------------
# Plot result
# -------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(t, v, color="#b03030", lw=1.2)
plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
plt.title(f"Dopaminergic neuron — smooth tonic firing ({freq:.2f} Hz)")
plt.grid(True)
plt.tight_layout()
plt.savefig("Dopa_voltage_plots/tonic_dopa_voltage_smooth_final.png", dpi=300)
plt.show()

print(f"✅ Simulation complete — Firing rate ≈ {freq:.2f} Hz")