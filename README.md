# PFC Microcircuit: Dopaminergic-Cholinergic-Glutamatergic NEURON Model

A NEURON (Python + HOC) simulation of prefrontal cortex circuitry, modeling the interaction between dopaminergic, cholinergic, and glutamatergic neurons, including nicotinic receptor dynamics (a4b2, a7). Built as a minor semester project.

## Overview

The model simulates three cell types and their interactions:

- **Dopaminergic neuron** (`dopa_neuron.hoc`) - tonic and burst firing dynamics, modulated by nicotinic receptors on its dendrites.
- **Cholinergic neuron** (`chol_neuron.hoc`) - provides acetylcholine input via axonal terminals.
- **Glutamatergic (pyramidal) neuron** (`glu_neuron.hoc`) - used standalone and as part of a simplified PFC microcircuit with an SOM interneuron (`pfc_microcircuit.py`).

Ion channel and synaptic mechanisms are implemented as NMODL (`.mod`) files, including nicotinic acetylcholine receptors (`a4b2_receptor.mod`, `a7.mod`), NMDA synapses (`nmda.mod`), calcium dynamics (`cadyn.mod`, `cachan.mod`, `capump.mod`), potassium/sodium channels (`kdr.mod`, `kca.mod`, `skca.mod`, `nattxr.mod`, `nattxs.mod`), and transmitter release (`release.mod`).

## Repository structure

```
├── *.mod                  # NMODL ion channel / synapse / receptor mechanisms
├── *.hoc                  # Cell templates (dopaminergic, cholinergic, glutamatergic)
├── driver.py               # Main simulation driver (dopa-cholinergic interaction sweep)
├── pfc_microcircuit.py     # Standalone PFC pyramidal + SOM interneuron circuit
├── test_glu.py              # Sanity test for the glutamatergic cell template
├── tonic_dopa.py            # Dopaminergic tonic firing simulation
├── subthreshold.py          # Subthreshold voltage analysis around spikes
├── PSD.py                   # Power spectral density analysis of subthreshold voltage
└── testDriver.hoc           # HOC-based test driver
```

## Requirements

- [NEURON](https://www.neuron.yale.edu/neuron/) (with Python support)
- Python 3, numpy, matplotlib, pandas, scipy

## Running

Compile the mechanisms first:

```bash
nrnivmodl
```

Then run any of the simulation scripts, e.g.:

```bash
python driver.py
python pfc_microcircuit.py
```

## Notes

Compiled mechanism binaries (`arm64/`, `x86_64/`, etc.) are build artifacts and are not tracked in this repository - regenerate them locally with `nrnivmodl`.
