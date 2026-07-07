from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import os

h.load_file("stdlib.hoc")
h.load_file("nrngui.hoc")
h.load_file("stdrun.hoc")
h.load_file("dopa_neuron.hoc")
h.load_file("chol_neuron.hoc")

dopa = h.dopaminergic()
chol = h.cholinergic()

num_dopa_dend = 16
num_chol_axon = 7

# Setting simulation parameters
h.tstop = 2000
h.dt = 0.025
v_init = -65

rec_names = ["a4b2_dopa", "a7_dopa"]

num_rec1s = [0, 116]
num_rec2s = [0, 127]

num_rec = [num_rec1s, num_rec2s]
num_rec_comb = list(itertools.product(*num_rec))

plot_folder = 'Dopa_voltage_plots'
os.makedirs(plot_folder, exist_ok=True)

vol_folder = 'syn_vol_ach'
os.makedirs(vol_folder, exist_ok=True)

simulation = 1
start_simulation = 1

recep = [None] * 2000
# Combine the two lists of combinations and test each nicotine condition
# Combine the two lists of combinations
for num_recs in num_rec_comb:
    if simulation >= start_simulation:
        num_rec1 = num_recs[0]
        num_rec2 = num_recs[1]

        for i in range(0, num_dopa_dend):
            for j in range(0, num_rec1):
                recep[j] = h.a4b2()
                recep[j].loc(dopa.dend[i](0.5))
                h.setpointer(chol.axon[0](0.9)._ref_T_rel, 'C_in', recep[j])

            for j in range(0, num_rec2):
                recep[j] = h.a7()
                recep[j].loc(dopa.dend[i](0.5))
                h.setpointer(chol.axon[0](0.9)._ref_T_rel, 'C_in', recep[j])
            
                
        for i in range(0, num_rec1):
            recep[i] = h.a4b2()
            recep[i].loc(dopa.soma(0.5))
            h.setpointer(chol.axon[0](0.9)._ref_T_rel, 'C_in', recep[i])

            
        for i in range(0, num_rec2):
            recep[i] = h.a7()
            recep[i].loc(dopa.soma(0.5))
            h.setpointer(chol.axon[0](0.9)._ref_T_rel, 'C_in', recep[i])
                               
      
            
        print(f"Simulation is: {simulation} with {num_recs}")
            
        voltage_vec = h.Vector().record(dopa.soma(0.5)._ref_v)
        t_vec = h.Vector().record(h._ref_t)

        g = h.Graph()
        g.size(0, h.tstop, -80, 40)
        g.addvar("Dopa Vm", dopa.soma(0.5)._ref_v)
        
        h.finitialize(v_init)
        while h.t < h.tstop:
            h.fadvance()
            h.doNotify()
        
        vol_points = [round(voltage_vec.x[i], 0) for i in range(len(voltage_vec))]

        # Define the file name
        file_name = f'{vol_folder}/voltage_vector{simulation}.txt'

        # Save the voltage vector to a .txt file
        with open(file_name, 'w') as file:
            for voltage in vol_points:
                file.write(f"{voltage}\n") 
			
        # Plot and save the voltage graph
        plt.figure(figsize=(10, 6))
        plt.plot(voltage_vec, label='Voltage Trace')
        plt.xlabel('Time (ms)')
        plt.ylabel('Dopa voltage (mV)')
        plt.title(f"Dopa voltage at Simulation {simulation}")
        plt.legend()
        plt.grid(True)
        file_name = f'{plot_folder}/Dopa voltage at simulation{simulation}.jpg'
        plt.savefig(file_name)
        plt.clf()          

    simulation += 1

