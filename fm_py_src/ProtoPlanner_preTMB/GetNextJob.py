#! usr/bin/env python

###########################################################################
# Selects next job where either start_1 and -2 are = 0 form tbl_prot_jobs #
###########################################################################
import sys
sys.path.append('../commonlibs')
import os, time, DBaseUtils, JobSelection, WorkUnit, FileTransfer, ConfigParser
from os import listdir

def main():
    success_wu = False
    ''' Getting destinations for storing tar.gz files '''

    tarfile_dir = ''
    server = ''
    server_tmp = ''
    tag_name = ''
    config = ConfigParser.ConfigParser()

    try:
	config.read('/home/fightm/fightmalaria/fm_py_src/config/fm_parameters.cfg')
        tarfile_dir = config.get('planner_folders_path','tarfile_dir')
        server = config.get('planner_folders_path','server')
        server_tmp = config.get('planner_folders_path','server_tmp')
        tag_name = config.get('planner_folders_path','tag_name')
    except IOError:
	 print 'Error accessing fm_parameters.cfg file'
    
    server_tmp = server + ':' +  server_tmp
       
    conDB = DBaseUtils.create_conn()
    cursorDB = DBaseUtils.create_cursor(conDB)

    ''' Selecting id num and name of the first protein for which screen is not complete'''
    result_1 = JobSelection.select_next_prot(cursorDB)
    prot_id = str(result_1[0])
    prot_name = str(result_1[1])
    
    '''Using above result_1, select b_file and status from jobs list for that particular protein '''
    result_2 = JobSelection.select_next_job(cursorDB, prot_name)
    job_id = str(result_2[0])
    b_file = result_2[1]
    start_1 = result_2[2]
    start_2 = result_2[3]
    
    ''' Determining flag for tar.gz filename to indicate first or second job submission '''
    filename_flag = JobSelection.determine_job_flag(start_1, start_2)
    
    ''' Creating work unit files in a temp dir'''
    success_wu = WorkUnit.create_wu(cursorDB,prot_name,b_file, filename_flag, tarfile_dir)
  
    ''' Updating job as start_1 or _2 = True in database if tar.gz file make is successful '''
    if success_wu == False:
        print 'Error, False reutrned from work unit tar.gz file creation.'
        FileTransfer.local_files_remove(tarfile_dir)
        DBaseUtils.close_cursor(cursorDB)
        DBaseUtils.close_conn(conDB)
        sys.exit(main())
    #TODO: #log error
    
    ''' Send work-unit to BOINC and remove tar.gz file. Cmd_str is build in
    FileTransfer as file-exists check is carried out.  '''
    success_wu = FileTransfer.boinc_file_copy(tarfile_dir, server_tmp)

    ''' Move file to download dir on BOINC server ''' 
    cmd_1 = 'ssh ' + server
    tar_filename = prot_name + '_b_' + str(b_file) + '_' + filename_flag + '.tar.gz'
    arg_1 = '\'./proto/move_file ' + tar_filename + '\'' 
    
    cmd_str_1 = '\"\"' + cmd_1 + ' ' + arg_1 + '\"\"'
    success_wu = True # FileTransfer.boinc_invoke_cmd(cmd_str_1) ### neutered for test
    
    if success_wu == False:
        FileTransfer.local_files_remove(tarfile_dir)
        DBaseUtils.close_cursor(cursorDB)
        DBaseUtils.close_conn(conDB)
        sys.exit(main())
   
    ''' Invoke/submit cli cmd(s) on BOINC server '''
    cmd_2 = 'ssh ' + server
    b_filename = 'b_' + str(b_file) + '_00'
    wu_name = tar_filename[:-7]

    arg_2 = '\'cd proto; pwd; ./gen ' + b_filename + ' ' + prot_name + ' ' + \
    tag_name + ' ' + tar_filename + ' ' + wu_name + '\''    
    
    cmd_str_2 = '\"\"' + cmd_2 + ' ' + arg_2 + '\"\"'
    success_wu = True  # FileTransfer.boinc_invoke_cmd(cmd_str_2) ###### neutered for test 
  
    if success_wu == True:
        ''' Updates tbl_<prot_name>_jobs entry as job status as sent '''
        JobSelection.update_start_status(cursorDB,job_id,prot_name,start_1,start_2)
             
    ''' Close database objects, remove all remaining files ''' 
    FileTransfer.local_files_remove(tarfile_dir)
    DBaseUtils.close_cursor(cursorDB)
    DBaseUtils.close_conn(conDB)
   
