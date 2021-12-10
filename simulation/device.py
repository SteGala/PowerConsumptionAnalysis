import json
import utils

class Device:
    def __init__(self, device) -> None:
        self.name = device["name"]
        self.CPU_cores = float(device["CPU_cores"])
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

        self.consumption["transfer_function"] = utils.generate_continous_function_from_discrete_data(data_performance["data"]["core_score"], data_consumption["data"]["core_consumption"], self.name.split("-")[0], "Energy_consumption")
        self.performance["transfer_function"] = utils.generate_continous_function_from_discrete_data(data_performance["data"]["core_score"], data_performance["data"]["core_usage"], self.name.split("-")[0], "Pasmark_score")
        
    def __str__(self) -> str:
        return "- Dev name: " + self.name + "\tCPU cores: " + str(self.CPU_cores)

    def compute_initial_workload_consumption(self):
        consumption = 0.0
        if self.has_load_to_move:
            for l in self.load_to_move:
                consumption = consumption + float(self.consumption["transfer_function"](l))
        else:
            consumption = self.consumption["transfer_function"](0)

        return consumption

    def compute_initial_score(self):
        score = 0.0
        if self.has_load_to_move:
            for l in self.load_to_move:
                score = score + l

        return score

    def get_total_core(self):
        return self.CPU_cores

    def get_consumption_at_load(self, load):            
        return float(self.consumption["transfer_function"](load))

    def get_score_at_load(self, load):            
        return float(self.performance["transfer_function"](load))

    def convert_remaining_score_to_CPU_core(self, remaining_score):
        score = self.CPU_cores - remaining_score
        return float(self.performance["transfer_function"](score))
