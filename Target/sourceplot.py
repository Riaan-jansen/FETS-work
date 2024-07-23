'''script contains:
- plotData which takes file and plots currently energy-flux for several
different volumes of target.
- ntof_reader for plotting time of flight fluka data
- and read_sheet & plot_pbeam for plotting of proton beam energy from excel.'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import simpson

# this file is the USRTRACK result for R=3, 300 micron thick, lithium target
# split into several slices. Proton beam E=3MeV 1cm square.
filename = 'burntrk_tab.lis'


def indexFinder(list, target):
    '''takes a list and a target value. calculates the square of the
    differences and finds the smallest difference and returns that index.'''
    residuals = []
    for x in list:
        r = (x - target)**2
        residuals.append(r)

    for i, ele in enumerate(residuals):
        if ele == min(residuals):
            index = i
            return index


def getData(fpath):
    '''open usrtrk_tab.lis file and read the data into x amount of volume
    groups. file must be: energy bin edges in first two columns, flux next
    with units in n/GeV/cmq/pr and error in 4th column in %.'''
    # using 1 cm square proton beam n/cm2 -> n
    p_beam = 3.75e+16  # protons / s
    with open(fpath, 'r') as f:
        file = f.read().strip()
        sections = file.split('\n\n')
        sections_list = [section.strip().split('\n') for section in sections]
    detectors = []
    array = []
    for section in sections_list:
        edges = []
        flux = []
        error = []

        for line in section:
            line = line.split()
            # Works with USRTRACK, USRYIELD and USRBDX where # is comment
            if line[0] == '#':
                if line[1] == 'Detector':
                    # Keeps detector name for plot label
                    detectors.append(line[4])
            else:
                midpoint = (float(line[0]) + float(line[1])) / 2
                edges.append(midpoint * 1e9)
                fval = float(line[2]) * p_beam * midpoint
                flux.append(fval)
                error.append(float(line[3]) * fval)  # % error * total flux
        array.append([edges, flux, error])

    array.append(detectors)
    return array


def plotData(fpath, show=True):
    ''''''
    array = getData(fpath)
    detectors = array[-1]

    area_xs = 0
    area_tot = 0
    area_useful = 0

    list_ratio = []
    list_total = []
    list_useful = []

    for i, ele in enumerate(array[:-1]):
        energy = ele[0]
        flux = ele[1]
        if show is True:
            plt.plot(energy, flux, label=f'detector {detectors[i]}',
                     lw=2, marker='o')

        # this is to see the total 'useful' protons from each detector.
        peak_start = 2.15e6     # start of the p,n peak
        peak_stop = 2.45e6      # end of the p,n peak
        threshold = 1.882e6  # threshold of the p,n reaction

        # finds the index of the above energy values
        idxstart = indexFinder(energy, peak_start)
        idxstop = indexFinder(energy, peak_stop)
        idxthr = indexFinder(energy, threshold)

        # integrates in the index limits and over the whole spectra
        peak_area = simpson(flux[idxstart:idxstop], energy[idxstart:idxstop])
        total_area = simpson(flux, energy)
        useful_area = simpson(flux[idxthr:], energy[idxthr:])

        # adds to the total area. for comparision of different target thickness
        area_xs = area_xs + peak_area
        area_tot = area_tot + total_area
        area_useful = area_useful + useful_area

        # adds individual bit to list to cast to array to plot bar chart
        list_total.append(total_area)
        list_useful.append(useful_area)

    # showing the plot. log y scale best
    if show is True:
        plt.title('Proton flux - energy measured in different volume elements')
        plt.xlabel('Energy (eV)')
        plt.ylabel('Flux (protons/cm2/s)')
        plt.legend()
        plt.semilogy()
        plt.grid()
        plt.show()
    else:
        return (detectors, list_total, list_useful)


def plotBar(fpath):
    '''plots the total protons in each volume element and useful ones.'''
    tuple = plotData(fpath, show=False)
    detectors = tuple[0]
    list_total = tuple[1]
    list_useful = tuple[2]

    plt.title('Proton tracking in each element of the target')
    plt.xlabel('Detector region (microns)')
    plt.ylabel('Protons (a.u.)')
    plt.bar(detectors, list_total, color='blue', label='Total protons')
    plt.bar(detectors, list_useful, bottom=list_total, color='r',
            label='Protons above threshold')
    for i, label in enumerate(detectors):
        ratio = list_useful[i]/list_total[i] * 100
        plt.annotate(f'{ratio:.5f} %     ',
                     xy=(detectors[i], list_total[i]),
                     xytext=(-0.32+i, list_total[i]*1.10))
    plt.legend()
    plt.show()


plotData(filename)
plotBar(filename)


def reader(fpath):
    energy = []

    with open(fpath, 'r') as f:
        for line in f:
            line = line.split()
            energy.append(float(line[1]))

    return energy


def ntof_reader(fpath):
    energy = []
    age = []
    weight = []

    with open(fpath, 'r') as f:
        for line in f:
            line = line.split()
            energy.append(float(line[1]))
            age.append(float(line[2]))
    bins = np.logspace(-10, 1, num=20)
    plt.hist(age, bins=bins)
    plt.semilogx()
    plt.show()
    return None


def plotter(fpath):
    energy = reader(fpath)

    plt.hist(energy, bins=200)
    # plt.semilogx()

    plt.show()


def plot_pbeam(length, energy):

    plt.plot(length, energy, color='blue', marker='o')
    plt.title("Proton Beam Energy against Target Depth")
    plt.xlabel("Target thickness (microns)")
    plt.ylabel("Beam particle energy (keV)")
    plt.axhline(y=2180, ls='--', color='red', label='within (p,n) peak')
    plt.axhline(y=2500, ls='--', color='red')
    plt.axhline(y=1880, ls='--', label='threshold (p,n)')
    plt.legend()
    plt.grid()
    plt.show()


def read_sheet(filename):
    data = pd.read_csv(filename)
    length = data['length']
    energy = data['energy']
    return length, energy


def read_source(filename):
    # array = ([midpoint, flux, error])
    flux = []
    erg = []
    array = getData(filename)
    for row in array:
        for ele in row:
            print(ele[0], ele[1])
        
        
read_source('ntof_src_tab.lis')

# length = [0, 50, 100, 150, 200, 250, 300]
# energy = [3, 2.715, 2.4, 2.06, 1.66, 1.18, 0.46]

length, energy = read_sheet('Spreadsheet4.csv')
plot_pbeam(length, energy)

# plotter('sourcef')
# ntof_reader('ntof2001_sourcentof')
# plot_pbeam()
