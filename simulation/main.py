import infrastructure as infra
import os
import time
import utils

N_THREAD = 1

if __name__ == "__main__":
    report_path = "./reports-" + str(int(time.time()))
    utils.create_report_directory(report_path)
    infrastructures = []

    for i in range(N_THREAD):
        infrastructure = infra.Infrastructure('./example_infrastructures/infrastructure.json', infra.compare_by_consumption)
        infrastructures.append(infrastructure)

    # Start all threads
    for x in infrastructures:
        x.start()

    # Wait for all of them to finish
    for x in infrastructures:
        x.join()

    #print()
    #print("Scheduling simulation optimized for execution score")
    #infrastructure.schedule_wokloads(infra.compare_by_score)
#
    #print()
    #print("Scheduling simulation optimized for efficiency")
    #infrastructure.schedule_wokloads(infra.compare_by_efficiency)