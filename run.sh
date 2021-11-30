#!/bin/bash

rm -f ./data/*

./scripts/scrape_process_metrics.sh &
./scripts/scrape_cpu_power.sh &

sleep 60

./scripts/run_load_test.sh

killall scrape_process_metrics.sh
killall scrape_cpu_power.sh