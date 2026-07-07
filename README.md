# Nicotinic Modulation of a Dopaminergic Neuron — NEURON Model

A NEURON (Python + HOC) model of how nicotinic acetylcholine receptor
(α7, α4β2) activity shapes the excitability of a reconstructed
dopaminergic neuron, with exploratory extensions toward a small cortical
microcircuit. Built as an M.Sc. minor project (IIT Delhi).

## Core model
- **Dopaminergic neuron** (`dopa_neuron.hoc`) — biophysically detailed,
  reconstructed-morphology dopaminergic neuron (16 dendritic sections)
  carrying α7 and α4β2 nicotinic receptors (`a7.mod`, `a4b2_receptor.mod`)
  on its dendrites; reproduces tonic and burst firing. Receptor densities
  were guided by single-cell RNA-seq data.
- **Driver & analysis** — `driver.py` sweeps α4β2/α7 receptor counts on the
  dopaminergic cell under cholinergic drive; `subthreshold.py` and `PSD.py`
  quantify how receptor density alters subthreshold voltage dynamics and
  their power spectrum; `tonic_dopa.py` runs tonic-firing simulations.

## Exploratory extensions (work in progress)
Built around the core model to probe circuit context:
- **Cholinergic neuron** (`chol_neuron.hoc`) — acetylcholine source via an
  ACh-pulse / release mechanism (`ACh_pulse.mod`, `release.mod`).
- **Cortical microcircuit** (`glu_neuron.hoc`, `pfc_microcircuit.py`) —
  a glutamatergic pyramidal cell with SOM- and VIP-interneuron motifs
  (VIP providing disinhibition), using NMDA synapses (`nmda.mod`).

## Mechanisms
NMODL (`.mod`) files implement the ion-channel, synaptic, and receptor
mechanisms: nicotinic receptors (`a4b2_receptor.mod`, `a7.mod`), NMDA
synapses (`nmda.mod`), calcium dynamics (`cadyn.mod`, `cachan.mod`,
`capump.mod`), potassium/sodium channels (`kdr.mod`, `kca.mod`, `skca.mod`,
`nattxr.mod`, `nattxs.mod`), and transmitter release (`release.mod`).

## Repository structure
```
├── *.mod                # NMODL ion-channel / synapse / receptor mechanisms
├── *.hoc                # Cell templates (dopaminergic, cholinergic, glutamatergic)
├── driver.py            # Main simulation driver (dopa–cholinergic sweep)
├── tonic_dopa.py        # Dopaminergic tonic-firing simulation
├── subthreshold.py      # Subthreshold voltage analysis around spikes
├── PSD.py               # Power spectral density of subthreshold voltage
├── pfc_microcircuit.py  # Exploratory pyramidal + SOM/VIP interneuron circuit
├── test_glu.py          # Sanity test for the glutamatergic template
└── testDriver.hoc       # HOC-based test driver
```

## Requirements
- [NEURON](https://www.neuron.yale.edu/neuron/) (with Python support)
- Python 3, numpy, scipy, matplotlib, pandas

## Running
Compile the mechanisms first:
```bash
nrnivmodl
```
Then run any of the scripts, e.g.:
```bash
python tonic_dopa.py
python subthreshold.py
python pfc_microcircuit.py
```

## Notes
Compiled mechanism binaries (`arm64/`, `x86_64/`, etc.) are build artifacts
and can be regenerated with `nrnivmodl`.
