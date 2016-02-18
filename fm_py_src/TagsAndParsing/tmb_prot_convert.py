#! usr/bin/env python
# Aug 24
# Code is written only to handle mol2 files

import os, sys
from os import chdir, listdir, path

sourcepath = '/home/lavinp/fightmalaria/prot_files/ascii_files/'
destpath = '/home/lavinp/fightmalaria/prot_files/tmb_files/'

sourcelist = listdir(sourcepath)

for entry in sourcelist:
	infile = sourcepath + entry        
	outfile = destpath + entry[0:4] + '.tmb'
	print infile, outfile, 'conversion'

	os.system('touch ' + outfile)
	
	os.system('/home/lavinp/fightmalaria/ehits_install/eHiTS_6.2/Linux/bin/convert ' + infile + ' ' + outfile  + ' -config /home/lavinp/fightmalaria/ehits_install/eHiTS_6.2/data/parameters.cfg')
	

