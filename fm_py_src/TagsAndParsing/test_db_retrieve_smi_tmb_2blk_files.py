#! usr/bin/env python
import os, time
from os import listdir
import MySQLdb, _mysql
##### retrieves one tmb file and make a tmb file to test, aug 23

startTime = time.time()
print 'Start time is:',time.ctime(startTime)

myDB = MySQLdb.connect(host="cagraidsvr03.cs.tcd.ie", port=3306, user="lavinp", passwd="0iFetEkg0e")
cHandler = myDB.cursor()

stm1 ="SELECT tmbfile FROM fightmalaria.tbl_b100files WHERE id = 1;"
cHandler.execute(stm1)
result_1 = cHandler.fetchone()

content = result_1[0]

fn = open('testtmb_onetag.tmb', 'wb')
fn.write(content)
fn.close()

cHandler.close()
myDB.close()

endTime = time.time()
diff = endTime - startTime
print 'Time taken:',diff
