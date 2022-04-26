#!/bin/bash
#SBATCH --mem=500
#SBATCH -t 0-11:59:00
#SBATCH -p short
#SBATCH --mail-type=ALL
#SBATCH -o /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/014-2_tree_simulation_msprime/E08_simulate_real_Ne/logs/sim_pop_sizes_%j.out
#SBATCH -e /n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/014-2_tree_simulation_msprime/E08_simulate_real_Ne/logs/sim_pop_sizes_%j.err  

echo "Starting simulation for total pop size $1, subpop size $2, mutation rate change $3"
out_dir="/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/014-2_tree_simulation_msprime/E08_simulate_real_Ne/simulations/03_test_range_pop_sizes/total_pop_$1/subpop_$2/mut_fold_change_$3"

mkdir -p $out_dir

python3 ./scripts/sim_mut_rate_change_NEW.py --n 1000 --init_N $1 --subpop_N $2 --mut_rate 1e-9 --mut_fold_change $3 --seed 1234 --seq_length 5000000 \
--out_dir $out_dir