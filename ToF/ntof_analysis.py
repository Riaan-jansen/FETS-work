import spec_utilities as su
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


filename1 = 'ntof_src_tab.lis'
filename = 'tof_file'


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
        edges = []  # add starting point here (i.e. 1e-14) if histogram
        flux = []
        error = []

        for line in section:
            line = line.split()
            # Works with USRTRACK, USRYIELD and USRBDX where '#' is comment
            if line[0] == '#':
                if line[1] == 'Detector':
                    # Keeps detector name for plot label
                    detectors.append(line[4])
            else:
                # not edges - every interval after 1st. watch for shifting
                edges.append(float(line[1]))
                # for differential yield dN/dx1dx2 - this is * dx1
                midpoint = (float(line[0]) + float(line[1])) / 2
                fval = float(line[2]) * midpoint * p_beam
                flux.append(fval)
                error.append(float(line[3]) * fval / 100)  # % error * total

        array.append([edges, flux, error])

    array.append(detectors)
    # array is a list where each entry is a detector, with each detector
    # being a list of lists (edges, flux, error). array[-1] is det names.
    return array


def getPeaks(fpath, show=False):
    '''receives data. iterates over each detector to find peak with scipy.
    fits gaussian to peak'''
    array = getData(fpath)
    detectors = array[-1]
    width = 0.0001
    fwhms = []

    for i, ele in enumerate(array[:-1]):
        time = ele[0]
        flux = ele[1]

        # need to fit ONE gaussian to the data. need the most prominent peak
        maxflux = max(flux)
        index = flux.index(maxflux)

        try:
            params = su.guess_fit(time, flux, guess_0=time[index],
                                  guess_2=width)
            fit, opt = su.gauss_fit(time, flux, guess=params)

            FWHM = 2.355*opt[2]
            # FWHM = findFWHM(fit, time)
            fwhms.append((detectors[i], float(FWHM), float(opt[0]),
                          float(opt[1])))  # opt[0] is centre

        except RuntimeError:
            print('Gaussian could not be fitted to ', detectors[i])
            pass

        if show is True:
            plt.plot(time, flux, label=f'detector {detectors[i]}',
                     lw=2, marker='o')
            plt.plot(time, fit, color='r', ls='--')
            plt.axvline(time[index], color='grey', ls=':')
            try:
                # plt.semilogx()
                plt.legend()
                plt.show()
            except UserWarning:
                print('Data undefined. Can not log y.')

    return fwhms


def findFWHM(fit, array):
    '''OBSOLETE. and also not working
    takes: fit (y array), array (x array)
    returns: FWHM'''
    idxmax = np.argmax(fit)
    maximum = fit[idxmax]
    halfmax = maximum/2
    res1 = []
    res2 = []
    for i in fit[:idxmax]:
        r = (i - halfmax)**2
        res1.append(r)
    for i in fit[idxmax:]:
        r = (i - halfmax)**2
        res2.append(r)

    try:
        print('mins', min(res1), min(res2), '\n')
        idx1 = res1.index(min(res1))
        idx2 = res2.index(min(res2))
        print('times', array[idx2],  array[idx1], '\n')
        FWHM = array[idx2] - array[idx1]
        return FWHM
    except ValueError:
        print('no minimum found')
        return None


def plotFWHM(fpath):
    '''uses getPeaks to create array of FWHM values and then plot the
    relationship between detector (energy~wavelength) and FWHM.'''
    fwhms = getPeaks(fpath, show=False)
    widths = [tup[1] for tup in fwhms]
    # names of detectors need to be float!
    names = [float(tup[0]) for tup in fwhms]
    peaks = [float(tup[2]) for tup in fwhms]

    plt.bar(names, widths)
    plt.title('FWHM for time of flight of neutrons 1-10 A')
    plt.ylabel('FWHM (s)')
    plt.xlabel('Wavelength (A)')
    plt.show()


