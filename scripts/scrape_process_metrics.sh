#!/bin/bash
touch ./data/cpu_usage
touch ./data/memory_usage

hostname=$(hostname)
thread=$(nproc --all)

echo "#how to read {pid, name, pcpu}" >> ./data/cpu_usage
echo "#how to read {pid, name, pmem}" >> ./data/memory_usage


while sleep 5
do
    echo "#### $(date +%s)" >> ./data/memory_usage
    echo "#### $(date +%s)" >> ./data/cpu_usage
    cmd=$(ps -eo pid,pcpu,pmem,comm --sort -pcpu | tail -n +2)
    cpu=""
    mem=""
    totcpu=0
    totram=0
    while read z
    do
        process=$(echo $z | cut -d " " -f 4)
        pid=$(echo $z | cut -d " " -f 1)
        pcpu=$(echo $z | cut -d " " -f 2)
        pmem=$(echo $z | cut -d " " -f 3)

        echo "$pid $process $pcpu" >> ./data/cpu_usage
        echo "$pid $process $pmem" >> ./data/memory_usage

        totcpu=$(echo "scale=3;$totcpu+$pcpu" | bc)
        totram=$(echo "scale=3;$totram+$pmem" | bc)

        #cpu="${cpu}scraper_cpu_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pcpu}"$'\n'
        #mem="${mem}scraper_memory_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pmem}"$'\n'
    done <<< "$cmd"
    
    #echo "$(date +%s) $(echo "scale=3;$totcpu/$thread" | bc)" >> ../data/cpu_usage
    #echo "$(date +%s) $totcpu" >> ../data/cpu_usage
    #echo "$(date +%s) $totram" >> ../data/memory_usage
    #curl -X POST -H  "Content-Type: text/plain" --data "$cpu" http://localhost:9091/metrics/job/top/instance/machine
    #curl -X POST -H  "Content-Type: text/plain" --data "$mem" http://localhost:9091/metrics/job/top/instance/machine

    #echo $(date)
done
