#!/bin/bash
#SBATCH --mem=10G
#SBATCH -t 2-00:00
#SBATCH -p medium
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/bol_snppar_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/logs/bol_snppar_%j.err

#input 
alignment="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/bol_masked_snpAln_unwrapped.fasta"
snp_list="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/vars/bol_masked_snp_positions.txt"
tree='/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/working_trees/bol/bol_iqtree_noOutgroup_ROOTED.tree'
gbk='/n/data1/hms/dbmi/farhat/nikki/abscessus/references/GCF_003609715.1/GCF_003609715.1_full.gb'
#output
out_dir="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/010_homoplasy/snppar_output/bol_allSnp/"
prefix="bol_recombination_free_snppar_"

snppar -m $alignment -l $snp_list -t $tree -g $gbk -d $out_dir -p $prefix -A