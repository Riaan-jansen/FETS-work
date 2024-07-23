import matplotlib.pyplot as plt
import numpy as np

# t_max = 24*3600*days for days
# step = 24*3600 for steps of days
t_max = 24*3600*365*100
step = 24*3600
n_max = int(t_max / step)


def buildup():
    '''buildup of be-7 over time. units nuclei/s'''
    be_rate = ((4.54E-4 + 4.85e-4 + 7.34e-4 + 5.81e-4 + 3.41e-4)
               * np.pi * 9 * 0.0025)
    be_rate = be_rate + (4.45E-04 + 4.06e-6) * np.pi * 9 * 0.005
    be_rate = be_rate * 3.75e+16
    return be_rate  # obsolete


def decay():
    '''be-7 half life is 53 days'''
    t_2 = 53.5 * 24 * 3600
    be_decay = 0.69314718056 / t_2
    return be_decay


def beam_on(n):
    '''manually adjustable cycle size, iterates over "on" cycle time for half
    the cycle, fraction of total n. period after ontime is beam shutdown'''
    cycle = 30
    result = []
    factor = 1.0
    ontime = int(n*factor)

    for i in range(ontime):
        # i % cycle = i (if cycle >i) = (int)remainder i / cycle (if cycle <i)
        # if ^ < (int)cycle/2 : 1.
        # half the cycle value (ie 15 from 30) will be 1, the next half will
        # be 0.
        if (i % (cycle)) < (cycle // 10):
            result.append(1)
        else:
            result.append(0)

    for i in range(ontime, n):
        # all off
        result.append(0)

    return result


# +       |    -
# buildup | decay
# start with all lithium nuclei. use rate of li decay to work out li at time t
# li/start * be_rate = +
# 1 - li/start * be_decay = -


def euler(n_max):
    decay_all = 4.2857E-9
    decay_pn = 2.6055E-13
    decay_be = decay()
    li_n = [3.5953E+22]
    be_n = [0]

    # beam_off returns list where ele=1 for beam on, 0 for off
    beam_factor = beam_on(n_max)

    for i in range(1, n_max):
        if beam_factor[i] != 0:
            li_f = -decay_all * li_n[i-1] + decay_be * be_n[i-1]
            be_f = -decay_be * be_n[i-1] + decay_pn * li_n[i-1]
        else:
            li_f = decay_be * be_n[i-1]
            be_f = -decay_be * be_n[i-1]

        li = (step * li_f) + li_n[i-1]
        be = (step * be_f) + be_n[i-1]

        li_n.append(li)
        be_n.append(be)
    return li_n, be_n


def plotter(n_max, days=True):
    if days is True:
        time = list(i * step/(3600*24) for i in range(n_max))
    else:
        time = list(i * step for i in range(n_max))
    li_n, be_n = euler(n_max)

    max_be = max(be_n)
    max_time = time[be_n.index(max(be_n))]

    # Plotting lithium, beryllium, and the peak beryllium point
    # plt.plot(time, li_n, label='lithium', lw=2)
    plt.plot(time, be_n, label='beryllium', lw=2)

    if days is True:
        plt.xlabel('Time (days)')
        plt.axvline(max_time, ls=':', label=f'''max be-7={max_be:.2e},
                    t={max_time:.3f}''')
        plt.axhline(5.647E+10, ls=':', label='''Background equivalent dose''',
                    color='red')
    else:
        plt.xlabel('Time (microseconds)')

    plt.legend()
    plt.grid()
    plt.semilogy()  # needed to see the detail
    plt.ylabel('Beryllium-7 nuclei')
    plt.title('Beryllium-7 nuclei in the target over time')
    plt.show()
    return None


def activity(N):
    '''input: number of be-7 nuclei. returns: activity (decays per second).
    OBSOLETE. a 42 fs half life will obviously not contribute to any dose
    removing the target.'''
    # where decay() is Be-7 decay constant
    # and factor 0.1 is for 10% gamma chance in be decay
    A = decay() * N * 0.1
    return A


def dose(N):
    '''Dose rate [J/kg/s] = activity [1/s] * energy of each decay [J] * weight
    * geometry / mass of target [kg]. Returns dose rate in microSv/hr'''
    E = 477 * 1.6E-16  # Energy per event in Joules
    mass = 70          # mass of target in kg
    weight = 1         # radiation weight. 1 for gamma, 5, 10, 20 for neutron.

    # for 1 m away 0.5x1.7 area human.
    geometry = 0.404 / (np.pi * 4)  # changes with distance and exposure

    print(activity(N))

    Dose = activity(N) * E * weight * geometry / mass
    return Dose * 3600 * 10**6


print(dose(7.5E+15), 'microSv/hr')

plotter(n_max, days=True)