def resolvePeaks(fpath):
    ''''''
    fwhms = getPeaks(fpath, show=False)
    widths = [tup[1] for tup in fwhms]
    # names of detectors need to be float!
    names = [float(tup[0]) for tup in fwhms]
    peaks = [float(tup[2]) for tup in fwhms]

    plt.errorbar(peaks, names, xerr=[x/2 for x in widths], capsize=10, fmt='s')
    plt.scatter(peaks, names, marker='s', s=16, cmap='inferno')
    plt.title('Resolution of different wavelengths')
    plt.xlabel('Time (s)')
    plt.ylabel('wavelengths (A)')
    plt.grid()
    plt.show()


class wavelengths():
    def __init__(self):
        # wavelength <- energy bins
        self.A10 = [8.030e-13, 8.358e-13]
        self.A9 = [9.892e-13, 1.034e-12]
        self.A8 = [1.248e-12, 1.313e-12]
        self.A7 = [1.624e-12, 1.720e-12]
        self.A6 = [2.200e-12, 2.353e-12]
        self.A5 = [3.140e-12, 3.412e-12]
        self.A4 = [4.870e-12, 5.386e-12]
        self.A3 = [8.523e-12, 9.740e-12]
        self.A2 = [1.857e-11, 2.269e-11]
        self.A1 = [6.769e-11, 1.011e-10]
        # time bins according to wavelength
        self.nbins = 100
        self.time = np.logspace(-7, -1, num=self.nbins)
        self.T10 = [-3, -2]


def readFile(fpath):
    '''reads collision tape for energy, age and weight.\nbins into wavelength
intervals as requested.\n'''
    # range class contains energy intervals for associated wavelengths
    bins = wavelengths()

    # first entry is title for later use in dataframe
    energy = ['energy']
    time = ['time']
    weight = ['weight']
    A1 = [1]
    A2 = [2]
    A3 = [3]
    A4 = [4]
    A5 = [5]
    A6 = [6]
    A7 = [7]
    A8 = [8]
    A9 = [9]
    A10 = [10]
    ALL = [0]

    # opening the file to read line by line, strip() takes out whitespace.
    try:
        with open(fpath, 'r') as f:
            for line in f:
                line = line.split()
                E = line[1]  # the element corresponding to
                T = line[2]  # that value in the file
                W = line[3]  # make sure to check the index
                energy.append(float(E))
                time.append(float(T))
                weight.append(float(W))

    # if the energy falls within the requested bin, append time to the
    # associated wavelength list
        for i, x in enumerate(energy[1:]):
            if bins.A1[0] <= x <= bins.A1[1]:
                A1.append(time[i])
            if bins.A2[0] <= x <= bins.A2[1]:
                A2.append(time[i])
            if bins.A3[0] <= x <= bins.A3[1]:
                A3.append(time[i])
            if bins.A4[0] <= x <= bins.A4[1]:
                A4.append(time[i])
            if bins.A5[0] <= x <= bins.A5[1]:
                A5.append(time[i])
            if bins.A6[0] <= x <= bins.A6[1]:
                A6.append(time[i])
            if bins.A7[0] <= x <= bins.A7[1]:
                A7.append(time[i])
            if bins.A8[0] <= x <= bins.A8[1]:
                A8.append(time[i])
            if bins.A9[0] <= x <= bins.A9[1]:
                A9.append(time[i])
            if bins.A10[0] <= x <= bins.A10[1]:
                A10.append(time[i])
            # for plotting across 1 - 10 A.
            if bins.A10[0] <= x <= bins.A1[1]:
                ALL.append(time[i])
        print(A10)
        plt.hist(A10, bins=np.logspace(-3, -2, num=25))
        # plt.semilogy()
        plt.semilogx()
        # plt.show()

    except FileNotFoundError:
        print(f'---File {fpath} not found.---')


def plot_rftr():
    '''quick plot for rftr material comparison'''
    

# readFile(filename)
# resolvePeaks('beam9_33_tab.lis')
file = 'beam9fin_0_tab.lis'
getPeaks(file, show=True)
plotFWHM(file)
