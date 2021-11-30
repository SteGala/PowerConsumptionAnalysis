#!/bin/bash
hostname=$(hostname)

while sleep 1
do
    powertop --time=10 --csv=output_cpu_power.csv -q
    usage=$(cat output_cpu_power.csv | grep "The system baseline power is estimated at:" | cut -d " " -f 9)

    usage_metric="scraper_cpu_usage_power{hostname=\"${hostname}\"} ${usage}"$'\n'
    
    curl -X POST -H  "Content-Type: text/plain" --data "$usage_metric" http://localhost:9091/metrics/job/top/instance/machine

    echo $(date)
done