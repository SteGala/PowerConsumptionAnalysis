package main

import (
	"log"

	//_ "net/http/pprof"
	"strconv"
	"time"

	infra "github.com/stegala/PowerConsumptionAnalysis/pkg/infrastructure"
	"github.com/stegala/PowerConsumptionAnalysis/pkg/utils"
)

var numberOfInfrastructure = 4
var safeThreadMargin = 0

func main() {
	//go func() {
	//	http.ListenAndServe(":1234", nil)
	//}()
	//currCPU := runtime.NumCPU()
	currCPU := 4
	log.Println("Detected " + strconv.Itoa(currCPU) + " virtual CPUs")

	curTime := int(time.Now().Unix())
	report_path := "./report-" + strconv.Itoa(curTime)
	infrastructures := make([]infra.Infrastructure, 0, numberOfInfrastructure)
	infraChannel := make([]chan bool, 0, numberOfInfrastructure)
	computationStart := make([]bool, 0, numberOfInfrastructure)
	computationEnd := make([]bool, 0, numberOfInfrastructure)

	if err := utils.CreateDirectory(report_path); err != nil {
		log.Fatal(err)
	} else {
		log.Println("Successfully created report directory " + report_path)
	}

	for i := 0; i < numberOfInfrastructure; i++ {
		infrastructures = append(infrastructures, *infra.NewInfrastructure("./example_infrastructures/infrastructure"+strconv.Itoa(i)+".json", report_path))
		computationStart = append(computationStart, false)
		computationEnd = append(computationEnd, false)
		infraChannel = append(infraChannel, make(chan bool))
	}

	runningInstances := 0
	for id, i := range infrastructures {
		if runningInstances >= currCPU-safeThreadMargin {
			for runningInstances >= currCPU-safeThreadMargin {
				for id2, start := range computationStart {
					if start && !computationEnd[id2] {
						select {
						case _, ok := <-infraChannel[id2]:
							if ok {
								log.Printf("Infrastructure %d finished the simulation.\n", id2)
								computationEnd[id2] = true
								runningInstances--
							} else {
								log.Println("Channel closed!")
							}
						default:
						}
					}
				}
				time.Sleep(time.Duration(1) * time.Minute)
			}
		}
		runningInstances++
		computationStart[id] = true
		log.Printf("Infrastructure %d started the simulation.\n", id)
		go i.ComputeOptimizedPlacement(infraChannel[id])
		//time.Sleep(time.Duration(15) * time.Second)
	}

	for id, start := range computationStart {
		if start && !computationEnd[id] {
			<-infraChannel[id]
			log.Printf("Infrastructure %d finished the simulation.\n", id)
			computationEnd[id] = true
		}
	}

	utils.SummarizeReportsConsumption(numberOfInfrastructure, report_path, infrastructures[0].GetSimulationStartTime(), infrastructures[0].GetSimulationEndTime())
	elapsedTime := time.Now().Unix() - int64(curTime)
	log.Printf("Simulation ended in %ds\n", elapsedTime)

}
