import tkinter as tk
from tkinter import messagebox

class SJFSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("SJF Simulation")

        self.num_processes = 0
        self.process_data = []
        self.current_time = 0
        self.ready_queue = []
        self.gantt_chart = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Number of Processes:").grid(row=0, column=0)
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.grid(row=0, column=1)

        tk.Button(self.root, text="Submit", command=self.submit_processes).grid(row=0, column=2)

    def submit_processes(self):
        try:
            self.num_processes = int(self.num_processes_entry.get())
            if self.num_processes <= 0:
                raise ValueError
            self.create_process_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of processes.")

    def create_process_entries(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Arrival Time").grid(row=0, column=0)
        tk.Label(self.root, text="Burst Time").grid(row=0, column=1)

        for i in range(self.num_processes):
            tk.Label(self.root, text=f"Process {i + 1}:").grid(row=i + 1, column=0)
            arrival_entry = tk.Entry(self.root)
            burst_entry = tk.Entry(self.root)
            arrival_entry.grid(row=i + 1, column=1)
            burst_entry.grid(row=i + 1, column=2)
            self.process_data.append((arrival_entry, burst_entry))

        tk.Button(self.root, text="Start Simulation", command=self.start_simulation).grid(row=self.num_processes + 1, columnspan=3)

    def start_simulation(self):
        self.process_data = [(int(arrival.get()), int(burst.get())) for arrival, burst in self.process_data]
        self.process_data.sort(key=lambda x: x[0])  

        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        self.current_time = 0

        for arrival, burst in self.process_data:
            if arrival > self.current_time:
                self.current_time = arrival
            self.ready_queue.append((arrival, burst))

            self.ready_queue.sort(key=lambda x: x[1])

            current_process = self.ready_queue.pop(0)
            self.gantt_chart.append((current_process[0], self.current_time))
            self.current_time += current_process[1]

            waiting_time = self.current_time - arrival - burst
            turnaround_time = self.current_time - arrival
            response_time = waiting_time if waiting_time > 0 else 0

            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
            total_response_time += response_time

            # Display waiting time, turnaround time, and response time for each process
            messagebox.showinfo("Process Results",
                                f"Process {len(self.gantt_chart)}:\n"
                                f"Waiting Time: {waiting_time}\n"
                                f"Turnaround Time: {turnaround_time}\n"
                                f"Response Time: {response_time}")

        avg_waiting_time = total_waiting_time / self.num_processes
        avg_turnaround_time = total_turnaround_time / self.num_processes
        avg_response_time = total_response_time / self.num_processes

        self.display_gantt_chart()

        messagebox.showinfo("Simulation Results", 
                            f"Average Waiting Time: {avg_waiting_time:.2f}\n"
                            f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
                            f"Average Response Time: {avg_response_time:.2f}")

    def display_gantt_chart(self):
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Gantt Chart")

        canvas = tk.Canvas(gantt_window, width=600, height=200)
        canvas.pack()

        y = 50
        for index, (start, end) in enumerate(self.gantt_chart):
            canvas.create_text(start * 10, y, anchor=tk.SW, text=f"P{index + 1}")
            canvas.create_rectangle(start * 10, y - 20, end * 10, y + 20, fill="sky blue")
            canvas.create_text(end * 10, y, anchor=tk.SE, text=f"{end}")

        canvas.create_text(0, y + 30, anchor=tk.SW, text="Time")
        canvas.create_line(0, y, 600, y)
        canvas.create_line(0, y - 20, 0, y + 20, arrow=tk.LAST)

def main():
    root = tk.Tk()
    app = SJFSimulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
