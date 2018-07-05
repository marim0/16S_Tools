import pandas as pd
import os
import sys
import logging
from argparse import ArgumentParser
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

argparser = ArgumentParser()
argparser.add_argument('-i', '--input', required=True)
argparser.add_argument('-l', '--level', type=int, required=True)
argparser.add_argument('-o', '--output', required=True)
argparser.add_argument('-m', '--map', required=True)
argparser.add_argument('-d', '--description', required=True)
	
args = argparser.parse_args()
if args.level >= 1 and args.level <= 3:
	LEVEL = args.level
else:
	raise ValueError('Please specify 1,2, or 3.')

ONEORTWO = args.description
MAPFILE = args.map
INPUTFILE = args.input
OUTPUTFILE = args.output

if ONEORTWO == "1":
	df = pd.read_csv(INPUTFILE, sep="\t", header=1)
	df = df.drop("KEGG_Description", axis=1)
elif ONEORTWO == "2":
	df = pd.read_csv(INPUTFILE, sep="\t", header=0)
else:
	raise ValueError('Please specify PICRUSt version.')

logging.info("raw dataframe KO count: " + str(df.shape[0]))
map = pd.read_csv(MAPFILE, sep="\t", header=0)
df = df[df[df.columns[0]].isin(map["KO"])]
logging.info("filtered dataframe KO count: " + str(df.shape[0]))

df = pd.concat([map.set_index("KO"), df.set_index(df.columns[0])], axis=1).dropna()

logging.info("collapsing KEGG_Pathways ...")
update_d = {}

def collapse(x):
	pathways = []
	ps = x.KEGG_Pathways
	if "|" in ps:
		cps = ps.split("|")
		for cp in cps:
			if "." in cp:
				stp = cp.split(".")[0]
				pathways.append(stp.split(";"))
			else:
				pathways.append(cp.split(";"))
	else:
		if "." in ps:
			stp = ps.split(".")[0]
			pathways.append(stp.split(";"))
		else:
			pathways.append(ps.split(";"))

	update_d[x.name] = {"KEGG_Description":x.KEGG_Description, "KEGG_Pathways":pathways}
df.apply(lambda x: collapse(x), axis=1)

logging.info("collapsing to level ...")
df = df.drop(["KEGG_Description", "KEGG_Pathways"], axis=1)
collapseDf = pd.DataFrame()

for ko in df.index:
    subDf = pd.DataFrame(df.loc[ko])
    update = []
    for path in update_d[ko]["KEGG_Pathways"]:
        if len(path)>=LEVEL:
            update.append(path[LEVEL-1])
    for level in update:        
        subDf[level] = subDf[ko]
    subDf = subDf.drop([ko], axis=1).T
    collapseDf = pd.concat([collapseDf, subDf], axis=0)
   
logging.info("concatenating ...")
complete = collapseDf.groupby(collapseDf.index).sum()
logging.info("final dataframe pathway count: " + str(complete.shape[0]))
logging.info("outputting ...")
complete.to_csv(OUTPUTFILE, sep="\t")
