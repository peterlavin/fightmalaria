#! usr/bin/env python

#===============================================================================
# Class object represents data from a result line
#===============================================================================
import os, sys
sys.path.append('../commonlibs')
import DBaseUtils

class LigLine:

    def __init__(self, curDB, prot_str, lig, this_sc):
        self.cursorDB = curDB
        self.prot_name = prot_str
        self.ligand = lig
        self.this_score = this_sc


    def insert_new_result(self):
        insert_success = False
        cursorDB = self.cursorDB
        prot_name = self.prot_name
        score = self.this_score
        ligand = self.ligand
        
        try:
            sql_stm = "INSERT INTO fightmalaria.tbl_" + prot_name + "_results (ligand, score_1) VALUES ('" + \
            str(ligand) + "', '" + str(score) + "');"
            DBaseUtils.execute_sql_void(cursorDB, sql_stm)
            print 'Score', score, 'for ligand', ligand, 'inserted in database.' 
            insert_success = True
        except(IOError, OSError, MySQLdb.Error, e):
            print "Error %d: %s" % (e.args[0], e.args[1])
            #TODO: write to log file here
            print 'Error inserting new ligand results in database.'
            insert_success = False

        return insert_success


    def update_existing_lig(self, which_score):
        update_success = False
        cursorDB = self.cursorDB
        prot_name = self.prot_name
        score = self.this_score
        ligand = self.ligand

        try:
            sql_stm = "Update fightmalaria.tbl_" + prot_name + "_results SET " + \
            which_score + " = " + str(score) + " WHERE ligand = '" + str(ligand) + "';"
            result_1 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
            print 'Score', score, 'for ligand', ligand, 'updated in database.'
            update_success = True
        except(IOError, OSError, MySQLdb.Error, e):
            print "Error %d: %s" % (e.args[0], e.args[1])
            print 'Error updating existing ligand results in database'
            update_success = False
                
        return update_success


    def determine_if_new_lig(self):
        ''' SQL stm to determine if there is already a score for this ligand in res tbl '''
        existing_lig = False
        cursorDB = self.cursorDB
        ligand = self.ligand
        prot_name = self.prot_name
        
        try:
            sql_stm = "SELECT ligand FROM fightmalaria.tbl_" + prot_name + \
            "_results WHERE ligand = '" + str(ligand) + "' LIMIT 1;"
            result_1 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
        except(IOError, OSError, MySQLdb.Error, e):
            print "Error %d: %s" % (e.args[0], e.args[1])            
        
        if result_1 == None:
            existing_lig = False
        else:
            existing_lig = True
        
        return existing_lig


    def determine_which_score_update(self):
        which_score = 'score_aux'
        cursorDB = self.cursorDB
        prot_name = self.prot_name
        ligand = self.ligand
        
        try:
            sql_stm = "SELECT score_1, score_2 FROM fightmalaria.tbl_" + prot_name + "_results WHERE ligand = '" + str(ligand) + "';"
            result_1 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
            score_1 = result_1[0]
            score_2 = result_1[1]
                
            if (result_1[0] != None and result_1[1] == None):
                which_score = 'score_2'
            elif (result_1[0] == None and result_1[1] != None):
                which_score = 'score_1'
            elif (result_1[0] != 'None' and result_1[1] != 'None'):
                which_score = 'score_aux'
            
            return which_score
        except(IOError, OSError, MySQLdb.Error, e):
            print "Error %d: %s" % (e.args[0], e.args[1])
            #TODO: write to log file here
            print 'Error getting which_score decision from database.'
            return 'score_aux'
        
