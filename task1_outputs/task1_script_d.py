import subprocess
import csv
import re

def run_simulation(seed, interarrival, service, K, n_batches, k_arrivals):
    process = subprocess.Popen(
        ["mm1.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    input_data = (
        f"{seed}\n"
        f"M\n"
        f"{interarrival}\n"
        f"{K}\n"
        f"M\n"
        f"{service}\n"
        f"1\n"                  # warm-up = yes
        f"{n_batches}\n"
        f"{k_arrivals}\n"
    )
    output, error = process.communicate(input=input_data)
    if error:
        print("Error from mm1.exe:", error)
    return output

def parse_and_save_csv(text_output, filename):
    lines = text_output.splitlines()
    batch_data = []

    # Pattern for batch lines -> e.g. "98: 0.518123 0.532 0 -1.#IND"
    batch_pattern = re.compile(r"^\s*(\d+):\s+([0-9.\-+]+|#IND|-1\.#IND)\s+([0-9.\-+]+|#IND|-1\.#IND)\s+([0-9.\-+]+|#IND|-1\.#IND)\s+([0-9.\-+]+|#IND|-1\.#IND)")

    # Summary lines
    summary = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = batch_pattern.match(line)
        if m:
            batch_num = int(m.group(1))
            rho       = m.group(2)
            loss      = m.group(3)
            avg_q     = m.group(4)
            delay_q   = m.group(5)
            batch_data.append([batch_num, rho, loss, avg_q, delay_q])
            continue

        # Capture summary lines
        if "Server utilisation rho" in line:
            summary["ServerUtilization"] = line.split(":")[1].strip()
        elif "Loss ratio" in line:
            summary["LossRatio"] = line.split(":")[1].strip()
        elif "Average number of queued arrivals" in line:
            summary["AvgQueued"] = line.split(":")[1].strip()
        elif "Average delay of queued arrivals" in line:
            summary["AvgDelayQueued"] = line.split(":")[1].strip()

    # Write CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Batch",
            "ServerUtilization",
            "LossRatio",
            "AvgNumInQueue",
            "AvgDelayInQueue"
        ])

        for row in batch_data:
            writer.writerow(row)

        writer.writerow([])
        writer.writerow(["Summary Measures (across all batches)"])
        
        for key, val in summary.items():
            nice_name = {
                "ServerUtilization": "Server Utilization",
                "LossRatio":           "Loss/Blocking Probability",
                "AvgQueued":           "Average Number in Queue",
                "AvgDelayQueued":      "Average Delay of Queued Arrivals"
            }.get(key, key)
            writer.writerow([nice_name, val])

# --- Main script for Part D ---
n_batches = 400
K = 0        # No delay line
seed = 543524533
k = 1000     # fixed for part d

cases = {
    "1.d-a": {"interarrival": 5, "service": 5},
    "1.d-b": {"interarrival": 5, "service": 4},
    "1.d-c": {"interarrival": 5, "service": 3},
}

for case_name, params in cases.items():
    inter = params["interarrival"]
    serv = params["service"]

    print(f"\nRunning {case_name} | λ={1/inter:.3f}, μ={1/serv:.3f} | k={k}, n_batches={n_batches} ...")
    output = run_simulation(seed, inter, serv, K, n_batches, k)
    csv_file = f"t1p_{case_name}_k{k}.csv"
    parse_and_save_csv(output, csv_file)
    print(f"Saved -> {csv_file}")

print("\nAll part D simulations completed successfully!")
