#! usr/bin/env python

import os, time
import MySQLdb

startTime = time.time()
print '\nStart time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

fileId = 1

for i in range(1,501):
	# making b filename
	inc = i
	incStr = str(inc)
	newf = 'b_' + incStr + '_00.sdf'
	contentBuffer = ''
	for j in range(0,2):
		fileIdStr = str(fileId)
		stm1_1 = "SELECT sdf_file FROM fightmalaria.tbl_ligfiles WHERE id = "+ fileIdStr +";"
		cHandler.execute(stm1_1)
		result1_1 = cHandler.fetchone()
		ligFile = result1_1[0]
		contentBuffer = contentBuffer + ligFile
		fileId = fileId +1
		stm1_2 = "UPDATE fightmalaria.tbl_ligfiles SET b100 = '" + newf + "' WHERE id = "+fileIdStr+";"
		cHandler.execute(stm1_2)
		#cHandler.execute("COMMIT")
	stm2_1 ="INSERT INTO fightmalaria.tbl_b100files (id, b_file, filename, comment) VALUES ("+ incStr +", '" + contentBuffer + "','" + newf + "','SMI x2 blk')"
	cHandler.execute(stm2_1)


cHandler.close()
myDB.close()
		
endTime = time.time()
print 'Finish time is:',time.ctime(endTime)
print 'Duration: ',(endTime - startTime)
