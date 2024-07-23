import pandas as pd
import argparse


def getFiles(input, cycles):
    '''in: name of input folder, out: dataframe with regions and
    energies as columns.'''
    start = r"1Region"
    end = r"Total (integrated over volume):"
    Energy = []
    Region = []
    data = []
    for i in range(1, cycles + 1):
        file = input + f'00{i}.out'
        try:
            lines = []
            with open(file, 'r') as f:
                appending = False
                for line in f:
                    if end in line:
                        break
                    if start in line:
                        appending = True
                    if appending is True:
                        lines.append(line.split())
                lines = lines[4:-1]  # works around whitespace/headers
            data.append(lines)
        except FileNotFoundError:
            print('File not found')

    for line in data:
        for row in line:
            # casts to float and replaces double notation
            erg = float(row[5].replace('D', 'E'))
            Energy.append(erg)
            Region.append(row[1])

    dict = {'Region': Region, 'Energy': Energy}
    df = pd.DataFrame(dict)
    df = df.filter(regex='TAR')
    return df


def getInfo(input, cycles=5):
    '''uses erg2heat() to convert energy from dataframe to heat
    and prints to terminal all the values. returns none'''
    df = getFiles(input, cycles)
    # makes a list of all unique elements in 'Region'
    regions = df['Region'].unique().tolist()
    print(r'''
-----------------------------------------
REGION   :: Energy (keV)   +/- Standard Deviation
-----------------------------------------''')
    for region in regions:
        values = df['Energy'].where(df['Region'] == region)
        # takes the mean/stdev of all the values where 'region' = region
        # * 1E6 to convert from GeV to keV.
        mean = float(values.mean()) * 1E6
        std = float(values.std()) * 1E6

        print(f'{region:8} :: {mean:.4e} +/- {std:.4e}')

    print(42*'-', '\nNo. of Regions: %i' % len(regions))
    print(f'''{42*'-'}''')
