#! usr/bin/env python

###########################################################################
# Creates tar/zipped work units of files for passing to agents            #
###########################################################################
import sys
sys.path.append('../commonlibs')
import os, time, DBaseUtils, tarfile, pexpect
from os import chdir

def create_wu(cursorDB,prot_name,b_file, flag, tarfile_dir):
    ''' getting prot and b_file from database '''
    try:
        sql_stm = "SELECT file FROM fightmalaria.tbl_prot_list WHERE prot_name LIKE '" + prot_name + "';"
        result_4 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
        
        full_b_filename = 'b_' + str(b_file) + '_00.sdf'
        sql_stm = "SELECT b_file FROM fightmalaria.tbl_b100files WHERE filename LIKE '" + full_b_filename + "';"
        result_5 = DBaseUtils.execute_sql_ret_one(cursorDB, sql_stm)
    except:
        #TODO: write to log file here
        print 'Error getting prot & ligand files form database.'
        return False
    try:
        ''' writing prot_name file '''
	os.chdir(tarfile_dir)
        pf = open(prot_name, 'w')
	file_string = str(result_4[0])
	pf.write(file_string)
        pf.close()
    except IOError:
        print 'Error opening prot file'
        return False
            
    try:
        ''' writing b_xx file '''
        lf = open('b_' + str(b_file) + '_00', 'w')
        lf.write(result_5[0])
        lf.close()
    except:
        print 'Error opening lig file'
        return False
 
    try: 
        tar_filename = prot_name + '_' + 'b_' + str(b_file) + '_' + flag + '.tar.gz'
        b_filename = 'b_' + str(b_file) + '_00'
        tar = tarfile.open(tar_filename, "w:gz")
        tar.add(prot_name)
        tar.add(b_filename)
        tar.close()
        #TODO: remove print prot_name + '_' + 'b_' + str(b_file) + '_' + flag + '.tar.gz files created; ',

    except:
        print 'Error making tar.gz file'
        return False
    try:
        os.remove('./' + prot_name)
        os.remove('./' + b_filename)
        #TODO: remove print 'Files', prot_name, '&', b_filename, 'removed. '
    except:
        print 'Error removing file'
        return False
   
    return True
  
