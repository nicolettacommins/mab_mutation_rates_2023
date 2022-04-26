
####################

# Purpose: This snakefile takes a list of run accessions as input, downloads the fastq files, compresses them, and runs initial quality steps.

###################


## retrieve run accessions from a list
with open(config["runs"], "r") as inp:
    runs = inp.read().splitlines()

# retrieve run accessions from summary runs table
import pandas as pd
#with open(config["summary_runs"], "r") as inp:
#    runs=pd.read_csv(inp, sep='\t').run_id.tolist()

reads = ['1', '2']

adapter_list=config["adapter_list"]

rule all:
    input:  
        expand(config["temp_dir"]+"{run}_{read}.fastq", run=runs, read=reads),
        expand(config["trimmed_dir"]+"trimmed/{run}_1_trimmed.fastq", run=runs),
        expand(config["trimmed_dir"]+"trimmed/{run}_2_trimmed.fastq", run=runs),
        expand(config["trimmed_dir"]+"fastqc/{run}_{read}_trimmed_fastqc.html", run=runs, read=reads),
        expand(config["trimmed_dir"]+"fastqc/{run}_{read}_trimmed_fastqc.zip", run=runs, read=reads)


# download fastq files using list of run accessions
rule download_fastq:
    output: config["temp_dir"]+"{run}_1.fastq", config["temp_dir"]+"{run}_2.fastq"
    log: config["log_dir"]+"download_fastq/"+"{run}_1", config["log_dir"]+"download_fastq/"+"{run}_2"
    threads: 8
    conda: config["dl_qc_env_path"]
    shell:
        "fasterq-dump {wildcards.run} --split-files -e 8 -O {config[temp_dir]} -t {config[temp_dir]}"
# cite: https://github.com/ncbi/sra-tools

# adapter list from: https://github.com/stephenturner/adapters/blob/master/adapters_combined_256_unique.fasta
# can move adapter list to config file later
rule trimmomatic_pe:
    input:
        r1=config["temp_dir"]+"{run}_1.fastq",
        r2=config["temp_dir"]+"{run}_2.fastq"
    output:
        r1=config["trimmed_dir"]+"trimmed/{run}_1_trimmed.fastq",
        r2=config["trimmed_dir"]+"trimmed/{run}_2_trimmed.fastq",
        # reads where trimming entirely removed the mate
        r1_unpaired=config["trimmed_dir"]+"unpaired/{run}_1_trimmed.unpaired.fastq",
        r2_unpaired=config["trimmed_dir"]+"unpaired/{run}_2_trimmed.unpaired.fastq"
    log:
        config["log_dir"]+"trimmomatic/{run}.log"
    params:
        # list of trimmers (see manual)
        trimmer=[f"ILLUMINACLIP:'{adapter_list}':2:30:10:2:true SLIDINGWINDOW:4:20 MINLEN:15"], 
        # optional parameters
        extra="-phred33"
    threads: 8
    wrapper:
        "0.38.0/bio/trimmomatic/pe"

# take a look to see if adapter trimming and quality filtering looks ok
rule fastqc:
    input:
        config["trimmed_dir"]+"trimmed/{run}_{read}_trimmed.fastq"
    output:
        html=config["trimmed_dir"]+"fastqc/{run}_{read}_trimmed_fastqc.html",
        zip=config["trimmed_dir"]+"fastqc/{run}_{read}_trimmed_fastqc.zip" # the suffix _fastqc.zip is necessary for multiqc to find the file
    params: ""
    threads: 8
    log:
        config["log_dir"]+"fastqc/{run}_{read}.log"
    wrapper:
        "0.38.0/bio/fastqc"
