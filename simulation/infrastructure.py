import json
import device

def compare_by_consumption(devices, sol1, sol2):
    consumption_sol1 = 0
    consumption_sol2 = 0

    for i in range(len(sol1)):
        CPU_used = devices[i].get_total_core() - sol1[i]
        consumption_sol1 = consumption_sol1 + devices[i].get_consumption_at_load(CPU_used)

    for i in range(len(sol2)):
        CPU_used = devices[i].get_total_core() - sol2[i]
        consumption_sol2 = consumption_sol2 + devices[i].get_consumption_at_load(CPU_used)

    return consumption_sol1 - consumption_sol2


def compare_by_score(it1, it2):
    pass
def compare_by_efficiency(it1, it2):
    pass


class Infrastructure:
    def __init__(self) -> None:
        with open('./infrastructure.json') as f:
            data = json.load(f)

        self.infra_name = data["name"]
        self.devices = []

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

        for i in range(len(self.devices)):
            remaining_core.append(int(self.devices[i].get_total_core()))
            final_solution.append(-1)
            

        for d in self.devices:
            if d.has_load_to_move:
                for l in d.load_to_move:
                    workload.append(int(l))

        self.recursive_schedule(remaining_core, workload, final_solution, 0, compare_function)
        print(final_solution)
    
    def recursive_schedule(self, remaining_core, workload, final_solution, id, compare_function):
        if id == len(workload):
            # final step of the recursion
            if final_solution[0] == -1:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]
                return

            if compare_function(self.devices, remaining_core, final_solution) < 0:
                for i in range(len(final_solution)):
                    final_solution[i] = remaining_core[i]

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

    def compute_initial_consumption(self):
        consumption = 0

        for d in self.devices:
            consumption = consumption + d.compute_initial_workload_consumption()

        return round(consumption, 2)

    def compute_initial_score(self):
        score = 0

        for d in self.devices:
            score = score + d.compute_initial_score()

        return round(score, 2)