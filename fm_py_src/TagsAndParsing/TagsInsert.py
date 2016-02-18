#! usr/bin/env python

import os, sys, linecache
from os import listdir
from openeye.oechem import *

path_to_orig_files = '/home/lavinp/fightmalaria/ligand_files/individuals/'
path_to_smi_files = '/home/lavinp/fightmalaria/ligand_files/smi_indiv/'

filelist = listdir(path_to_orig_files)

def format_filename(num):
	i = num
	formatted_num = '%(#)0012i' % \
	{"#": i}
	return formatted_num

i = 1
for entry in filelist:
	# reading line 1, composing fm_ligand_name
	name_line = linecache.getline(path_to_orig_files + entry, 1)
	name_line = name_line.strip(' ')
	name_line = name_line.strip('\n')
	fm_ligand_name = name_line + '_' + format_filename(i)
	print fm_ligand_name
	
	# creating input and output streams
	ifs = oemolistream()
	ifs.open(path_to_orig_files + entry)

	ofs = oemolostream()
	ofs.open(path_to_smi_files + entry)

	for mol in ifs.GetOEGraphMols():
		# adding SMILES string
		OESetSDData(mol, "$SMI", OECreateCanSmiString(mol))
		
		# adding fm_tagname tags
		OESetSDData(mol, "fm_tagname", fm_ligand_name)

		# writing modified molecule to output stream
		OEWriteMolecule(ofs, mol)
	
	i = i + 1
	ofs.close()
	ifs.close()

