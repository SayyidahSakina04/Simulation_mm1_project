import subprocess
import openpyxl
import os


# Helper function to run mm1.exe with given parameters
def run_simulation(seed, interarrival, service, K, n_batches, k_arrivals):
    """
    This function runs mm1.exe using subprocess and collects the text output.
    """
    process = subprocess.Popen(
        ["mm1.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Prepare input sequence as if user typed them manually in the console
    input_data = f"{seed}\nM\n{interarrival}\n{K}\nM\n{service}\n1\n{n_batches}\n{k_arrivals}\n"

    output, error = process.communicate(input=input_data)
    return output


# Helper function to save output to Excel
def save_to_excel(text_output, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Simulation Output"

    # Write line-by-line to excel
    for i, line in enumerate(text_output.split("\n"), start=1):
        ws.cell(row=i, column=1, value=line)

    wb.save(filename)



# Main
print("--- TASK 1 AUTOMATED SIMULATION SCRIPT ---")
print("This script will run parts a, b, c for k = 250, 1000, 4000")
print("Results will be saved as Excel files.\n")

# n = int(input("Enter number of batches (n): "))
n = 100

# Queue size = 0 for task 1
K = 0

# Fixed seed for reproducibility
seed = 543524533

# Task 1 parameter sets
cases = {
    "a": {"interarrival": 5, "service": 5},
    "b": {"interarrival": 5, "service": 4},
    "c": {"interarrival": 5, "service": 3},
}

# Values of k to test
k_values = [250, 1000, 4000]


# RUNNING ALL SIMULATIONS

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

        filename = f"t1p'{case_name}'k'{k}'.xlsx"
        save_to_excel(sim_output, filename)

        print(f"Saved → {filename}")

print("\nAll simulations completed successfully!")
