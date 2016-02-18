#! usr/bin/env python

#===============================================================================
# Class object represents data from a protein name line
#===============================================================================
import os, sys
sys.path.append('../commonlibs')
import DBaseUtils

class ProtLine:

    def __init__(self, prot_name):
        self.prot_string = prot_name
        
        
    def verify_receptor(self, cursorDB):
        is_valid_receptor = False
        prot_name = self.prot_string

        try:
            sql_stm = "SELECT prot_name FROM fightmalaria.tbl_prot_list WHERE prot_name LIKE '" + prot_name + "';"
            result_1 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
            if result_1[0] == prot_name:
                is_valid_receptor = True    
        except:
            #TODO: write to log file here
            print 'Error verfiying prot name in database.'
            is_valid_receptor = False

        return is_valid_receptor
