Snakefile #1 takes a list of Run Accessions and downloads fastq files from NCBI. It trims reads and then runs fastQC on the fastq files.

Notebooks/process_fastqc_drop_contaminants/filter_by_GC_content shows how we used multiqc output to filter isolates with bad %GC content distribution indicative of contamination and rewrote the filtered dataset into a .tsv file that maps BioSample IDs to run accessions (input for snake file #2)

Snakefile #2 combines all runs from the same BioSample into one fastq file and does all the processing for variant calling. 

Notebooks/select_subspecies_cutoffs shows how we evaluated the output of fastANI to create a set of rules for assigning isolates to a subspecies

Notebooks/define_loci_to_include shows how we masked regions of the genome to exclude from analysis 

Snakefile #3 filters vcf files to exclude calls with low quality calls, converts the vcf file to a fasta file, masks fasta files to restrict to high-quality core loci, and combines them into a multiple sequence alignment for input into Gubbins

