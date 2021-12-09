import json
import device

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

    def schedule_wokloads(self):
        count = []
        remaining_core = []
        workload = []

        for i in range(len(self))
    def recursive_schedule(self):



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