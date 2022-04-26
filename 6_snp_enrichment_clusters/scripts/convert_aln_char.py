# 20210507NC 
# script to convert all the Ns to -s in an alignment

# imports
import sys
import argparse
import re
from Bio import AlignIO
from Bio.Seq import Seq

# command line parsing
def get_options():

    parser = argparse.ArgumentParser(description='Remove all instances of one character'
                                    'from an alignment and replace them with a new character',
                                     prog='convert_aln_char')

    # input options
    parser.add_argument('--in_aln',
                        help = 'Input alignment (FASTA format)',
                        required = True)
    parser.add_argument('--out_aln',
                        help = 'Output file name (FASTA format)',
                        required = True)
    parser.add_argument('--old_char',
                        help = 'character we want to replace',
                        required=True)
    parser.add_argument('--new_char',
                        help = 'character we want to insert instead of --from_char',
                        required=True)

    return parser.parse_args()

# main code
if __name__ == "__main__":

    # Get command line options
    args = get_options()

    # Read in alignment
    alignment = AlignIO.read(args.in_aln,'fasta')
    for taxon in alignment:
        new_seq=str(taxon.seq).replace(args.old_char, args.new_char)
        taxon.seq=Seq(new_seq)

    with open(args.out_aln,'w') as output_alignment:
        AlignIO.write(alignment, output_alignment, 'fasta')
