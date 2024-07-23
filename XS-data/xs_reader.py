import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def reader(fpath=None):
    list = []
    if fpath is None:
        fpath = input('Type filename: ')
    data = open(fpath, 'r')
    energy = []
    xs = []
    for i, line in enumerate(data):
        line = line.split()
        if '//' in line[0]:
            break
        if '#' not in line[0]:
            energy.append(line[0])
            xs.append(line[1])
    data.close()
    return energy, xs


def plotter(fpath=None):
    x, y = reader(fpath)
    plt.step(x, y)

    plt.show()


def csv_plotter(filenames):

    for i, _ in enumerate(filenames):

        idata = pd.read_csv(filenames[i], delimiter=',')
        headers = idata.columns.tolist()

        for j in headers:
            if '(EV) 1.1' in j:
                e_header = j
            if 'DATA ' in j:
                xs_header = j

        edata = idata[e_header]
        xsdata = idata[xs_header]

        plt.plot(edata, xsdata, label=filenames[i])
        plt.annotate(filenames[i], (edata[0], xsdata[0]))

    plt.xlabel('Energy (eV)')
    plt.ylabel('Cross section (b)')
    plt.title('xs data. ')
    plt.xlim(right=7e6)
    plt.legend()
    plt.grid()
    plt.show()


filenames = ['Li7(p,n).csv', 'Be10(p,n).csv']# , 'H3(p,n).csv']
# filenames = ['K41(p,n).csv', 'Ca48(p,n).csv', 'Be10(p,n).csv',
#             'B11(p,n).csv', 'C13(p,n).csv', 'Li7(p,n).csv', 'O18(p,n).csv',
#             'H3(p,n).csv', 'C14(p,n).csv', 'S34(p,n).csv', 'Ti49(p,n).csv',
#             'V51(p,n).csv', 'V51(p,n).csv', 'Cr53(p,n).csv', 'Mn55(p,n).csv',
#             'Au197(p,n)ND.csv', 'U238(p,n).csv', 'Fe57(p,n).csv']
fpaths = ['Nuclear_Data/'+i for i in filenames]
csv_plotter(fpaths)


def xs_plotter():
    '''quick bar graph of xs data @ 3 MeV for poster'''
    mat = ['Be9', 'Li7', 'H3', 'Ti49']
    xs = [0.095, 0.295, 0.53426, 0.144]

    plt.bar(mat, xs, color=['red', 'green', 'blue', 'brown'])
    plt.xlabel('Isotope')
    plt.ylabel('Cross section (B)')
    plt.title('Isotope - (p, n) cross section at 3 MeV')
    plt.grid('minor', lw=0.3)
    plt.minorticks_on()
    plt.show()

# xs_plotter()

# E0li, xs0li = reader("Li7-L0.txt")
# E1li, xs1li = reader("Li7-L1.txt")

# E0be, xs0be = reader("Be9-L0.txt")
# E1be, xs1be = reader("Be9-L1.txt")

# plt.scatter(E0li, xs0li, label='Li7')
# plt.scatter(E0be, xs0be, label='Be9')

# plt.show()
