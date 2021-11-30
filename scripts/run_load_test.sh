#!/bin/bash

test_iteration=10

rm ./data/load_events
touch ./data/load_events

thread=$(nproc --all)
echo "Detected $thread thread(s)"

step=$(echo "scale=3;$thread/$test_iteration" | bc)
echo "Testing with CPU step increase of $step"
echo

cpus=$step

while (( $(echo "$cpus <= $thread" | bc -l) ))
do
    # keep track of load events
    echo "$(date +%s) start" >> ./data/load_events
    echo "$cpus" >> ./data/load_events

    echo "Testing with cpu=$cpus"
    docker run 

    # keep track of load events
    echo "$(date +%s) end" >> ./data/load_events

    cpus=$(echo "scale=3;$cpus+$step" | bc)
done