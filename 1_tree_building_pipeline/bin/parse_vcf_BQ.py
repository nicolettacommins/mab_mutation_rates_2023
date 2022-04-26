#!/usr/bin/env python3

import allel
import pickle
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("subsp_list", type=str,
					help="text file with a list of all the samples")
parser.add_argument("chrom_length", type=str,
					help="length of main alignment (excluding plasmids)")
parser.add_argument("BQ_thresh", type=str,
					help="threshold for base quality")
parser.add_argument("outfile", type=str,
					help="named of outfile to store dictionary")
args = parser.parse_args()

chrom_length=int(args.chrom_length)
sample_list = [line.rstrip('\n') for line in open(args.subsp_list)]

BQ=[0]*chrom_length
BQ_thresh=int(args.BQ_thresh)

for sample in sample_list:
	filepath = 'results/{}/pilon/{}_full.vcf.gz'.format(sample,sample)
	callset = allel.read_vcf(filepath, fields=['variants/CHROM', 'variants/BQ', 'variants/POS'])
	for i in range(0,len(callset['variants/BQ'])):
		if callset['variants/CHROM'][i]!=callset['variants/CHROM'][0]:
			break
		if -1< callset['variants/BQ'][i]<BQ_thresh:
			BQ[callset['variants/POS'][i]-1]=BQ[callset['variants/POS'][i]-1]+1	
	print("Counted {}.".format(sample))

with open(args.outfile, 'wb') as handle:
	pickle.dump(BQ, handle, protocol=pickle.HIGHEST_PROTOCOL)





