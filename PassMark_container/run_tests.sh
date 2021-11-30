#!/bin/bash

test_iteration=10

thread=$(nproc --all)
echo "Detected $thread thread(s)"

step=$(echo "scale=3;$thread/$test_iteration" | bc)
echo "Testing with CPU step increase of $step"