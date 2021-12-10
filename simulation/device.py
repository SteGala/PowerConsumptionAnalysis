import json

class Device:
    def __init__(self, device) -> None:
        self.name = device["name"]
        self.CPU_cores = int(device["CPU_cores"])
        self.load_to_move = []

        if device["load"]["need_to_move"] == "true":
            self.has_load_to_move = True
            self.load_to_move = device["load"]["load_to_move"]
        else:
            self.has_load_to_move = False

        with open(device["consumption_details"]) as f:
            data_consumption = json.load(f)

        with open(device["performance_details"]) as f:
            data_performance = json.load(f)

        self.consumption = {}
        self.performance = {}

        self.consumption["core_usage"] = data_consumption["data"]["core_usage"]
        self.performance["core_usage"] = data_performance["data"]["core_usage"]
        self.consumption["core_consumption"] = data_consumption["data"]["core_consumption"]
        self.performance["core_score"] = data_performance["data"]["core_score"]
        
    def __str__(self) -> str:
        return "- Dev name: " + self.name + "\tCPU cores: " + str(self.CPU_cores)

    def compute_initial_workload_consumption(self):
        consumption = 0.0
        if self.has_load_to_move:
            for l in self.load_to_move:
                id = 0
                for cons in self.consumption["core_usage"]:
                    if cons == l:
                        break

                    id = id + 1

                if id >= len(self.consumption["core_usage"]):
                    print("Mismatch between power consumption data and load to move")
                    exit(-1)

                consumption = consumption + float(self.consumption["core_consumption"][id])

        return consumption

    def compute_initial_score(self):
        score = 0.0
        if self.has_load_to_move:
            for l in self.load_to_move:
                id = 0
                for cons in self.performance["core_usage"]:
                    if cons == l:
                        break

                    id = id + 1

                if id >= len(self.performance["core_usage"]):
                    print("Mismatch between power consumption data and load to move")
                    exit(-1)

                score = score + float(self.performance["core_score"][id])

        return score

    def get_total_core(self):
        return self.CPU_cores

    def get_consumption_at_load(self, load):
        if load == 0:
            return 0.0
            
        for i in range(len(self.consumption["core_usage"])):
            if load == self.consumption["core_usage"][i]:
                return float(self.consumption["core_consumption"][i])
