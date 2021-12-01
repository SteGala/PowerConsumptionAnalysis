#!/bin/bash
touch ./data/cpu_usage
touch ./data/cpu_usage_docker
touch ./data/memory_usage

hostname=$(hostname)
thread=$(nproc --all)

echo "#how to read {pid, name, pcpu}" >> ./data/cpu_usage
echo "#how to read {timestamp, aggregated_cpu}" >> ./data/cpu_usage_docker
echo "#how to read {pid, name, pmem}" >> ./data/memory_usage


while sleep 5
do
    echo "#### $(date +%s)" >> ./data/memory_usage
    echo "#### $(date +%s)" >> ./data/cpu_usage

    #cmd=$(top -b -n2 -d 0.1)  
    #ntask=$(echo "$cmd" | grep "Tasks:" | tail -n 1 | cut -d " " -f 2)
    #taskList=$(echo "$cmd" | tail -n $ntask | gawk '{print $1,$9,$10,$12}')
    
    cmdDocker=$(docker stats --no-stream | grep "passmark_container" | gawk '{print $3}' | cut -d "%" -f 1)
    echo "$(date +%s) $cmdDocker" >> ./data/cpu_usage_docker

    #while read z
    #do
        #process=$(echo $z | cut -d " " -f 4)
        #pid=$(echo $z | cut -d " " -f 1)
        #pcpu=$(echo $z | cut -d " " -f 2)
        #pmem=$(echo $z | cut -d " " -f 3)

        #echo "$pid $process $pcpu" >> ./data/cpu_usage
        #echo "$pid $process $pmem" >> ./data/memory_usage

        #totcpu=$(echo "scale=3;$totcpu+$pcpu" | bc)
        #totram=$(echo "scale=3;$totram+$pmem" | bc)

        #cpu="${cpu}scraper_cpu_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pcpu}"$'\n'
        #mem="${mem}scraper_memory_usage_percentage{process=\"${process}\", pid=\"${pid}\", hostname=\"${hostname}\"} ${pmem}"$'\n'
    #done <<< "$taskList"
    
    #echo "$(date +%s) $(echo "scale=3;$totcpu/$thread" | bc)" >> ../data/cpu_usage
    #echo "$(date +%s) $totcpu" >> ../data/cpu_usage
    #echo "$(date +%s) $totram" >> ../data/memory_usage
    #curl -X POST -H  "Content-Type: text/plain" --data "$cpu" http://localhost:9091/metrics/job/top/instance/machine
    #curl -X POST -H  "Content-Type: text/plain" --data "$mem" http://localhost:9091/metrics/job/top/instance/machine

    #echo $(date)
done
