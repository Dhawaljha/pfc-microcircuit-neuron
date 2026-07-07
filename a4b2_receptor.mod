NEURON {
  POINT_PROCESS a4b2
  USEION na READ ena WRITE ina
  USEION ca READ eca WRITE ica  
  POINTER C_in
  RANGE C0, C1, C2, C3, D1, D2, O1, O2,erev, i
  RANGE g, gmax, rb3, rob, rb1, rb2
  GLOBAL Rb1, Ru1, Rb2, Ru2, Rb3, Ru3, a1, b1, a2, b2, Rob, Rou, Rr1, Rd1, Rr2, Rd2
}

UNITS {
  (nA) = (nanoamp)
  (mV) = (millivolt)
  (pS) = (picosiemens)
  (umho) = (micromho)
  (mM) = (millimole/liter)
  (uM) = (micromole/liter)
  (mA) = (milliamp)
}

PARAMETER {
  gmax	= 60  (pS)	: maximal conductance
: Rates

  Rb1 = 33 (/mM /ms)
  Ru1 = 981.3e-03 (/ms)
  Rb2 = 22 (/mM /ms)
  Ru2 = 1962.6e-03 (/ms)
  Rb3 = 11 (/mM /ms)
  Ru3 = 2944e-03 (/ms)
  a1 = 6.4e-08 (/ms)
  b1 = 43e-03 (/ms)
  a2 = 2772e-03 (/ms)
  b2 = 6550e-03 (/ms)
  Rob = 14 (/mM /ms)
  Rou = 356e-03 (/ms)
  Rd1 = 207e-03 (/ms)
  Rr1 = 38e-03 (/ms)
  Rd2 = 1014e-03 (/ms)
  Rr2 = 51e-03 (/ms)
  erev = 0 (mV)
}

ASSIGNED {
  v		(mV)		: postsynaptic voltage
  g 		(pS)		: conductance
  C_in (mM)
  rb1 (/ms)
  rb2 (/ms)
  rb3 (/ms)
  rob (/ms)
  i (nA)
  eca (mV)
  ena (mV)
  ica (nA)
  ina (nA)
}

STATE {
   C0 C1 C2 C3 O1 O2 D1 D2
}

INITIAL {
  C0 = 1
}

BREAKPOINT {
  SOLVE kstates METHOD sparse

  g = gmax * (O1 + O2)
  ina = (1e-6)*(10/28)*g*(v-ena)
  ica = (1e-6)*(18/28)*g*(v-eca)
  i = ina + ica 
}

KINETIC kstates {
    rb1 = Rb1 * C_in
	rb2 = Rb2 *C_in
	rb3 = Rb3 *C_in
	rob = Rob * C_in
	
   ~C0 <-> C1 (rb1, Ru1)
   ~C1 <-> C2 (rb2, Ru2)
   ~C2 <-> C3 (rb3, Ru3)
   ~C2 <-> O1 (b1, a1)
   ~C3 <-> O2 (b2, a2)
   ~O1 <-> O2 (rob, Rou)
   ~O1 <-> D1 (Rd1, Rr1)
   ~O2 <-> D2 (Rd2, Rr2)
 
  CONSERVE C0+C1+C2+C3 + O1+ O2+D1+D2 = 1
 }

