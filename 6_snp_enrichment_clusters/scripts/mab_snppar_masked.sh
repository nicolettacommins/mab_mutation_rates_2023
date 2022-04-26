#!/bin/bash
#SBATCH --mem=10G
#SBATCH -t 4-00:00
#SBATCH -p medium
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mab_snppar_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mab_snppar_%j.err

#input 
alignment="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/mab_masked_snpAln_unwrapped.fasta"
snp_list="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/mab_masked_snp_positions.txt"
tree='/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/working_trees/mab/mab_upid_dropped_outgroup_and_outlier_distance_rooted.tree'
gbk='/n/data1/hms/dbmi/farhat/nikki/abscessus/references/GCF_000069185.1/GCF_000069185.1_full.gb'
#output
out_dir="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/snppar_output/mab_recombinationFree/"
prefix="mab_recombFree_snppar_"

snppar -m $alignment -l $snp_list -t $tree -g $gbk -d $out_dir -p $prefix -A