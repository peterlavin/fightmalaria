#! usr/bin/env python
import os, time
from os import listdir
import MySQLdb

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
	file = open(source_dir + filename, 'rb')
	ligand = file.read()
	file.close()
	inc = str(i)
	stm1 ="INSERT INTO fightmalaria.tbl_ligfiles (id, sdf_file, comment) VALUES (" + inc + ",'" + ligand + "', 'Has smi')"
	cHandler.execute(stm1)
	
stm3 = "SELECT COUNT(sdf_file) FROM fightmalaria.tbl_ligfiles"
cHandler.execute(stm3)
res = cHandler.fetchone()
for i in res:
	oPut = i
print oPut, 'files in database' # debug code

cHandler.close()
myDB.close()

endTime = time.time()
diff = endTime - startTime
print 'Time taken:',diff
