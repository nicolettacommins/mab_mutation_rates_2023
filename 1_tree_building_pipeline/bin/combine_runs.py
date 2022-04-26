#Written by LF, modified by NC
#makes directory of trimmed reads more general
import argparse
import json
import pandas as pd
import sys
import os
import re
import subprocess as sbp
from itertools import islice

parser = argparse.ArgumentParser()
parser.add_argument("biosample", type=str,
                    help="Biosample we are interested in")
parser.add_argument("summary_runs", type=str,
                    help="tsv containing the associations biosample => run_ids")
parser.add_argument("trimmed_fastq_dir", type=str,
                    help="directory containing the temporary files of the results")
parser.add_argument("fastq_dir", type=str,
                    help="directory where I want to put my combined fastq files")
args = parser.parse_args()

# I get the data about my strain
print("- I am retrieving the data about the runs to analyze from {}".format(args.summary_runs))
tab=pd.read_csv(args.summary_runs, sep="\t")
tab_sel=tab.loc[tab["biosample"]==args.biosample]
## If I do not find anything, the analysis finishes here
if tab_sel.shape[0] == 0:
    raise Exception("- [ERROR] Sorry! I did not find the biosample you provided in the summary runs file.") 
## If I find multiple lines corresponding to one biosample, something went wrong too
elif tab_sel.shape[0] > 1:
    raise Exception("- [ERROR] There are multiple lines in the summary_runs file that match the biosample you provided.") 
else:
    runs=tab_sel.iloc[0]["run_id"].split(",")

    # Now I can combine the runs that succeeded
    fq_comb1 = os.path.join(args.fastq_dir, "combined/", args.biosample + "_1_combined.fastq")
    fq_comb2 = os.path.join(args.fastq_dir, "combined/", args.biosample + "_2_combined.fastq")

    # I reinitialize the fastq files.
    cmd="touch {}".format(fq_comb1)
    os.system(cmd)
    cmd="touch {}".format(fq_comb2)
    os.system(cmd)

    for run in runs:
        trflstem1 = os.path.join(args.trimmed_fastq_dir, run + "_1_trimmed.fastq")
        trflstem2 = os.path.join(args.trimmed_fastq_dir, run + "_2_trimmed.fastq")
        cmd="cat {0} >> {1}".format(trflstem1,fq_comb1)
        os.system(cmd)
        cmd="cat {0} >> {1}".format(trflstem2,fq_comb2)
        os.system(cmd)
