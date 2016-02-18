#! usr/bin/env python
# Python script to insert SMILES strings for files to tbl_ligfiles in dbase.
import os, time
from os import listdir
import MySQLdb
from openeye.oechem import *

startTime = time.time()
print 'Start time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

def format_filename(num):
	i = num
	formatted_num = '%(#)0012i' % \
	{"#": i}
	return formatted_num

source_dir = '/home/lavinp/fightmalaria/ligand_files/smi_indiv/'

#make list of dirs in smi single parsed files
smidirlist = listdir(source_dir)

# interate over single smi files
for i in range(1, 1001):
	filename = format_filename(i) + '.sdf'
	print filename, i

	# generating SMILES string
	ifs = oemolistream()
	ifs.open(source_dir + filename)
	for mol in ifs.GetOEGraphMols():
		smi_string =  OECreateCanSmiString(mol)
		print smi_string
	ifs.close()

	inc = str(i)
	stm1 ="UPDATE fightmalaria.tbl_ligfiles SET smi_str = '" + smi_string + "' WHERE id ='" + str(i) + "';"
	cHandler.execute(stm1)

	
stm3 = "SELECT COUNT(smi_str) FROM fightmalaria.tbl_ligfiles"
cHandler.execute(stm3)
res = cHandler.fetchone()
for i in res:
	oPut = i
print oPut, 'SMILES strings in database' # debug code

cHandler.close()
myDB.close()

endTime = time.time()
diff = endTime - startTime
print 'Time taken:',diff
