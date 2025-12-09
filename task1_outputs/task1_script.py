import subprocess
import csv
import re

# Run mm1.exe simulation
def run_simulation(seed, interarrival, service, K, n_batches, k_arrivals):
    process = subprocess.Popen(
        ["mm1.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    input_data = (
        f"{seed}\nM\n{interarrival}\n{K}\nM\n{service}\n1\n{n_batches}\n{k_arrivals}\n"
    )
    output, error = process.communicate(input=input_data)
    return output

# Parse output and save CSV with proper headers
def parse_and_save_csv(text_output, filename):
    lines = text_output.split("\n")
    batch_data = []
    summary_data = {}

    # Regex to parse batch rows
    batch_pattern = re.compile(r"^\s*(\d+):\s+([\d\.\-#]+)\s+([\d\.\-#]+)\s+([\d\.\-#]+)\s+([\d\.\-#]+)")
    summary_patterns = {
        "ServerUtilization": re.compile(r"Server utilisation rho:\s+([\d\.\-#]+)"),
        "LossRatio": re.compile(r"Loss ratio:\s+([\d\.\-#]+)"),
        "AverageQueued": re.compile(r"Average number of queued arrivals:\s+([\d\.\-#]+)"),
        "AverageDelayQueued": re.compile(r"Average delay of queued arrivals:\s+([\d\.\-#]+)")
    }

    # Parse each line
    for line in lines:
        m = batch_pattern.match(line)
        if m:
            batch_data.append(m.groups())
            continue

        for key, pattern in summary_patterns.items():
            sm = pattern.search(line)
            if sm:
                summary_data[key] = sm.group(1)

    # Write CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Batch headers
        writer.writerow(["Batch", "LossProbability", "ServerUtilization", "AvgQueued", "AvgDelayQueued"])
        for row in batch_data:
            writer.writerow(row)

        # Summary section
        writer.writerow([])
        writer.writerow(["Summary"])
        for key, val in summary_data.items():
            writer.writerow([key, val])

# ---------------- MAIN ----------------
n = 100
K = 0
seed = 543524533

cases = {
    "a": {"interarrival": 5, "service": 5},
    "b": {"interarrival": 5, "service": 4},
    "c": {"interarrival": 5, "service": 3},
}
k_values = [250, 1000, 4000]

for case_name, params in cases.items():
    inter = params["interarrival"]
    serv = params["service"]

    for k in k_values:
        print(f"\nRunning Case {case_name.upper()} with k = {k} ...")
        sim_output = run_simulation(
            seed=seed,
            interarrival=inter,
            service=serv,
            K=K,
            n_batches=n,
            k_arrivals=k
        )
        filename = f"t1p_{case_name}_k_{k}.csv"
        parse_and_save_csv(sim_output, filename)
        print(f"Saved → {filename}")

print("\nAll simulations completed successfully!")
