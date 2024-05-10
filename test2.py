import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, arrival_time, burst_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1

class RoundRobin:
    def __init__(self, processes, quantum):
        self.processes = processes
        self.quantum = quantum
        self.current_time = 0
        self.finished_processes = []

    def run(self):
        while self.processes:
            for process in self.processes:
                if process.arrival_time <= self.current_time:
                    if process.response_time == -1:
                        process.response_time = self.current_time - process.arrival_time
                    if process.remaining_time > self.quantum:
                        self.current_time += self.quantum
                        process.remaining_time -= self.quantum
                    else:
                        self.current_time += process.remaining_time
                        process.turnaround_time = self.current_time - process.arrival_time
                        process.waiting_time = process.turnaround_time - process.burst_time
                        self.finished_processes.append(process)
                        self.processes.remove(process)
                    break
                else:
                    self.current_time += 1

    def calculate_averages(self):
        total_waiting_time = sum(process.waiting_time for process in self.finished_processes)
        total_turnaround_time = sum(process.turnaround_time for process in self.finished_processes)
        total_response_time = sum(process.response_time for process in self.finished_processes)
        num_processes = len(self.finished_processes)
        avg_waiting_time = total_waiting_time / num_processes
        avg_turnaround_time = total_turnaround_time / num_processes
        avg_response_time = total_response_time / num_processes
        return avg_waiting_time, avg_turnaround_time, avg_response_time

def validate_input(input_str):
    try:
        num = int(input_str)
        if num < 0:
            return False
        return True
    except ValueError:
        return False

def submit():
    process_count = process_count_entry.get()
    quantum = quantum_entry.get()

    if not (validate_input(process_count) and validate_input(quantum)):
        messagebox.showerror("Error", "Please enter valid positive integers.")
        return

    process_count = int(process_count)
    quantum = int(quantum)

    processes = []
    for i in range(process_count):
        arrival_time = int(arrival_time_entries[i].get())
        burst_time = int(burst_time_entries[i].get())
        processes.append(Process(arrival_time, burst_time))

    scheduler = RoundRobin(processes, quantum)
    scheduler.run()

    avg_waiting_time, avg_turnaround_time, avg_response_time = scheduler.calculate_averages()

    gantt_chart = ""
    for process in scheduler.finished_processes:
        gantt_chart += f"Process {scheduler.finished_processes.index(process) + 1} "
    gantt_chart_label.config(text=gantt_chart)

    avg_waiting_time_label.config(text=f"Average Waiting Time: {avg_waiting_time}")
    avg_turnaround_time_label.config(text=f"Average Turnaround Time: {avg_turnaround_time}")
    avg_response_time_label.config(text=f"Average Response Time: {avg_response_time}")

root = tk.Tk()
root.title("Round Robin Scheduler")

process_count_label = tk.Label(root, text="Number of Processes:")
process_count_label.grid(row=0, column=0)

process_count_entry = tk.Entry(root)
process_count_entry.grid(row=0, column=1)

quantum_label = tk.Label(root, text="Time Quantum:")
quantum_label.grid(row=1, column=0)

quantum_entry = tk.Entry(root)
quantum_entry.grid(row=1, column=1)

arrival_time_labels = []
burst_time_labels = []
arrival_time_entries = []
burst_time_entries = []

for i in range(5):  # Maximum 5 processes for simplicity
    arrival_time_labels.append(tk.Label(root, text=f"Arrival Time P{i + 1}:"))
    arrival_time_labels[i].grid(row=i+2, column=0)
    arrival_time_entries.append(tk.Entry(root))
    arrival_time_entries[i].grid(row=i+2, column=1)

    burst_time_labels.append(tk.Label(root, text=f"Burst Time P{i + 1}:"))
    burst_time_labels[i].grid(row=i+2, column=2)
    burst_time_entries.append(tk.Entry(root))
    burst_time_entries[i].grid(row=i+2, column=3)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=7, columnspan=4)

gantt_chart_label = tk.Label(root, text="")
gantt_chart_label.grid(row=8, columnspan=4)

avg_waiting_time_label = tk.Label(root, text="")
avg_waiting_time_label.grid(row=9, columnspan=4)

avg_turnaround_time_label = tk.Label(root, text="")
avg_turnaround_time_label.grid(row=10, columnspan=4)

avg_response_time_label = tk.Label(root, text="")
avg_response_time_label.grid(row=11, columnspan=4)

root.mainloop()
