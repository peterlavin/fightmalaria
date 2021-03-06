#! usr/bin/env python
#===============================================================================
# Calls methods to query database to get work units.
#===============================================================================

import sys, threading, thread, time, GetNextJob

interval = 0
min_interval = 30

if len(sys.argv) > 1:
    print sys.argv[1], 'sec passed as time interval.'
    if sys.argv[1] > 30:
	interval = float(sys.argv[1])
    else:
	interval = min_interval
	print 'Interval set at minimun value of', min_interval, 'sec'
else:
    interval = min_interval
    print 'No interval argument passed in, defaulting to', interval, 'sec'

class GetJobs(threading.Thread):

    def run(self):        
        # check status of SGA/PGA, not needed here.
        agent = True
        
        if agent == True:
            # call methods to get work units
            GetNextJob.main()
            
if __name__=="__main__":

    while True:
	GetJobs().start()
        time.sleep(interval)
   
