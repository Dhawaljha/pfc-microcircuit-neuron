INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX rel
	USEION ca READ ica, cai WRITE cai
	RANGE T,FA,CA,Fmax,Ves,b,u,k1,k2,k3,nt,kh
: from cad :
	RANGE depth,kt,kd,cainf,taur
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(mM) = (milli/liter)
: from cad:
	(molar) = (1/liter)			: moles do not appear in units
:	(mM)	= (millimolar)
	(um)	= (micron)
:	(mA)	= (milliamp)
	(msM)	= (ms mM)

}
: from cad:

CONSTANT {
	FARADAY = 96489		(coul)		: moles do not appear in units
:	FARADAY = 96.489	(k-coul)	: moles do not appear in units
}

PARAMETER {

	Ves = 0.04 	(mM)		: conc of vesicles
	Fmax = 0.001	(mM)		: conc of fusion factor F
	b = 1e10	(/mM4-ms)	: ca binding to F
	u = 0.1 	(/ms)		: ca unbinding 
	k1 = 1000   	(/mM-ms)	: F binding to vesicle
	k2 = 0.1	(/ms)		: F unbinding to vesicle
	k3 = 4   	(/ms)		: exocytosis of T
	nt = 10000			: nb of molec of T per vesicle
	kh = 15 	(/ms)		: cst for hydolysis of T
: from cad:
	depth	= 1	(um)		: depth of shell
	taur	= 1000	(ms)		: rate of calcium removal
	cainf	= 2.4e-4	(mM)		
	
}

ASSIGNED {
	ica		(mA/cm2)
	drive_channel	(mM/ms)
	drive_pump	(mM/ms)
}

STATE {
	FA	(mM)
	VA	(mM)
	T	(mM)
	cai	(mM) 
}

INITIAL {
	FA = 0
	VA = 0
	T = 0
	cai = cainf
}

BREAKPOINT {
	SOLVE state METHOD derivimplicit
}

LOCAL bfc , kfv

DERIVATIVE state {

	bfc = b * (Fmax-FA-VA) * cai^4
	kfv = k1 * FA * Ves
	FA'	= bfc - u * FA - kfv + k2 * VA
	VA'	= kfv - (k2+k3) * VA
	T'	= nt * k3 * VA - kh * T
: from cad:

	drive_channel =  - (10000) * ica / (2* FARADAY * depth)

	if (drive_channel <= 0.) { drive_channel = 0. }	: cannot pump inward
	
	cai'= -bfc + 4*u*FA + drive_channel  + (cainf-cai)/taur
	}	