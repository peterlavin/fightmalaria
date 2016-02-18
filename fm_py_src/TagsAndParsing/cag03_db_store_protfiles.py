#! usr/bin/env python
import os, time
from os import listdir
import MySQLdb, _mysql
# Inserts protein mol and tmb files to dbase

startTime = time.time()
print 'Start time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

mol_source_dir = '/home/lavinp/fightmalaria/prot_files/ascii_files/'
tmb_source_dir = '/home/lavinp/fightmalaria/prot_files/tmb_files/'


mol_dirlist = listdir(mol_source_dir)

# interate over single mol files
for i in range(0,len(mol_dirlist)):
	inc = str(i + 1)
	filename = mol_dirlist[i]
	prot_name = mol_dirlist[i][0:4]
	print prot_name, 'In mol loop'


	stm1 = "INSERT INTO fightmalaria.tbl_prot_list (id, prot_name, comment, status) VALUES ('"  + inc + "', '" + prot_name + "', 'From UI', '0');"
	cHandler.execute(stm1)
	
tmb_dirlist = listdir(tmb_source_dir)
                                                                                                                        
# interate over single mol files
for entry in tmb_dirlist:
        filename = entry
        prot_name = entry[0:4]
        print prot_name, 'In tmb loop'
        binfile = open(tmb_source_dir + filename, 'rb')
                                                                                                                        
        stm1 ="UPDATE fightmalaria.tbl_prot_list SET tmbfile = '" + _mysql.escape_string(binfile.read()) + "' WHERE prot_name LIKE '" + prot_name + "';"
        
        cHandler.execute(stm1)
        binfile.close()



stm3 = "SELECT COUNT(tmbfile) FROM fightmalaria.tbl_prot_list"
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



