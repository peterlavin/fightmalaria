#! usr/bin/env python

import os, sys, TagsInsert


def run_process(py_script_name):
	try:
		python TagsInsert.main()
		print 'Completed... ', py_script_name
	except:
		print 'Error in... ', py_script_name + '.py'
		sys.exit()


for script in (['TagsInsert',\
'cag03_db_store_smi_single_files',\
'cag03_db_make_b_smi_files',\
'make_2blk_files_to_hd',\
'tmb_multiple_conv',\
'cag03_store_smi_tmb_2blk_files',\
]):
	run_process(script)

