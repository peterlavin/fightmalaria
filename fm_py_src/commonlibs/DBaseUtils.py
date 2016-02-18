#! usr/bin/env python

###########################################################################
# Creates a database connection to fightmalaria on cagraidsvr01           #
# and returns this.                                                       #
###########################################################################
import MySQLdb, sys, string, ConfigParser

def create_conn():
    myDB = None
    pwd = ''
    cfg_passwd_file_addr = ''
    cfg_port = 0
    cfg_user = ''
    cfg_host = ''
    config = ConfigParser.ConfigParser()

    try:
	config.read('/home/lavinp/fightmalaria/fm_py_src/config/fm_parameters.cfg')
	cfg_host = config.get('database','host')
	cfg_port = config.get('database','port')
	cfg_port = int(cfg_port)
	cfg_user = config.get('database','user')
	cfg_passwd_file_addr = config.get('database','passwd_file_addr')
    except IOError:
	print 'Error accessing fm_parameters.cfg file'
    
    try:
        pw_file = open(cfg_passwd_file_addr)
        pwd = pw_file.read()
        pwd = pwd.rstrip('\n')
        pw_file.close()
    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
        print 'Error opening passwd file'
        
    try:
        myDB = MySQLdb.connect(
        host=cfg_host,
        port=cfg_port,
        user=cfg_user,
        passwd=pwd)
        return myDB
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(0)
        
                    
    return myDB


def create_cursor(conn):
    cur = None
    try:
        cur  = conn.cursor()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(0)
    return cur


def close_cursor(cur):
    try:
        cur.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        
    return True


def close_conn(conn):
    try:
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        
    return True


def execute_sql_void(cursor,sql_stm):
    try:
        cursor.execute(sql_stm)

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(0)


def execute_sql_ret_one(cursor,sql_stm):
    try:
        cursor.execute(sql_stm)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit()
    result0_1 = cursor.fetchone()

    return result0_1
