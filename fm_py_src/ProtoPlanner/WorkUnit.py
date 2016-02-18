#! usr/bin/env python

###########################################################################
# Creates tar/zipped work units of files for passing to agents            #
###########################################################################
import sys
sys.path.append('../commonlibs')
import os, time, DBaseUtils, tarfile, pexpect
from os import chdir

prot_filename = ''
b_filename = ''

def create_wu(cursorDB,prot_name,b_file, flag, tarfile_dir):
    ''' getting prot and b_file from database '''
    try:
	prot_filename = prot_name + '.tmb'
	sql_stm = "SELECT tmbfile FROM fightmalaria.tbl_prot_list WHERE prot_name LIKE '" + prot_name + "';"
        result_4 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
        
        full_b_filename = 'b_' + str(b_file) + '_00.tmb' # this line and SQL stms change for tmb

	filename_sdf = 'b_' + str(b_file) + '_00.sdf'
        sql_stm = "SELECT tmbfile FROM fightmalaria.tbl_b100files WHERE filename LIKE '" + filename_sdf + "';"
	result_5 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
	print prot_filename, full_b_filename, 'TEST IN WorkUnit.py'
    except:
        #TODO: write to log file here
        print 'Error getting prot & ligand TMB files from database.'
        return False
    try:
        ''' writing prot_name file '''
	os.chdir(tarfile_dir)
        pf = open(prot_filename, 'wb')
	prot_content = result_4[0]
	pf.write(prot_content)
        pf.close()
    except IOError:
        print 'Error opening prot tmb file'
        return False
            
    try:
        ''' writing b_xx tmb file '''
        lf = open(full_b_filename, 'wb')
	lig_content = result_5[0]
        lf.write(lig_content)
        lf.close()
    except IOError:
        print 'Error opening lig file'
        return False
 
    try: 
        tar_filename = prot_name + '_' + 'b_' + str(b_file) + '_' + flag + '.tar.gz'
        b_filename = 'b_' + str(b_file) + '_00'
        tar = tarfile.open(tar_filename, "w:gz")
        tar.add(prot_filename)
        tar.add(full_b_filename)
        tar.close()
        
    except:
        print 'Error making tar.gz file'
        return False
    try:
        os.remove('./' + prot_filename)
        os.remove('./' + full_b_filename)
       
    except:
        print 'Error removing file'
        return False
   
    return True
  
