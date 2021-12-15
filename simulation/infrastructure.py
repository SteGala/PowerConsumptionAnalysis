import json
import device
import utils
import time
from threading import Thread
import datetime
import os
import pandas as pd

def compare_by_consumption(devices, sol1, sol2):
    consumption_sol1 = 0
    consumption_sol2 = 0

    for i in range(len(sol1)):
        CPU_used = devices[i].CPU_cores - sol1[i]
        consumption_sol1 = consumption_sol1 + devices[i].get_consumption_at_load(CPU_used)

    for i in range(len(sol2)):
        CPU_used = devices[i].CPU_cores - sol2[i]
        consumption_sol2 = consumption_sol2 + devices[i].get_consumption_at_load(CPU_used)

    #if consumption_sol1 < consumption_sol2:
    #    print("Found worst solution with consumption " + str(consumption_sol1))
    # lower consumption better
    return consumption_sol1 - consumption_sol2


def compare_by_score(devices, sol1, sol2):
    score_sol1 = 0
    score_sol2 = 0

    for i in range(len(sol1)):
        CPU_used = devices[i].get_total_core() - sol1[i]
        score_sol1 = score_sol1 + devices[i].get_score_at_load(CPU_used)

    for i in range(len(sol2)):
        CPU_used = devices[i].get_total_core() - sol2[i]
        score_sol2 = score_sol2 + devices[i].get_score_at_load(CPU_used)

    # higher score better
    return score_sol2 - score_sol1

def compare_by_efficiency(devices, sol1, sol2):
    efficiency_sol1 = 0
    efficiency_sol2 = 0

    for i in range(len(sol1)):
        CPU_used = devices[i].get_total_core() - sol1[i]
        consumption_sol1 = devices[i].get_consumption_at_load(CPU_used)
        score_sol1 = devices[i].get_score_at_load(CPU_used)
        efficiency_sol1 = efficiency_sol1 + score_sol1/consumption_sol1

    for i in range(len(sol2)):
        CPU_used = devices[i].get_total_core() - sol2[i]
        consumption_sol2 = devices[i].get_consumption_at_load(CPU_used)
        score_sol2 = devices[i].get_score_at_load(CPU_used)
        efficiency_sol2 = efficiency_sol2 + score_sol2/consumption_sol2

    return efficiency_sol2 - efficiency_sol1


