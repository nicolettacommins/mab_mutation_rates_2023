#!/bin/bash
#SBATCH --mem=100
#SBATCH -t 0-01:00:00
#SBATCH -p short
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/014_tree_simulation_msprime/E08_simulate_real_Ne/logs/sim_pop_sizes_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/014_tree_simulation_msprime/E08_simulate_real_Ne/logs/sim_pop_sizes_%j.err  

for j in 3000 8000 14000 26000 57000 #large subpop size
do
	for k in 718 143 71 14 #small subpop size
	do
		for i in 1 #mutation rate change
		do
			sbatch ./scripts/20211111_test_real_Ne_caller_loopPopSizes2.sh $j $k $i
		done
	done
done
