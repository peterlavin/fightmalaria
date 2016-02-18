#! usr/bin/env python

###########################################################################
# scp and ssh to BOINC server using pexpect module                        #
###########################################################################
import os, sys, pexpect
from os import chdir, getcwd, listdir

def boinc_file_copy(tarfile_dir, server_tmp):
    
    success = False
    tarfile_list = listdir(tarfile_dir)
    ''' precaution to removing files not ending with .tar.gz ''' 
    i = 0
    while i < len(tarfile_list):
        if tarfile_list[i][-7:] != '.tar.gz':
            del tarfile_list[i]
        else:
            i = i + 1
    if len(tarfile_list) == 0:
        print 'No file found in', tarfile_dir
        success = False
        return success
    
    try:
        cmd = 'scp'
        filename = tarfile_list[0]
        st = '\'\'' + cmd + ' ' + filename + ' ' + server_tmp + '\'\'' 
        server_cmd_1 = pexpect.run(st)
        print 'CMD ISSUED:', server_cmd_1
        success = True
        #TODO: need to check for failed scp transfer
    except:
        print 'Error send ing tar.gz file to boinc.'
        return False
        
    return True

def local_files_remove(tarfile_dir):
    ''' removes all files and remnants in working dir '''
    filename = listdir(tarfile_dir)
    for i in range(0, len(filename)):
        os.remove(tarfile_dir + filename[i])
       
def boinc_invoke_cmd(cdm_str):
    success = False
    try:
        ret_string = pexpect.run(cdm_str)
        print 'BOINC RESPONSE:', ret_string
        success = True
        return success
    except:
        print 'Error invoking:', cdm_str, 'on Boinc server.'
        success = False
        
    return success


