import os
import numpy as np
import matplotlib.pyplot as plt

# Folder containing your voltage files
data_folder = 'syn_vol_ach'  # Update to your folder name
file_names = [f for f in os.listdir(data_folder) if f.endswith('.csv') or f.endswith('.txt') or f.endswith('.npy')]
file_names = sorted(file_names)[:4]  # Analyze only first four files

h_dt = 0.025  # Use your h.dt value in ms
spike_threshold = -40  # mV, adjust if needed
window_ms = 10  # ms window around spike

for idx, fname in enumerate(file_names, 1):
    # Load the voltage vector (adjust for your file format)
    full_path = os.path.join(data_folder, fname)
    if fname.endswith('.csv'):
        voltage = np.loadtxt(full_path, delimiter=',')
    elif fname.endswith('.txt'):
        voltage = np.loadtxt(full_path)
    elif fname.endswith('.npy'):
        voltage = np.load(full_path)
    else:
        continue

    times = np.arange(len(voltage)) * h_dt

    spike_indices = np.where(voltage > spike_threshold)[0]
    mask = np.zeros_like(voltage, dtype=bool)
    pad = int(window_ms / h_dt)
    for si in spike_indices:
        mask[max(0, si - pad):min(len(voltage), si + pad)] = True
    voltage_sub = voltage.copy()
    voltage_sub[mask] = np.nan

    mean_sub = np.nanmean(voltage_sub)
    std_sub = np.nanstd(voltage_sub)
    print(f"File: {fname} - Subthreshold mean: {mean_sub:.2f} mV, std: {std_sub:.2f} mV")

    # Plot each analysis
    plt.figure(figsize=(10,6))
    plt.plot(times, voltage, label='Raw Voltage')
    plt.plot(times, voltage_sub, label='Subthreshold', color='orange')
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title(f'Subthreshold Analysis - File {fname}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{data_folder}/Subthreshold_{os.path.splitext(fname)[0]}.jpg')
    plt.close()
