'''cut-off for mgdraw files.\n
searches file and discards all entries where neutron energy\n
is greater than the specified threshold.'''

import argparse


def readFile(fpath, threshold):
    ''''''
    outfile = []
    try:
        with open(fpath, 'r') as f:
            for line in f:
                line = line.split()
                E = float(line[1])  # the energy (adjust according to file)
                if E <= threshold:
                    line = '  '.join(line)
                    line = line + '\n'
                    outfile.append(line)
        return outfile

    except FileNotFoundError:
        print(f'---File {fpath} not found.---')


def writeFile(fpath, threshold, outpath='NEW_FILE.txt'):
    ''''''
    outfile = readFile(fpath, threshold)
    with open(outpath, 'w') as f:
        for line in outfile:
            f.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
                                     script to cut-off any neutrons
                                     above a threshold energy.''',
                                     add_help=False)
    parser.add_argument('-h', action="help",
                        help="""""")
    parser.add_argument('inp', type=str, help='name / path to file')
    parser.add_argument('threshold', type=float, help="energy cut-off (GeV)")
    parser.add_argument('ofile', nargs='?', default=5)

    args = parser.parse_args()
    writeFile(args.fpath, args.threshold, outpath=args.ofile)
