#! /usr/bin/env python

#===============================================================================
# Receives a result file object and processes each line in it.
#===============================================================================
import os, sys, linecache
sys.path.append('../commonlibs')
import DBaseUtils, ProtLineProcess, LigandLineProcess
from ProtLineProcess import ProtLine
from LigandLineProcess import LigLine

class ResultFileProcess:
    
    def __init__(self, file):
        self.fileObj = file
    
    
    def ParseResFile(self):
        file_processed = False
        
        ''' creating database objects '''
        conDB = DBaseUtils.create_conn()
        cursorDB = DBaseUtils.create_cursor(conDB)
        current_file = self.fileObj
        prot_name = ''
        
        for line in current_file:
	    if line[0:9] == ' ' or line[0:9] == '\n' or line[0:1] == '':
	       file_processed = True
	       break	
            elif line[0:9] == ('Receptor:'):
               prot_name = line[9:15]
               prot_name = prot_name.rstrip(' ')
               prot_name = prot_name.rstrip('\n')
               prot_name = prot_name.lstrip(' ')
               protln = ProtLine(prot_name)
               ''' check for existance in database here '''
               prot_exists = protln.verify_receptor(cursorDB)
               if prot_exists == False:
                   file_processed = False
                   ''' Break here to abort if first line is not a valid receptor name '''
                   break
            elif line[0:9] != ('Receptor:'):
               '''if stm to catch empty line at end of file ''' 
	       score = line[0:6]               
	       score = score.rstrip(' ')  
	       pos = line.rfind('Name: ')	
	       ligand = line[pos+5:]
               ligand = str(ligand)
               ligand = ligand.rstrip('\n') 
               ligand = ligand.rstrip(';')
               ligand = ligand.lstrip(' ')
               ligand = ligand[-12:]
	       ligand = int(ligand)
	
	       ligln = LigLine(cursorDB, prot_name, ligand, score)
               new_lig_res = ligln.determine_if_new_lig()
	                                     
               if (new_lig_res == False):
             	file_processed = ligln.insert_new_result()
               else:
              	which_score = ligln.determine_which_score_update()
              	file_processed = ligln.update_existing_lig(which_score)
        
               
        DBaseUtils.close_cursor(cursorDB)
        DBaseUtils.close_conn(conDB)
        return file_processed
