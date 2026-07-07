import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Parameters
h_dt = 0.025  # Sampling interval in ms, adjust as per your simulation
spike_threshold = -40 # mV threshold to mask spikes
window_ms = 10  # Exclude ±10 ms around spike to avoid spike influence in subthreshold

# Folder containing voltage vector files - edit path accordingly
data_folder = 'syn_vol_ach'
file_names = [
    'voltage_vector1.txt',
    'voltage_vector2.txt',
    'voltage_vector3.txt',
    'voltage_vector4.txt'
]

def load_and_mask_spikes(filepath):
    voltage = np.loadtxt(filepath)
    spike_indices = np.where(voltage > spike_threshold)[0]
    mask = np.zeros_like(voltage, dtype=bool)
    pad = int(window_ms / h_dt)
    for spike in spike_indices:
        start = max(0, spike - pad)
        end = min(len(voltage), spike + pad)
        mask[start:end] = True
    voltage[mask] = np.nan  # Mask spike regions
    return voltage

plt.figure(figsize=(12, 8))

for i, fname in enumerate(file_names, 1):
    filepath = os.path.join(data_folder, fname)
    voltage_sub = load_and_mask_spikes(filepath)
    # Remove nans for PSD calculation
    voltage_sub = voltage_sub[~np.isnan(voltage_sub)]
    
    fs = 1000 / h_dt  # Sampling frequency in Hz (convert from ms^-1)
    
    # Compute PSD using Welch's method
    f, Pxx = welch(voltage_sub, fs=fs, nperseg=2048)
    
    # Plot PSD in logarithmic scale
    plt.subplot(2, 2, i)
    plt.semilogy(f, Pxx)
    plt.title(f'PSD of Subthreshold Voltage - {fname}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density')
    plt.grid(True)

plt.tight_layout()
plt.savefig('PSD_Subthreshold_Analysis.png')
plt.show()
