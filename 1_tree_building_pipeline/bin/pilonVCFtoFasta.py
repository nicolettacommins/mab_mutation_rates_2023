#!/usr/bin/env python

import sys
import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


#####################
# This script takes a variable number of input vcf files.  Each vcf file must contain
# snp information about only one strain.  At least one input file must be supplied.  The
# name of an output file must also be supplied, and output is in snpt able format.  The
# output contains the combined information about all strains.
# NOTE : position for indels is the locus before the insertion or deletion

# Got from Grad Lab, modified by NC 2020040
# NOTE: modified in a hacky way only to get the first chromosome because for MAB stuff I want to ignore plasmids for now.
#############


# check for correct number of inputs
if len(sys.argv) != 3 :
     print("Usage: VCFToFasta.py <input vcf> <output fasta>")
     sys.exit(0)

def read_vcf(inFile):
    """Create strings corresponding to chromosome"""
    with open(inFile, 'r') as vcf:

        # Get chrom name and length.
        for line in vcf:
            if ("contig" in line and "length" in line):
                line = line.strip()
                length = line.split("=")[-1].strip(">")
                print(length)
                refID = line.split(",")[0].split("=")[-1]
                chromosome = ["N"] * int(length)
                break

        # write sequence into chromosome 
        for line in vcf:
            if line[0] != "#" and refID in line:
                line = line.strip()
                CHROM, POS, ID, REF, ALT, QUAL, FILTER = line.split()[0:7]
                FILTERS = FILTER.split(";")
                if len(REF) == 1 and len(ALT) == 1: # keep this the way it is
                    if "PASS" in FILTERS:
                        if ALT == ".":
                            ALLELE = REF
                        else:
                            ALLELE = ALT
                    else:
                        print(FILTER)
                index = int(POS) - 1
                chromosome[index] = ALLELE
    return(chromosome, refID)

def write_fasta(chromosome, outFile, refID, sample):
    record = SeqRecord(Seq("".join(chromosome)), id=refID, description=sample) #changed ID to refID so will be compatible with bedtools maskfasta
    SeqIO.write(record, outFile, "fasta")

sample_name = os.path.basename(sys.argv[1])[0:-4]
chromosome, refID = read_vcf(sys.argv[1])
write_fasta(chromosome, sys.argv[2], refID, sample_name)


