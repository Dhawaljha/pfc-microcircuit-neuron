NEURON {
  SUFFIX kdyn
  USEION k READ ko,ik WRITE ko 
  RANGE ko, ko0, KAF
}

UNITS {
  (mM) = (milli/liter)
  (mA) = (milliamp)
   F    = (faraday) (coul)
}

PARAMETER {
  dtau    = 7 (ms)           : decay time constant
  ko0 = 5.9	(mM)     
  dep = 0.2 (micron) 
  KAF = 2
}

ASSIGNED {
  ik     (mA/cm2)
}

INITIAL{
   ko = ko0
}

STATE {
  ko
}

BREAKPOINT { 
  SOLVE states METHOD derivimplicit
}

DERIVATIVE states {
  ko'= 1e4*ik/(F*dep*KAF) + (ko0-ko)/dtau
}
