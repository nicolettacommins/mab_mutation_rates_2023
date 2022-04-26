#!/bin/bash
#SBATCH --mem=5G
#SBATCH -t 2-00:00
#SBATCH -p medium
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mfasta_test_snppar_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mfasta_test_snppar_%j.err

#input 
alignment="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/analysis/snppar_troubleshooting/toy_aln.fasta"
snp_list="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/analysis/snppar_troubleshooting/toy_snp_pos.txt"
tree='/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/working_trees/mab/mab_upid_dropped_outgroup_and_outlier_distance_rooted.tree'
gbk='/n/data1/hms/dbmi/farhat/nikki/abscessus/references/GCF_000069185.1/GCF_000069185.1_full.gb'
#output
out_dir="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/analysis/snppar_troubleshooting/20210702_no_clean"
prefix="snppar_test_MFASTA"

snppar -m $alignment -l $snp_list -t $tree -g $gbk -d $out_dir -p $prefix -A --no_clean_up