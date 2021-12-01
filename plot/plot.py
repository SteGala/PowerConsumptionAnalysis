def read_load_events():
    samples = []
    with open('../data/load_events', 'r') as fileRead:
        data = fileRead.readlines()
        for line in data:
            if "#how" in line:
                continue
            sample = {}
            sample["start"] = line.split(" ")[0]
            sample["load"] = line.split(" ")[1]
            sample["score"] = line.split(" ")[2]
            sample["end"] = line.split(" ")[3]
            samples.append(sample)

    return samples

def read_resource_usage(filename):
    samples = []
    with open(filename, 'r') as fileRead:
        data = fileRead.readlines()
        timestamp = 0
        for line in data:
            if "#how" in line:
                continue
            if "###" in line:
                timestamp = line.split(" ")[1]
                continue
            sample = {}
            sample["time"] = int(timestamp)
            sample["pid"] = int(line.split(" ")[0])
            sample["process"] = line.split(" ")[1]
            sample["usage"] = float(line.split(" ")[2].replace(",", "."))
            samples.append(sample)

    return samples

def aggregate_resource_usage(data):
    result = []
    last_timestamp = 0

    if len(data) > 1:
        last_timestamp = data[0]["time"]
    else:
        print("no available data for resource usage")
        exit(-1)

    cumulative_load = 0
    processed_samples = 0
    for d in data:
        processed_samples = processed_samples + 1

        if last_timestamp != d["time"] or processed_samples == len(data):
            r = {}
            r["time"] = last_timestamp
            r["usage"] = cumulative_load
            result.append(r)
            print(cumulative_load)
            last_timestamp = d["time"]
            cumulative_load = d["usage"]
        else:
            cumulative_load = cumulative_load + d["usage"]

    return result
        

if __name__ == "__main__":
    load_events = read_load_events()
    memory_usage = read_resource_usage("../data/memory_usage")
    cpu_usage = read_resource_usage("../data/cpu_usage")

    cpu_usage_aggregated = aggregate_resource_usage(cpu_usage)
    
    #print(cpu_usage_aggregated)