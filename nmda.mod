INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
    POINT_PROCESS nmda
    POINTER C
    USEION na READ ena WRITE ina
    USEION ca READ eca WRITE ica
    RANGE C0, C1, C2, D, O, B
    RANGE g, gmax, rb
    RANGE ina, ica, eca, ena, i
    GLOBAL mg, Rb, Ru, Rd, Rr, Ro, Rc
    GLOBAL vmin, vmax
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (pS) = (picosiemens)
    (umho) = (micromho)
    (mM) = (milli/liter)
    (uM) = (micro/liter)
}

PARAMETER {

    Erev = 0      (mV)
    gmax = 300    (pS)
    mg = 1        (mM)
    vmin = -120   (mV)
    vmax = 100    (mV)

    Rb = 5        (/mM /ms)
    Ru = 9.5e-3   (/ms)
    Rd = 16e-3    (/ms)
    Rr = 13e-3    (/ms)
    Ro = 25e-3    (/ms)
    Rc = 59e-3    (/ms)
}

ASSIGNED {
    v   (mV)
    i   (nA)
    g   (pS)
    C   (mM)
    rb  (/ms)
    ena (mV)
    eca (mV)
    ina (nA)
    ica (nA)
}

STATE {
    C0
    C1
    C2
    D
    O
    B
}

INITIAL {
    rates(v)
    C0 = 1
}

BREAKPOINT {
    rates(v)
    SOLVE kstates METHOD sparse

    g = gmax * O * B
    ina = (1e-06) * g * 0.25 * (v - ena)
    ica = (1e-06) * g * 0.75 * (v - eca)
    i = ina + ica
}

KINETIC kstates {
    rb = Rb * C

    ~ C0 <-> C1 (2*rb, Ru)
    ~ C1 <-> C2 (rb, 2*Ru)
    ~ C2 <-> D  (Rd, Rr)
    ~ C2 <-> O  (Ro, Rc)

    CONSERVE C0 + C1 + C2 + D + O = 1
}

PROCEDURE rates(v(mV)) {
    TABLE B DEPEND mg FROM vmin TO vmax WITH 200

    : Mg2+ block - Jahr & Stevens
    B = 1 / (1 + exp(0.062 * (-v)) * (mg / 3.57))
}
