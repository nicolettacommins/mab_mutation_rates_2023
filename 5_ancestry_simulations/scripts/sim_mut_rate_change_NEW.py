import argparse
import msprime
import pandas as pd
import numpy as np
import os
from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from pairsnp import calculate_snp_matrix, calculate_distance_matrix
import pickle
import collections

parser=argparse.ArgumentParser()
parser.add_argument("--n", type=int, help="number of simulations to run")
parser.add_argument("--init_N", type=int, help="effective pop N of the ancestral population")
parser.add_argument("--subpop_N", type=int, help="effective pop N of the subpopulation we are trying to cluster")
parser.add_argument("--mut_rate", type=float, help="mutation rate per generation")
parser.add_argument("--mut_fold_change", type=int, help="mutation rate fold change")
parser.add_argument("--seed", type=int, help="random seed")
parser.add_argument("--seq_length", type=int, help="length of chromosome sequence")
parser.add_argument("--out_dir", type=str, help="parent directory to add set of fasta files")

args=parser.parse_args()


#define functions
def get_snp_mean_metric(d, subpopB, subpopA):
	b=np.array(d)[subpopB,:][:,subpopB]
	np.fill_diagonal(b, np.nan)

	a=np.array(d)[subpopA,:][:,subpopA]
	np.fill_diagonal(a, np.nan)
	
	metric=np.nanmean(b)/np.nanmean(a)
	return np.nanmean(b), np.nanmean(a), metric


################
#### MAIN ######
################

# make sure parent out file exists
if not os.path.exists(args.out_dir):
	os.mkdir(args.out_dir)

# make a subdirectory to hold the fasta files
fasta_dir=os.path.join(args.out_dir, 'fasta')
if not os.path.exists(fasta_dir):
	os.mkdir(fasta_dir)

# define nucleotide substitution model:
model=msprime.GTR(relative_rates=[0.174, 0.988, 0.09264, 0.162, 1, 0.175], equilibrium_frequencies=[0.17, 0.33, 0.33, 0.17])

# get pop Ns:
popC_N=args.init_N
popB_N=args.subpop_N
popA_N=popC_N-popB_N

# get sampling dates:
unclustered_dates_file=open('/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/metadata/dates/unclustered_gen_times', 'rb')
clustered_dates_file=open('/n/data1/hms/dbmi/farhat/nikki/abscessus/0_NOTEBOOKS/metadata/dates/clustA_gen_times', 'rb')
unclustered_dates=pickle.load(unclustered_dates_file)
clustered_dates=pickle.load(clustered_dates_file)

A_samples=[msprime.SampleSet(1, time=i, population="A") for i in unclustered_dates]
B_samples=[msprime.SampleSet(1, time=i, population="B") for i in clustered_dates]
samples=A_samples+B_samples
sample_size=len(samples)

# define demography:
demography = msprime.Demography()
demography.add_population(name="C", initial_size=popC_N)
demography.add_population(name="B", initial_size=popB_N)
demography.add_population(name="A", initial_size=popA_N)
demography.add_population_split(time=50_000, derived=["A", "B"], ancestral="C")

# definte number of replicates:
n=args.n

# run ancestry simulation
print("Simulating ancestries...")
replicates = msprime.sim_ancestry(samples=samples, ploidy=1, num_replicates=n, random_seed=args.seed, sequence_length=args.seq_length, demography=demography)
print("Done simulating ancestries.")

# create empty list to store the mean metric for each replicate
snp_dist_mean_metric_list=[]
b_metric_list=[]
a_metric_list=[]


