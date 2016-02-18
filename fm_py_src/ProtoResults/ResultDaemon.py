#! usr/bin/env python

#===============================================================================
# Daemon to repeatedly check for returned results files
#===============================================================================

import sys, time, threading, thread, CheckForResults


''' Handling arguments passed in ''' 
interval = 0

if len(sys.argv) > 1:
    interval = float(sys.argv[1])
else:
    interval = 10
    

class GetResults(threading.Thread):

    def run(self):        
        CheckForResults.main()
            
if __name__=="__main__":

    while True:
        GetResults().start()
        time.sleep(interval)
