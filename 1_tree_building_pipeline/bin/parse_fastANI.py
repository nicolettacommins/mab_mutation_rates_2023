import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fastANI_dir", type=str,
                    help="directory containing the fastANI output files")
parser.add_argument("outfile", type=str,
					help="output file")
parser.add_argument("failed", type=str,
					help="store failed samples")
args = parser.parse_args()

# where are the fastANI files
files=os.listdir(args.fastANI_dir)

#initialize a dataframe
dfObj = pd.DataFrame(columns=['sample','GCF_000069185.1', 'GCF_000497265.2', 'GCF_003609715.1'])
failed=[]

for file in files:
	# read in each file
	filepath=os.path.join(args.fastANI_dir, file)
	print(filepath)

	#get the name of the sample from the filename
	sample_name=file.split('.')[0]

	try:
		f=pd.read_csv(filepath, sep='\t', header=None)

		#retrieve the ANI values
		mab=f[f[1].str.contains('GCF_000069185.1')][2].item()
		mas=f[f[1].str.contains('GCF_000497265.2')][2].item()
		bol=f[f[1].str.contains('GCF_003609715.1')][2].item()

		#sort into a dictionary
		data=[{'sample': sample_name, 'GCF_000069185.1': mab, 'GCF_000497265.2': mas, 'GCF_003609715.1': bol}]

		#append to dataframe
		dfObj=dfObj.append(data)

	except:
		print("      - there is a problem with {}. Appending to list.".format(file))
		failed.append(sample_name)

#save data
dfObj.to_csv(args.outfile, sep='\t', index=False)

#save failed
with open(args.failed, 'w') as filehandle:
	for item in failed:
		filehandle.write('%s\n' % item)



