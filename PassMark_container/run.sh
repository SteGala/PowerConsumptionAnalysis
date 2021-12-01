#!/bin/bash

./pt_linux_x64 -r 1 -d $TESTLEN -i $TESTITERATIONS
#./pt_linux_x64 -r 1 -d 3 -i 5
mv results_cpu.yml "./data/results_cpu_$CURRENTLOAD.yml"