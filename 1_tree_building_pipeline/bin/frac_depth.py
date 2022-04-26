#!/usr/bin/env python3

import argparse
import pandas as pd
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("subsp_list", type=str,
                    help="test file with a list of all the samples")
parser.add_argument("chrom_length", type=str,
                    help="length of main alignment (excluding plasmids)")
parser.add_argument("depth_thresh", type=str,
                    help="threshold for sequencing depth")
parser.add_argument("outfile", type=str,
                    help="named of outfile to store dictionary")
args = parser.parse_args()

depth = {}
sample_list = [line.rstrip('\n') for line in open(args.subsp_list)]
chrom_length=int(args.chrom_length)
depth_thresh=int(args.depth_thresh)

for sample in sample_list:
	filepath = 'results/{}/depth/{}.depth'.format(sample,sample)
	file=pd.read_csv(filepath, sep='\t', header=None)

	#calculate the fraction of the reference genome with coverage >20x
	frac_depth=sum(file.iloc[0:chrom_length,2]>depth_thresh)/chrom_length

	#write to dict
	depth[sample]=frac_depth

	print('Read {}'.format(sample))

	del file

with open(args.outfile, 'wb') as handle:
    pickle.dump(depth, handle, protocol=pickle.HIGHEST_PROTOCOL)



