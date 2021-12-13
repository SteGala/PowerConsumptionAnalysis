import json
import utils

class Device:
    def __init__(self, device) -> None:
        self.name = device["name"]
        self.CPU_usage_baseline = float(device["CPU_usage_baseline"])
        self.CPU_cores = float(device["CPU_cores"]) - self.CPU_usage_baseline
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
        load = self.CPU_usage_baseline
        if self.has_load_to_move:
            for l in self.load_to_move:
                load = load + l

        return self.consumption["transfer_function"](load)

    def compute_initial_score(self):
        score = self.CPU_usage_baseline
        if self.has_load_to_move:
            for l in self.load_to_move:
                score = score + l

        return score

    def get_consumption_at_load(self, load):            
        return float(self.consumption["transfer_function"](load + self.CPU_usage_baseline))

    def get_score_at_load(self, load):            
        return float(self.performance["transfer_function"](load + self.CPU_usage_baseline))

    def convert_remaining_score_to_CPU_core(self, remaining_score):
        score = self.CPU_cores + self.CPU_usage_baseline - remaining_score
        return float(self.performance["transfer_function"](score))

    def check_same_device_type(self, dev2):
        if self.has_load_to_move and dev2.has_load_to_move:
            if self.load_to_move == dev2.load_to_move:
                if self.name.split('-')[0] == dev2.name.split('-')[0]:
                    return True
        return False