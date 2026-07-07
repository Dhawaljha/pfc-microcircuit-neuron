TITLE Nicotine Pulse Injector for nAChRs

NEURON {
    POINT_PROCESS AChPulse
    RANGE pulse_amp, pulse_dur, pulse_isi, num_pulses, ACh_out, condition
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (pS) = (picosiemens)
    (mM) = (millimole/liter)
}

PARAMETER {
    pulse_amp[2]        : Three test [low, mid, high] nicotine concentrations (mM)
    pulse_dur = 20 (ms) : Duration of each nicotine pulse
    pulse_isi = 100 (ms): ISI between pulses (start to start interval)
    num_pulses = 40      : Number of pulses
    condition = 0       : 0 = low, 1 = high
}

ASSIGNED {
    ACh_out (mM)   : Output signal, exposure to a3b4 nAChR
    pulse_count         : For tracking pulses internally
}

INITIAL {
    pulse_amp[0] = 0.001 (mM)
    pulse_amp[1] = 0.010 (mM)
    ACh_out = 0
    pulse_count = 0
    net_send(0, 1)      : Start first pulse immediately
}

BREAKPOINT {
    : Only event-driven
}

NET_RECEIVE (w) {
    :printf("Time: %g, Flag: %g, Pulse count: %g, ACh_out: %g\n", t, flag, pulse_count, ACh_out)
    
    if (flag == 1) {
        if (pulse_count < num_pulses) {
            ACh_out = pulse_amp[condition]
            pulse_count = pulse_count + 1
            net_send(pulse_dur, 2)
            :printf("Started pulse %g at time %g\n", pulse_count, t)
        }
    } else if (flag == 2) {
        ACh_out = 0
        : recursive net_event removed
        if (pulse_count < num_pulses) {
            net_send(pulse_isi - pulse_dur, 1)
            :printf("Ended pulse, scheduled next at time %g\n", t + pulse_isi - pulse_dur)
        }
    }
}
