NEURON {
  POINT_PROCESS a7
  POINTER C_in
  USEION na READ ena WRITE ina
  USEION ca READ eca WRITE ica
  RANGE i
  RANGE  R, aR, a2R, a3R, a4R, a5R,  a2D, a3D, D, aD, a4D, a5D, O
  RANGE g, gmax
  GLOBAL Rb, Ru, a, b, Rd, Rr, Rd1, rb
}

UNITS {
  (nA) = (nanoamp)
  (mV) = (millivolt)
  (pS) = (picosiemens)
  (umho) = (micromho)
  (mM) = (milli/liter)
  (uM) = (micro/liter)
  (mA) = (milliamp)
}

PARAMETER {
  gmax	= 95 (pS)	: maximal conductance
: Rates
  Rb = 50 (/mM /ms)
  Ru = 20 (/ms)
  a = 0.5 (/ms)
  b = 20 (/ms)
  Rd = 1e-3 (/ms)
  Rr = 2e-3 (/ms)
  Rd1 = 1 (/ms)
 }

ASSIGNED {
  v		(mV)		
  i	(nA)		
  g 		(pS)		
  rb		(/ms)    
  ica (nA)
  ina (nA)
  C_in (mM)
  ena (mV)
  eca (mV)
}

STATE {
  R aR a2R a3R a4R a5R O a2D a3D D aD a4D a5D
}

INITIAL {
  R = 1
}

BREAKPOINT {
  SOLVE kstates METHOD sparse
  
  g = gmax * O 
  ina = (1/11)* (1e-6) * g * (v - ena)
  ica = (10/11)* (1e-6) * g * (v - eca)
  i = ina + ica 
}

KINETIC kstates {
     rb = Rb * C_in
    
   ~ R <-> aR (5*rb, Ru )
   ~ aR <-> a2R (4*rb, 2*Ru)
   ~ a2R <-> a3R (3*rb, 3*Ru)
   ~ a3R <-> a4R (2*rb, 4*Ru)
   ~ a4R <-> a5R (rb, 5*Ru)
   ~ R <-> D (Rd, 32*Rr )
   ~ aR <-> aD (Rd, 16*Rr)
   ~ a2R <-> O (b, a)
   ~ O <-> a2D (Rd1, 8*Rr)
   ~ a3R <-> a3D (Rd, 4*Rr)
   ~ a4R <-> a4D (Rd, 2*Rr)
   ~ a5R <-> a5D (Rd, Rr)
   ~ D <-> aD (5*rb, Ru)
   ~ aD <-> a2D (4*rb, 2*Ru)
   ~ a2D <-> a3D (3*rb, 3*Ru)
   ~ a3D <-> a4D (2*rb, 4*Ru)
   ~ a4D <-> a5D (rb, 5*Ru)
   
  CONSERVE R + aR + a2R + a3R + a4R + a5R + O + a2D + a3D + D + aD + a4D + a5D = 1 
 }