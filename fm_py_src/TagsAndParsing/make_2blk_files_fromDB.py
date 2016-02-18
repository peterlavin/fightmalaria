#! usr/bin/env python

import os, time
import MySQLdb

destdir = '/home/lavinp/fightmalaria/ligand_files/smi_2blks/'

startTime = time.time()
print '\nStart time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

for i in range(1,501):
	# making b filename
	incStr = str(i)
	newf = 'b_' + incStr + '_00.sdf'
	contentBuffer = ''
	stm1_1 = "SELECT b_file FROM fightmalaria.tbl_b100files WHERE filename LIKE '" + newf + "';"
	cHandler.execute(stm1_1)

	result1_1 = cHandler.fetchone()
	contentBuffer = result1_1[0]
	
	# creating actual b_file on HD
	fn = open (destdir + newf, 'w')
	fn.write(contentBuffer)
	fn.close()
	
cHandler.close()
myDB.close()
		
endTime = time.time()
print 'Finish time is:',time.ctime(endTime)
print 'Duration: ',(endTime - startTime)
