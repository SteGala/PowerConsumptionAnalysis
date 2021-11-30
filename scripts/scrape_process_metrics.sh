#!/bin/bash
hostname=$(hostname)

while sleep 5
do
    cmd=$(ps -eo pid,pcpu,pmem,comm | tail -n +2)
    cpu=""
    mem=""
    while read z
    do
    process=$(echo $z | cut -d " " -f 4)
    pid=$(echo $z | cut -d " " -f 1)
    pcpu=$(echo $z | cut -d " " -f 2)
    pmem=$(echo $z | cut -d " " -f 3)

    cpu="${cpu}scraper_cpu_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pcpu}"$'\n'
    mem="${mem}scraper_memory_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pmem}"$'\n'
    done <<< "$cmd"
    
    curl -X POST -H  "Content-Type: text/plain" --data "$cpu" http://localhost:9091/metrics/job/top/instance/machine
    curl -X POST -H  "Content-Type: text/plain" --data "$mem" http://localhost:9091/metrics/job/top/instance/machine

    echo $(date)
done
