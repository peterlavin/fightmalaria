#! usr/bin/env python

import sys, unittest
sys.path.append('~/fightmalaria/fm_py_src/ProtoPlanner/')
sys.path.append('~/fightmalaria/fm_py_src/ProtoResults/')
sys.path.append('~/fightmalaria/fm_py_src/commonlibs/')
sys.path.append('~/fightmalaria/fm_py_src/ProtoPlanner/')

class ResultsTesting(unittest.TestCase):
 


 def runTest(self):
  assert 1 == 1, 'Failed test'
  print self, 'Test passed - OK'  

