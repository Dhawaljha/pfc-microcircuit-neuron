TITLE Delayed rectifire
 
COMMENT
  from "An Active Membrane Model of the Cerebellar Purkinje Cell
        1. Simulation of Current Clamp in Slice"
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
}
 
NEURON {
    SUFFIX kdr
	USEION k WRITE ik
    RANGE  gkbar, gk, minf, hinf, ik, alpha, beta
	GLOBAL q10
} 
 
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}
 
PARAMETER {
        v (mV)
        celsius = 37 (degC)
        dt (ms)
        gkbar	= .6 (mho/cm2)
        ek	= -85 (mV)

}
 
STATE {
        m h
}
 
ASSIGNED {
        ik (mA/cm2)
        gk (mho/cm2)
		minf 
		hinf 
        alpha (/ms)
		beta (/ms)
		q10
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp
        gk = gkbar *m*m*h
	    ik = gk* (v-ek)
}
 
UNITSOFF
 
INITIAL {
    q10 = 3^((celsius - 37)/10)
	rates(v)
	m = minf
	h = hinf
}

DERIVATIVE states {  :Computes state variables m,h
        rates(v)      :             at the current v and dt.
        m' = (minf-m)/taum(v)
        h' = (hinf-h)/tauh(v)
}

PROCEDURE rates(v(mV)) {
        LOCAL gamma, zeta
        alpha = -0.0047*(v-8)/(exp((v-8)/(-12))-1)
        beta = exp((v+127)/(-30))
        minf = alpha/(alpha+beta)
        
        gamma = -0.0047*(v+12)/(exp((v+12)/(-12))-1)
        zeta = exp((v+147)/(-30))
        
        hinf = 1.0 / (1+exp((v+25)/4))
}

FUNCTION taum(v(mV)) (/ms) {
        LOCAL gamma, zeta
        gamma = -0.0047*(v+12)/(exp((v+12)/(-12))-1)
        zeta = exp((v+147)/(-30))
        taum = 1 / (q10 * (gamma + zeta))
}

FUNCTION tauh(v(mV)) (/ms) {
        if (v < -25) {
                tauh = 1200 / q10
        } else {
                tauh = 10 / q10
        }
}

 
UNITSON