# for each ancestry simulation, simulate mutations:
print("Simulating mutations...")
for replicate_index, ts in enumerate(replicates):

	# get a list of all the isolates in subpopulation B for this ancestry simulation:
	pop_dict={ts.tables.populations[i].metadata['name']:i for i in [0,1,2]}
	A_pop_number=pop_dict['A']
	B_pop_number=pop_dict['B']
	subpopB_taxa=list(ts.tables.nodes.individual[(ts.tables.nodes.flags==1) & (ts.tables.nodes.population==B_pop_number)])
	subpopA_taxa=list(ts.tables.nodes.individual[(ts.tables.nodes.flags==1) & (ts.tables.nodes.population==A_pop_number)])

	## simulate mutations
	#get target node (common ancestor of subpop B)
	df=pd.DataFrame(list(zip(range(0,len(ts.tables.nodes)), ts.tables.nodes.population, ts.tables.nodes.time)), columns=['node', 'population', 'time'])
	popB_df=df[df.population==B_pop_number]
	target_node=int(popB_df.iloc[popB_df['time'].argmax()].node)

	# get list of subpopB nodes excluding the oldest node
	popB_nodes=list(popB_df.node)
	popB_nodes.remove(target_node)
	popB_nodes

	mtsA = msprime.sim_mutations(ts, rate=args.mut_rate, random_seed=args.seed, model=model)
	mtsB = msprime.sim_mutations(ts, rate=args.mut_rate/args.mut_fold_change, random_seed=args.seed, model=model)
	tables = ts.dump_tables()
	sites_to_add = {}

	# Only keep mutations from pop B nodes for the higher rate
	for site in mtsB.sites():
		mut = site.mutations[0]
		if mut.node in popB_nodes:
			sites_to_add[site.position] = {"ancestral_state": site.ancestral_state,
									   "mut_node": mut.node,
									   "mut_derived_state": mut.derived_state}

	# Only keep mutations from other nodes for the higher rate
	for site in mtsA.sites():
		mut = site.mutations[0]
		if mut.node not in popB_nodes:
			sites_to_add[site.position] = {"ancestral_state": site.ancestral_state,
									   "mut_node": mut.node,
									   "mut_derived_state": mut.derived_state}
	# Add all the mutations to keep, in position-order
	ordered_sites_to_add = collections.OrderedDict(sorted(sites_to_add.items()))
	for site_pos, site_data in ordered_sites_to_add.items():
		site_id = tables.sites.add_row(position=site_pos, ancestral_state=site_data["ancestral_state"])
		tables.mutations.add_row(site=site_id, node=site_data["mut_node"], derived_state=site_data["mut_derived_state"])
	tables.sort()

	## extract variant data:
	mts_pos=[]
	mts_alleles=[]
	mts_genotypes=[]
	for var in tables.tree_sequence().variants():
		mts_pos.append(var.site.position)
		mts_alleles.append(var.alleles)
		mts_genotypes.append(list(var.genotypes))
	
	mts_df=pd.DataFrame({
	'position': mts_pos,
	'mts_alleles': mts_alleles,
	'mts_genotypes': mts_genotypes
	})

	sequences=[[alleles[i] for i in np.array(genotypes)] for alleles, genotypes in zip(mts_df['mts_alleles'], mts_df['mts_genotypes'])]
	genotypes_df=pd.DataFrame(sequences).transpose()

	# write to fasta file:
	fasta_path=os.path.join(fasta_dir,'sim_'+str(replicate_index)+".fasta")

	with(open(fasta_path, "w")) as outfile:
		for row in range(len(genotypes_df)):
			outfile.write(">" + str(row) + "\n" + ''.join(genotypes_df.iloc[row].tolist())+ "\n")

	## read in SNP concatenate and build trees:
	aln=AlignIO.read(fasta_path, "fasta")
	# calculate the distance matrix:
	calculator = DistanceCalculator('identity')
	distMatrix = calculator.get_distance(aln)
	# Create a DistanceTreeConstructor object
	constructor = DistanceTreeConstructor()
	# Construct the phlyogenetic tree using NJ algorithm
	NJTree = constructor.nj(distMatrix)

	# midpoint root the tree:
	NJTree.root_at_midpoint()

	# if subpopB is monophyletic, calculate snp distance metric:
	subpopB_taxa_names=[str(i) for i in subpopB_taxa]
	if NJTree.is_monophyletic([i for i in NJTree.get_terminals() if i.name in subpopB_taxa_names])!=False:
		# get snp distances:
		sparse_matrix, consensus, seq_names = calculate_snp_matrix(fasta_path)
		d = calculate_distance_matrix(sparse_matrix, consensus, "dist", False)

		# get ratio of mean snp distances:
		b_metric, a_metric, snp_dist_mean_metric=get_snp_mean_metric(d, subpopB_taxa, subpopA_taxa)
		print('snp_dist_mean_metric: '+str(snp_dist_mean_metric))
		snp_dist_mean_metric_list.append(snp_dist_mean_metric) 
		b_metric_list.append(b_metric)
		a_metric_list.append(a_metric)

	else:
		print('Tree {} is not monophyletic'.format(replicate_index))


	print('Done with replicate {}'.format(replicate_index))

mean_file_handle=open(os.path.join(args.out_dir,"snp_dist_mean_ratios_"+str(args.mut_fold_change)), "wb")
pickle.dump(snp_dist_mean_metric_list, mean_file_handle)

# b_file_handle=open(os.path.join(args.out_dir,"b_mean_ratios_"+str(args.mut_fold_change)), "wb")
# a_file_handle=open(os.path.join(args.out_dir,"a_mean_ratios_"+str(args.mut_fold_change)), "wb")
# pickle.dump(b_metric_list, b_file_handle)
# pickle.dump(a_metric_list, a_file_handle)



