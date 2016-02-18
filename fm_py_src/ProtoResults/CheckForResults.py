#! usr/bin/env python

#===============================================================================
# Daemon to check for returned results files
#===============================================================================

import os, sys, time, shutil, linecache, ResultFileProcess, ConfigParser, DBaseUtils, FileNameProcess
from os import listdir, path, remove
from ResultFileProcess import ResultFileProcess
from FileNameProcess import FileNameProcess


def main():

    res_store = ''
    res_quarantine = ''
    res_complete = ''
    config = ConfigParser.ConfigParser()

    try:
        config.read('/home/lavinp/fightmalaria/fm_py_src/config/fm_parameters.cfg')
        res_store  = config.get('result_folders_path','res_store')
        res_quarantine = config.get('result_folders_path','res_quarantine')
        res_complete = config.get('result_folders_path','res_complete')
    except IOError:
	print 'Error accessing fm_parameters.cfg file'
	    
    try:
        result_list = listdir(res_store)
    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
        print 'Problem reading files in results directory'
        sys.exit(main())
            
    
    if len(result_list) != 0:
        for i in range(0,len(result_list)):
            file_processed = True
            receptor_line_check_1 = ''
            receptor_line_check_2 = ''
            receptor_line_check_bool = False
            
            try:
                fileObj = open(res_store + result_list[i])
                receptor_line_check_1 = linecache.getline(res_store + result_list[i], 1)[0:9]
                receptor_line_check_2 = linecache.getline(res_store + result_list[i], 2)[0:6]
                receptor_line_check_2 = receptor_line_check_2.strip(' ')
                
                try:  
                    float(receptor_line_check_2)
                    receptor_line_check_bool = True
                except ValueError:
                    receptor_line_check_bool = False

                task = ResultFileProcess(fileObj)
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)
                print 'Error opening results file'
                
            if (receptor_line_check_1 == 'Receptor:' and receptor_line_check_bool == True):
                file_processed = task.ParseResFile()
            else:
                file_processed = False
                            
            if file_processed == True:
                #TODO: log failure of file processing
                try:
                    conDB = DBaseUtils.create_conn()
		    cursorDB = DBaseUtils.create_cursor(conDB)
		    fileNameTask = FileNameProcess(cursorDB,result_list[i])
		    FileNameProcess.update_prot_jobs_tbl(fileNameTask)
		    DBaseUtils.close_cursor(cursorDB)
		    DBaseUtils.close_conn(conDB)

		    shutil.copy(res_store + result_list[i], res_complete + result_list[i])
                    remove(res_store + result_list[i])
                except (IOError, os.error), why:
                    print "Can't copy %s to %s: %s" % (res_store + result_list[i], res_complete + result_list[i], str(why))
                    ''' Exit system here to avoid duplicatng results '''
                    print 'Error removing processes file'
                    sys.exit(main())   
            else:
                #TODO: log failure of file processing
                try:
                    shutil.copy(res_store + result_list[i], res_quarantine)
                    remove(res_store + result_list[i])
                    print ' --- Problem file moved to Quarentine Folder:', time.ctime(time.time()), '---'
                except (IOError, os.error), why:
                    print "Can't copy %s to %s: %s" % (res_store + result_list[i], res_quarantine + result_list[i], str(why))
                    ''' Exit system here to avoid duplicatng results ''' 
                    print 'Error removing unprocessed file to quarantine'
                    sys.exit(main())    
         
            fileObj.close()

    else:
        print ' --- No results found at: ', time.ctime(time.time()), '---'
