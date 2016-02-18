#! usr/bin/env python
import os, time
from os import listdir
import MySQLdb, _mysql

startTime = time.time()
print 'Start time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

source_dir = '/home/lavinp/fightmalaria/ligand_files/smi_tmb_2blks/'

smidirlist = listdir(source_dir)

# interate over single smi files
for entry in smidirlist:
	filename = entry
	dbfile = entry[:-4] + '.sdf'
	print dbfile
	binfile = open(source_dir + filename, 'rb')
	#binfileBuffer = binfile.read()

	stm1 ="UPDATE fightmalaria.tbl_b100files SET tmbfile = '" + _mysql.escape_string(binfile.read()) + "' WHERE filename LIKE '" + dbfile + "';"
	#stm1 = "UPDATE fightmalaria.tbl_b100files SET comment = 'SMI x2 blks' WHERE filename LIKE '" + dbfile + "';"
	cHandler.execute(stm1)
	binfile.close()
	
stm3 = "SELECT COUNT(tmbfile) FROM fightmalaria.tbl_b100files"
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



