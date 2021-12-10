import json
import device
import utils

def compare_by_consumption(devices, sol1, sol2):
    consumption_sol1 = 0
    consumption_sol2 = 0

    for i in range(len(sol1)):
        CPU_used = devices[i].get_total_core() - sol1[i]
        consumption_sol1 = consumption_sol1 + devices[i].get_consumption_at_load(CPU_used)

    for i in range(len(sol2)):
        CPU_used = devices[i].get_total_core() - sol2[i]
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


class Infrastructure:
    def __init__(self) -> None:
        utils.remove_content_check_value_directory()

        with open('./infrastructure.json') as f:
            data = json.load(f)

        self.infra_name = data["name"]
        self.devices = []
        self.number_of_solutions = 0

        for dt in data["devices"]:
            for i in range(int(dt["replicas"])):
                dev_json = {}
                dev_json["name"] = dt["name"] + "-" + str(i)
                dev_json["load"] = dt["load"]
                dev_json["CPU_cores"] = dt["CPU_cores"]
                dev_json["consumption_details"] = dt["consumption_details"]
                dev_json["performance_details"] = dt["performance_details"]

                dev = device.Device(dev_json)
                self.devices.append(dev)

    def schedule_wokloads(self, compare_function):
        remaining_core = []
        workload = []
        final_solution = []
        self.number_of_solutions = 0

        for i in range(len(self.devices)):
            remaining_core.append(int(self.devices[i].get_total_core()))
            final_solution.append(-1)
            

        for d in self.devices:
            if d.has_load_to_move:
                for l in d.load_to_move:
                    workload.append(int(l))

        self.recursive_schedule(remaining_core, workload, final_solution, 0, compare_function)

        str_ret = " -- Final Scheduling Report ---\n"
        str_ret = str_ret + "Infrastructure name:    \t" + self.infra_name + "\n"
        str_ret = str_ret + "Number of devices:      \t" + str(len(self.devices)) + "\n"
        str_ret = str_ret + "Analyzed solutions:      \t" + str(self.number_of_solutions) + "\n"
        str_ret = str_ret + "Initial power consumption: \t" + str(self.compute_initial_consumption()) + " W" + "\n"
        str_ret = str_ret + "Final power consumption: \t" + str(round(self.compute_final_consumption(final_solution), 2)) + " W" + "\n"
        str_ret = str_ret + "Initial workload score: \t" + str(self.compute_initial_score()) + "\n"
        str_ret = str_ret + "Final workload score:   \t" + str(round(self.compute_final_score(final_solution), 2)) + "\n"
        str_ret = str_ret + "Devices: \n"

        for i in range(len(self.devices)):
            str_ret = str_ret + "\t- " + self.devices[i].name + "\tCPU (used/total) " + str(round(self.devices[i].convert_remaining_score_to_CPU_core(final_solution[i]), 1)) + "/" + str(round(float(self.devices[i].convert_remaining_score_to_CPU_core(0)), 1)) + "\n"
        
        print(str_ret)
    
    def recursive_schedule(self, remaining_core, workload, final_solution, id, compare_function):
        if id == len(workload):
            # final step of the recursion
            if final_solution[0] == -1:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]
                self.number_of_solutions = self.number_of_solutions + 1
                return

            if compare_function(self.devices, remaining_core, final_solution) < 0:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]
            self.number_of_solutions = self.number_of_solutions + 1
            return

        for i in range(len(remaining_core)):
            if workload[id] <= remaining_core[i]:
                remaining_core[i] = remaining_core[i] - workload[id]
                self.recursive_schedule(remaining_core, workload, final_solution, id+1, compare_function)
                remaining_core[i] = remaining_core[i] + workload[id]
 
        return
        



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
            CPU_used = self.devices[i].CPU_cores - remaining_resources[i]
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
