import itertools
import csv
import pickle

chrom_length=4978382
mas = [line.rstrip('\n') for line in open('subsp_assign/mas.txt')]

depth=[0]*chrom_length
for sample in mas:
	filepath = 'results/{}/depth/{}.depth'.format(sample,sample)
	with open(filepath, "r") as file:
		reader = csv.reader(file, delimiter='\t')
		for row in itertools.islice(reader, chrom_length):
			if int(row[2])>20:
				depth[int(row[1])-1]=depth[int(row[1])-1]+1
	print("Counted {}.".format(sample))


with open('masdepth.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(depth, filehandle)


