#!/bin/bash
#SBATCH --mem=10G
#SBATCH -t 2-00:00
#SBATCH -p medium
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mas_snppar_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/mas_snppar_%j.err

#input 
alignment="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/mas_masked_snpAln_unwrapped.fasta"
snp_list="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/mas_masked_snp_positions.txt"
tree='/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/working_trees/mas/mas_iqtree_noOutgroup_ROOTED.tree'
gbk='/n/data1/hms/dbmi/farhat/nikki/abscessus/references/GCF_000497265.2/GCF_000497265.2_full.gb'
#output
out_dir="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/snppar_output/mas_recombinationFree/"
prefix="mas_recombFree_snppar_"

snppar -m $alignment -l $snp_list -t $tree -g $gbk -d $out_dir -p $prefix -A