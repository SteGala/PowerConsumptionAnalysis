#!/bin/bash

test_iteration=10

touch ./data/load_events

thread=$(nproc --all)
echo "Detected $thread thread(s)"

step=$(echo "scale=3;$thread/$test_iteration" | bc)
echo "Testing with $test_iteration iterations and CPU step increase of $step"
echo

cpus=$step
echo "#how to read {start, load, score, end}" >> ./data/load_events

while (( $(echo "$cpus <= $thread" | bc -l) ))
do
    # keep track of load events
    echo -n "$(date +%s)" >> ./data/load_events
    echo -n " $cpus" >> ./data/load_events

    echo "$(date) start test with CPU=$cpus"

    docker run --name passmark_container -v /home/stefano/Desktop/PowerConsumptionAnalysis/data:/data --cpus=$cpus -e CURRENTLOAD=$cpus -e TESTLEN=4 -e TESTITERATIONS=2 -dit stegala/passmark_container:x86 ./run.sh  > /dev/null
    docker wait passmark_container > /dev/null
    # keep track of load events
    echo -n " $(cat data/results_cpu_$cpus.yml| grep SUMM_CPU | cut -d ":" -f 2)" >> ./data/load_events
    echo " $(date +%s)" >> ./data/load_events

    cpus=$(echo "scale=3;$cpus+$step" | bc)
    docker rm passmark_container > /dev/null
    sleep 60
done