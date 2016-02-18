#! usr/bin/env python

#===============================================================================
# Class object represents data from a result file name
#===============================================================================
import os
import DBaseUtils

class FileNameProcess:

    def __init__(self, curDB, res_filename):
        self.cursorDB = curDB
        self.resFname = res_filename    

    def update_prot_jobs_tbl(self):
        cursorDB = self.cursorDB
        res_filename = self.resFname
        
        res_filename = res_filename.lstrip(' ')
        res_filename = res_filename.rstrip(' ')        
        prot_name = res_filename[:4]
 
        b_file = res_filename 
        b_file = b_file[6:]
        b_file = b_file[:-2]
        b_file = b_file.lstrip('_')
        b_file = str(b_file)
      
        if res_filename[-1:] == 'a':
            which_comp = '1'
        if res_filename[-1:] == 'b':
            which_comp = '2'
        if res_filename[-1:] == 'z':
            which_comp = '3'        
        
        if which_comp != '3':
            try:
                sql_stm = "Update fightmalaria.tbl_" + prot_name + "_jobs SET comp_" + \
                which_comp + " = 1 WHERE b_file = '" + b_file + "';"
                result_1 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
                print 'comp_' + which_comp, 'for Protein', prot_name, 'updated in database.'
            except(IOError, OSError, MySQLdb.Error, e):
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    print 'Error updating tbl_prot_jobs in database'
                    
                

