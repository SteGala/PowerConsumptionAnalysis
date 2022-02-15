package utils

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

type SchedulingType int64

const (
	Original  SchedulingType = 1
	Basic     SchedulingType = 0
	Optimized SchedulingType = 2
	Enhanced  SchedulingType = 3
)

func (s SchedulingType) String() string {
	switch s {
	case Original:
		return "ORIGINAL"
	case Optimized:
		return "OPTIMIZED"
	case Basic:
		return "BASIC"
	case Enhanced:
		return "ENHANCED"
	default:
		return fmt.Sprintf("%d", int(s))

	}
}

func CreateDirectory(path string) error {
	return os.Mkdir(path, os.ModePerm)
}

func SummarizeReportsConsumption(nInfra int, reportPath string, start time.Time, end time.Time) {
	csvFileConsumption, err := os.Create(reportPath + "/overall_infrastructure_consumption.csv")
	if err != nil {
		log.Fatalf("failed creating file: %s", err)
	}

	csvwriter := csv.NewWriter(csvFileConsumption)

	csvFileConsumptionExcel, err := os.Create(reportPath + "/overall_infrastructure_consumption_excel.csv")
	if err != nil {
		log.Fatalf("failed creating file: %s", err)
	}

	csvwriterExcel := csv.NewWriter(csvFileConsumptionExcel)

	slotCount := 0
	for d := start; !d.After(end); d = d.Add(time.Duration(time.Minute)) {
		slotCount++
	}

	infrastructureConsumption := make([][]string, slotCount)
	infrastructureConsumptionExcel := make([][]string, 4)
	infrastructureConsumption[0] = make([]string, 0, nInfra*4+1)
	infrastructureConsumption[0] = append(infrastructureConsumption[0], "date")

	for i := 1; i < slotCount; i++ {
		infrastructureConsumption[i] = make([]string, 1, nInfra*4+1)
	}

	for i := 0; i < nInfra; i++ {
		infrastructureConsumption[0] = append(infrastructureConsumption[0], "infrastructure"+strconv.Itoa(i)+"-"+Basic.String())
		infrastructureConsumption[0] = append(infrastructureConsumption[0], "infrastructure"+strconv.Itoa(i)+"-"+Original.String())
		infrastructureConsumption[0] = append(infrastructureConsumption[0], "infrastructure"+strconv.Itoa(i)+"-"+Optimized.String())
		infrastructureConsumption[0] = append(infrastructureConsumption[0], "infrastructure"+strconv.Itoa(i)+"-"+Enhanced.String())
	}

	for i := 0; i < 4; i++ {
		infrastructureConsumptionExcel[i] = make([]string, nInfra+1)
		infrastructureConsumptionExcel[i][0] = SchedulingType(i).String()
	}

	for i := 0; i < nInfra; i++ {
		csvConsumptionBasic, err := os.Open(reportPath + "/infrastructure" + strconv.Itoa(i) + "/consumption-" + Basic.String() + ".csv")
		if err != nil {
			log.Fatal(err)
		}
		defer csvConsumptionBasic.Close()

		csvLinesConsumptionBasic, err := csv.NewReader(csvConsumptionBasic).ReadAll()
		if err != nil {
			fmt.Println(err)
		}

		csvConsumptionOriginal, err := os.Open(reportPath + "/infrastructure" + strconv.Itoa(i) + "/consumption-" + Original.String() + ".csv")
		if err != nil {
			log.Fatal(err)
		}
		defer csvConsumptionOriginal.Close()

		csvLinesConsumptionOriginal, err := csv.NewReader(csvConsumptionOriginal).ReadAll()
		if err != nil {
			fmt.Println(err)
		}

		csvConsumptionOptimized, err := os.Open(reportPath + "/infrastructure" + strconv.Itoa(i) + "/consumption-" + Optimized.String() + ".csv")
		if err != nil {
			log.Fatal(err)
		}
		defer csvConsumptionOptimized.Close()

		csvLinesConsumptionOptimized, err := csv.NewReader(csvConsumptionOptimized).ReadAll()
		if err != nil {
			fmt.Println(err)
		}

		csvConsumptionEnhanced, err := os.Open(reportPath + "/infrastructure" + strconv.Itoa(i) + "/consumption-" + Enhanced.String() + ".csv")
		if err != nil {
			log.Fatal(err)
		}
		defer csvConsumptionEnhanced.Close()

		csvLinesConsumptionEnhanced, err := csv.NewReader(csvConsumptionEnhanced).ReadAll()
		if err != nil {
			fmt.Println(err)
		}

		for j := 1; j < slotCount; j++ {
			infrastructureConsumption[j][0] = csvLinesConsumptionOriginal[j][0]
			sumBasic := 0.0
			sumOriginal := 0.0
			sumOptimized := 0.0
			sumEnhanced := 0.0
			for k := 1; k < len(csvLinesConsumptionOriginal[j]); k++ {
				if k < len(csvLinesConsumptionBasic[j]) {
					bas, err := strconv.ParseFloat(csvLinesConsumptionBasic[j][k], 64)
					if err != nil {
						log.Fatal(err)
					}
					sumBasic += bas
				}

				ori, err := strconv.ParseFloat(csvLinesConsumptionOriginal[j][k], 64)
				if err != nil {
					log.Fatal(err)
				}
				sumOriginal += ori

				opt, err := strconv.ParseFloat(csvLinesConsumptionOptimized[j][k], 64)
				if err != nil {
					log.Fatal(err)
				}
				sumOptimized += opt

				enh, err := strconv.ParseFloat(csvLinesConsumptionEnhanced[j][k], 64)
				if err != nil {
					log.Fatal(err)
				}
				sumEnhanced += enh
			}

			infrastructureConsumption[j] = append(infrastructureConsumption[j], fmt.Sprintf("%.3f", sumBasic))
			infrastructureConsumption[j] = append(infrastructureConsumption[j], fmt.Sprintf("%.3f", sumOriginal))
			infrastructureConsumption[j] = append(infrastructureConsumption[j], fmt.Sprintf("%.3f", sumOptimized))
			infrastructureConsumption[j] = append(infrastructureConsumption[j], fmt.Sprintf("%.3f", sumEnhanced))

			infrastructureConsumptionExcel[0][i+1] = fmt.Sprintf("%.3f", sumBasic)
			infrastructureConsumptionExcel[1][i+1] = fmt.Sprintf("%.3f", sumOriginal)
			infrastructureConsumptionExcel[2][i+1] = fmt.Sprintf("%.3f", sumOptimized)
			infrastructureConsumptionExcel[3][i+1] = fmt.Sprintf("%.3f", sumEnhanced)
		}
	}

	for _, empRow := range infrastructureConsumption {
		_ = csvwriter.Write(empRow)
	}

	for _, empRow := range infrastructureConsumptionExcel {
		_ = csvwriterExcel.Write(empRow)
	}

	csvwriter.Flush()
	csvwriterExcel.Flush()
	csvFileConsumption.Close()
	csvFileConsumptionExcel.Close()
}
