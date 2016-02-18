#!/bin/bash

export PATH=`pwd`/usr/local/bin:$PATH

#
# Added to run openeye OEChem software
PYTHONPATH=`pwd`/usr/local/openeye/wrappers/python/
LD_LIBRARY_PATH=`pwd`/usr/local/openeye/wrappers/libs:$LD_LIBRARY_PATH
export PYTHONPATH
export LD_LIBRARY_PATH

