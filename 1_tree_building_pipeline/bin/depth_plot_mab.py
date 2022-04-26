import itertools
import csv
import pickle

chrom_length=5067172
mab = [line.rstrip('\n') for line in open('subsp_assign/mab.txt')]

depth=[0]*chrom_length
for sample in mab:
	filepath = 'results/{}/depth/{}.depth'.format(sample,sample)
	with open(filepath, "r") as file:
		reader = csv.reader(file, delimiter='\t')
		for row in itertools.islice(reader, chrom_length):
			if int(row[2])>20:
				depth[int(row[1])-1]=depth[int(row[1])-1]+1

with open('mabdepth.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(depth, filehandle)













# #this works but is slow and not appropriate for large/many files

# import pandas as pd
# mab = [line.rstrip('\n') for line in open('subsp_assign/mab.txt')]

# file0=pd.read_csv('results/{}/depth/{}.depth'.format(mab[0],mab[0]), sep='\t', header=None)
# file0=file0.rename({0: 'chromosome', 1: 'position', 2: mab[0]}, axis='columns')

# for sample in mab[1:]:
# 	file = pd.read_csv('results/{}/depth/{}.depth'.format(sample,sample), sep='\t', header=None)
# 	file=file.rename({0: 'chromosome', 1: 'position', 2: sample}, axis='columns')
# 	file0=file0.merge(file, how='outer', on=['position', 'chromosome'])

# 	del file
# file0.to_csv('mab_table_test.txt', sep='\t', index=False)

# file0.iloc[:,2:]=file0.iloc[:,2:]>20
# file0['sum']=file0.iloc[:,2:].sum(axis=1)
# file0.to_csv('mab_table_sum.txt', sep='\t', index=False)

