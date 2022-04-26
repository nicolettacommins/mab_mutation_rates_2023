import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fastANI_output", type=str,
                    help="fastANI output file")
parser.add_argument("outfile", type=str,
					help="output file")
args = parser.parse_args()



filename=args.fastANI_output
try:
	file=pd.read_csv(filename, sep='\t', header=None)
	max_ani=file.iloc[:,2].max()
	if max_ani >= 98:

		x=file[file.iloc[:,2] >= 98]
		if len(x)==1:
			max_ref=x.iloc[0,1].split('/')[-2] #this is ugly but it works for now

			with open(args.outfile, 'w') as filehandle:
				filehandle.write('%s' % max_ref)

			print("      - Success! Wrote subspecies assignment to {}".format(args.outfile))

		else:
			print("      - {} has an ANI > 98 for more than one reference sequence. Could not assign subspecies.".format(args.outfile))

	else:
		print("      - {} has less than 98% ANI with any reference sequence. Could not assign subspecies.".format(filename))
except:
	print("      - Could not open {}. File may be empty.".format(filename))



