#!/bin/bash

./pt_linux_x64 -r 1
mv results_cpu.yml "./data/results_cpu_$CURRENTLOAD.yml"