class Infrastructure(Thread):
    def __init__(self, infra_file_name, optimization_function, directory) -> None:
        utils.remove_content_check_value_directory()

        Thread.__init__(self)

        with open(infra_file_name) as f:
            data = json.load(f)

        self.infra_name = data["name"]
        self.infra_file_name = infra_file_name
        self.directory = directory
        self.report_folder = self.directory + "/" + self.infra_file_name.split("/")[len(self.infra_file_name.split("/"))-1].split(".")[0]
        self.start_simulation = datetime.datetime.strptime(data["start_simulation"], "%Y-%m-%d %H:%M:%S")
        self.end_simulation = datetime.datetime.strptime(data["end_simulation"], "%Y-%m-%d %H:%M:%S")
        self.optimization_function = optimization_function
        self.devices = []
        self.number_of_solutions = 0
        self.total_number_of_solutions = 0
        device_type = 0

        for dt in data["devices"]:
            for i in range(int(dt["replicas"])):
                dev_json = {}
                dev_json["name"] = dt["name"] + "-#" + str(i)
                dev_json["constant_load"] = dt["constant_load"]
                dev_json["variable_load"] = dt["variable_load"]
                dev_json["CPU_cores"] = dt["CPU_cores"]
                dev_json["CPU_usage_baseline"] = dt["CPU_usage_baseline"]
                dev_json["consumption_details"] = dt["consumption_details"]
                dev_json["performance_details"] = dt["performance_details"]
                dev_json["device_type"] = device_type

                dev = device.Device(dev_json)
                self.devices.append(dev)
            device_type = device_type + 1

    def run(self):
        remaining_core = []
        workload = []
        final_solution = []
        self.number_of_solutions = 0
        start_time = time.time()

        for i in range(len(self.devices)):
            remaining_core.append(int(self.devices[i].CPU_cores))
            final_solution.append(-1)
            

        for d in self.devices:
            if d.has_constant_load_to_move:
                for l in d.constant_load_to_move:
                    workload.append(int(l))

        self.total_number_of_solutions = len(self.devices) ** len(workload)

        self.recursive_schedule(remaining_core, workload, final_solution, 0)

        os.mkdir(self.report_folder)
        
        infrastructure_consumption = {}
        infrastructure_consumption["date"] = []
        infrastructure_cpu_usage = {}
        infrastructure_cpu_usage["date"] = []

        for i in range(len(self.devices)):
            infrastructure_consumption[self.devices[i].name] = []
            infrastructure_cpu_usage[self.devices[i].name] = []

        delta = datetime.timedelta(minutes=2)
        start_date = self.start_simulation
        end_date = self.end_simulation
        while start_date <= end_date:
            infrastructure_consumption["date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
            for i in range(len(self.devices)):
                infrastructure_consumption[self.devices[i].name].append(round(self.devices[i].convert_remaining_score_to_consumption(final_solution[i]), 2))

            start_date += delta

        df = pd.DataFrame(infrastructure_consumption)

        df.to_csv(self.report_folder + '/consumption.csv', index=None)

        #print(infrastructure_consumption)
    
    def recursive_schedule(self, remaining_core, workload, final_solution, id):
        
        if id == len(workload):
            # final step of the recursion
            if final_solution[0] == -1:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]
                self.number_of_solutions = self.number_of_solutions + 1
                return

            if self.optimization_function(self.devices, remaining_core, final_solution) < 0:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]
            self.number_of_solutions = self.number_of_solutions + 1
            return

        for i in range(len(remaining_core)):
            if id == 0 and i > 0 and self.devices[i].check_same_device_type(self.devices[i-1]):
                continue
            
            if workload[id] <= remaining_core[i]:
                remaining_core[i] = remaining_core[i] - workload[id]
                self.recursive_schedule(remaining_core, workload, final_solution, id+1)
                remaining_core[i] = remaining_core[i] + workload[id]
 
        return

    def print_report(self, final_solution, start_time):
        str_ret = " -- Final Scheduling Report ---\n"
        str_ret = str_ret + "Infrastructure name:    \t" + self.infra_name + "\n"
        str_ret = str_ret + "Number of devices:      \t" + str(len(self.devices)) + "\n"
        str_ret = str_ret + "Analyzed solutions:      \t" + str(self.number_of_solutions) + "/" + str(self.total_number_of_solutions) + " (lower result may derive from pruning of unfeasible solutions)" +  "\n"
        str_ret = str_ret + "Simulation time:        \t" + str(int(time.time() - start_time)) + " s\n"
        str_ret = str_ret + "Initial power consumption: \t" + str(self.compute_initial_consumption()) + " W" + "\n"
        str_ret = str_ret + "Final power consumption: \t" + str(round(self.compute_final_consumption(final_solution), 2)) + " W" + "\n"
        str_ret = str_ret + "Initial workload score: \t" + str(self.compute_initial_score()) + "\n"
        str_ret = str_ret + "Final workload score:   \t" + str(round(self.compute_final_score(final_solution), 2)) + "\n"
        str_ret = str_ret + "Devices: \n"

        for i in range(len(self.devices)):
            str_ret = str_ret + "\t- " + self.devices[i].name + "\tCPU (used/total) " + str(round(self.devices[i].convert_remaining_score_to_CPU_core(final_solution[i]), 3)) + "/" + str(round(float(self.devices[i].convert_remaining_score_to_CPU_core(0)), 3)) + "\n"
        
        print(str_ret)
        
    def __str__(self) -> str:
        str_ret = "Infrastructure name: " + self.infra_name + "\n"
        str_ret = str_ret + "Number of devices: " + str(len(self.devices)) + "\n"
        str_ret = str_ret + "Initial power consumption: " + str(self.compute_initial_consumption()) + " W" + "\n"
        str_ret = str_ret + "Initial workload score: " + str(self.compute_initial_score()) + "\n"
        for d in self.devices:
            str_ret = str_ret + "\t" + str(d) + "\n"
        return str_ret

    def compute_initial_score(self):
        score = 0

        for d in self.devices:
            score = score + d.compute_initial_score()

        return round(score, 2)

    def compute_final_score(self, remaining_resources):
        score = 0.0
        for i in range(len(remaining_resources)):
            CPU_used = self.devices[i].CPU_cores + self.devices[i].CPU_usage_baseline  - remaining_resources[i]
            score = score + CPU_used

        return score

    def compute_initial_consumption(self):
        consumption = 0

        for d in self.devices:
            consumption = consumption + d.compute_initial_workload_consumption()

        return round(consumption, 2)

    def compute_final_consumption(self, remaining_resources):
        consumption = 0.0
        for i in range(len(remaining_resources)):
            CPU_used = self.devices[i].CPU_cores - remaining_resources[i]
            consumption = consumption + self.devices[i].get_consumption_at_load(CPU_used)

        return consumption
