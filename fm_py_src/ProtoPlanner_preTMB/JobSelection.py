#! usr/bin/env python

###########################################################################
# Methods to select next job from tbl_prot_list and tbl_'name'_jobs       #
###########################################################################

import sys
sys.path.append('../commonlibs')
import DBaseUtils

def select_next_prot(cursorDB):
    sql_stm = "SELECT id, prot_name, status FROM fightmalaria.tbl_prot_list " + \
    "WHERE id = (select min(id) FROM fightmalaria.tbl_prot_list WHERE status = 0);"
    result_1 = DBaseUtils.execute_sql_ret_one(cursorDB,sql_stm)
    
    return result_1

def select_next_job(cursorDB, prot_name):
    sql_stm = "SELECT id, b_file, start_1, start_2 FROM fightmalaria.tbl_" + \
    prot_name + "_jobs WHERE id = (SELECT MIN(id) FROM fightmalaria.tbl_" + \
    prot_name + "_jobs WHERE start_1 = '0' OR start_2 = '0');"
    result_2 = DBaseUtils.execute_sql_ret_one(cursorDB,sql_stm)
    
    return result_2

def update_start_status(cursorDB,job_id, prot_name, start_1, start_2):
    ''' method to update start status of jobs in tbl_'prot'_jobs '''
    if start_1 == 0 and start_2 == 0:
        sql_stm = "UPDATE fightmalaria.tbl_" + prot_name + \
        "_jobs SET start_1 = 1 WHERE id = '" + job_id + "';"
        DBaseUtils.execute_sql_void(cursorDB, sql_stm)
    elif start_1 == 1 and start_2 == 0:
        sql_stm = "UPDATE fightmalaria.tbl_" + prot_name + \
        "_jobs SET start_2 = 1 WHERE id = '" + job_id + "';"
        DBaseUtils.execute_sql_void(cursorDB, sql_stm)
    elif start_1 == 0 and start_2 == 1:
        sql_stm = "UPDATE fightmalaria.tbl_" + prot_name + \
        "_jobs SET start_1 = 1 WHERE id = '" + job_id + "';"
        DBaseUtils.execute_sql_void(cursorDB, sql_stm)

def determine_job_flag(start_1, start_2):
    ''' method to determine if tar.gz filename is named first or second job submission ''' 
    name_flag = 'x'
    if start_1 == 0 and start_2 == 0:
        name_flag = 'a'
    elif start_1 == 1 and start_2 == 0:
        name_flag = 'b'
    elif start_1 == 0 and start_2 == 1:
        name_flag = 'z'
       
    return name_flag
