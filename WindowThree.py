from tkinter import *
from PIL import ImageTk, Image
import sys

# Import shared data with proper fallback and initialization check
try:
    from WindowTwo import shared_data
    if not shared_data["scheduler"]:
        raise ImportError("No scheduler data")
except (ImportError, KeyError):
    print("No data available, returning to Window Two")
    import WindowTwo
    WindowTwo.window2.mainloop()
    sys.exit()

# Initialize variables from shared data
process_data = shared_data.get('process_data', [])
scheduler = shared_data.get('scheduler')
selected_algorithm = shared_data.get('selected_algorithm')

#CPU Scheduling Algorithms
#SJF (Non-Preemptive)
def sjf_non_preemptive(processes):
    # Sort by Arrival Time (AT), then Burst Time (BT)
    processes.sort(key=lambda x: (int(x[1]), int(x[2])))
    current_time = 0
    result = []

    for process in processes:
        pid, at, bt = process[0], int(process[1]), int(process[2])
        if current_time < at:
            current_time = at
        ct = current_time + bt
        tat = ct - at
        wt = tat - bt
        result.append([pid, at, bt, ct, tat, wt])
        current_time = ct

    return result
from heapq import heappush, heappop
#SJF (Preemptive)
def sjf_preemptive(processes):
    processes.sort(key=lambda x: int(x[1]))  # Sort by Arrival Time (AT)
    time = 0
    completed = 0
    n = len(processes)
    ready_queue = []
    result = []
    remaining_bt = {process[0]: int(process[2]) for process in processes}

    while completed < n:
        for process in processes:
            pid, at, bt = process[0], int(process[1]), int(process[2])
            if at <= time and remaining_bt[pid] > 0 and pid not in [p[1] for p in ready_queue]:
                heappush(ready_queue, (remaining_bt[pid], pid))

        if ready_queue:
            bt, pid = heappop(ready_queue)
            remaining_bt[pid] -= 1
            time += 1

            if remaining_bt[pid] == 0:
                completed += 1
                ct = time
                at = next(p[1] for p in processes if p[0] == pid)
                bt = next(p[2] for p in processes if p[0] == pid)
                tat = ct - int(at)
                wt = tat - int(bt)
                result.append([pid, at, bt, ct, tat, wt])
        else:
            time += 1

    return result
#round robin
def round_robin(processes, time_quantum=3):
    processes.sort(key=lambda x: int(x[1]))  # Sort by Arrival Time (AT)
    time = 0
    result = []
    queue = [(process[0], int(process[1]), int(process[2])) for process in processes]
    remaining_bt = {process[0]: int(process[2]) for process in processes}

    while queue:
        pid, at, _ = queue.pop(0)
        if time < at:
            time = at

        exec_time = min(remaining_bt[pid], time_quantum)
        time += exec_time
        remaining_bt[pid] -= exec_time

        if remaining_bt[pid] > 0:
            queue.append((pid, at, remaining_bt[pid]))
        else:
            ct = time
            bt = next(p[2] for p in processes if p[0] == pid)
            tat = ct - int(at)
            wt = tat - int(bt)
            result.append([pid, at, bt, ct, tat, wt])

    return result
#Preemptive (Priority)
def preemptive_priority(processes):
    processes.sort(key=lambda x: int(x[1]))  # Sort by Arrival Time (AT)
    time = 0
    completed = 0
    n = len(processes)
    ready_queue = []
    result = []
    remaining_bt = {process[0]: int(process[2]) for process in processes}

    while completed < n:
        for process in processes:
            pid, at, bt, pr = process[0], int(process[1]), int(process[2]), int(process[3])
            if at <= time and remaining_bt[pid] > 0 and pid not in [p[1] for p in ready_queue]:
                heappush(ready_queue, (pr, pid))

        if ready_queue:
            pr, pid = heappop(ready_queue)
            remaining_bt[pid] -= 1
            time += 1

            if remaining_bt[pid] == 0:
                completed += 1
                ct = time
                at, bt, pr = next((p[1], p[2], p[3]) for p in processes if p[0] == pid)
                tat = ct - int(at)
                wt = tat - int(bt)
                result.append([pid, at, bt, ct, tat, wt])
        else:
            time += 1

    return result
#Declare a dictionary to store shared data
shared_data = {}
# Initialize the Tkinter window
window3 = Tk()
window3.title("Process Page")
window3.configure(bg="white")
window3.resizable(False, False)
window_width, window_height = 1200, 870
# Center the window on the screen
screen_width, screen_height = window3.winfo_screenwidth(), window3.winfo_screenheight()
center_x, center_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
# Set window geometry with centered position
window3.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
# Title Frame (Red Bar)
loading_container = Frame(window3, bg="#910909", width=window3.winfo_screenwidth())
loading_container.grid(row=0, column=0, pady=5, padx=0, sticky="ew", columnspan=2)
window3.grid_columnconfigure(0, weight=1)
window3.grid_columnconfigure(1, weight=1)
# Title label
loading_label = Label(
    loading_container,
    text="Data Entry...",
    font=("Aharoni", 25, "italic"),
    fg="white", bg="#910909",
    bd=2,
    padx=5, pady=5
)
loading_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
# Create frame1 for table and a label
frame1 = Frame(window3, bg="white")
frame1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Create a label for the table
table_label = Label(frame1, text="Statistics", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
table_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# Create a table with headings: ID, AT, BT, CT, TAT, WT
# Note: Numner of rows will be dynamic and the data will be fetched from window2
table = Frame(frame1, bg="white")
table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Create a method to generate the table
def generate_table():
    # Clear existing table
    for widget in table.winfo_children():
        widget.destroy()

    try:
        scheduler = shared_data.get('scheduler')
        algorithm = shared_data.get('algorithm')
        
        if not scheduler or not algorithm:
            Label(table, text="No data available", width=30).grid(row=0, column=0)
            return

        # Run selected algorithm
        if algorithm == "SJF (Non-Preemptive)":
            results = scheduler.sjf_nonpreemptive()
        elif algorithm == "SJF (Preemptive)":
            results = scheduler.sjf_preemptive()
        elif algorithm == "RR":
            results = scheduler.round_robin()
        elif algorithm in ["Preemptive (Non-Priority)", "Preemptive (Priority)"]:
            results = scheduler.priority_scheduling(preemptive=True)

        # Display results in table
        headings = ["ID", "AT", "BT", "CT", "TAT", "WT"]
        for i, heading in enumerate(headings):
            Label(table, text=heading, width=10, relief="solid").grid(row=0, column=i)

        for i, process in enumerate(scheduler.processes):
            values = [
                process.pid,
                process.arrival_time,
                process.burst_time,
                process.completion_time,
                process.turnaround_time,
                process.waiting_time
            ]
            for j, value in enumerate(values):
                Label(table, text=value, width=10, relief="solid").grid(row=i+1, column=j)

        # Update averages
        update_averages(scheduler)
        
    except Exception as e:
        Label(table, text=f"Error: {str(e)}", width=30).grid(row=0, column=0)

    def update_averages(scheduler):
        total_ct = sum(p.completion_time for p in scheduler.processes)
        total_tat = sum(p.turnaround_time for p in scheduler.processes)
        total_wt = sum(p.waiting_time for p in scheduler.processes)
        n = len(scheduler.processes)
        
        avg_entries = frame4.grid_slaves()
        avg_entries[4].delete(0, END)
        avg_entries[4].insert(0, f"{total_ct/n:.2f}")
        avg_entries[2].delete(0, END) 
        avg_entries[2].insert(0, f"{total_tat/n:.2f}")
        avg_entries[0].delete(0, END)
        avg_entries[0].insert(0, f"{total_wt/n:.2f}")

# Call the method to generate the table
generate_table()

#================================================================================================
#Create a frame for the Ready Queue of processes
frame3 = Frame(window3)
frame3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
# Create a label for the Ready Queue
ready_queue_label = Label(frame3, text="Ready Queue", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
ready_queue_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# Create a canvas for the Ready Queue
canvas = Canvas(frame3,bg="black", width=700, height=100)
canvas.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
# Create a method to generate the Ready Queue
def generate_ready_queue():
    # Clear existing canvas
    canvas.delete("all")

    try:
        # Fetch and process data for the ready queue
        process_data = shared_data.get('process_data', [])
        selected_algorithm = shared_data.get('selected_algorithm')

        if not process_data or not selected_algorithm:
            return

        if selected_algorithm in ["SJF (Non-Preemptive)", "SJF (Preemptive)", "RR", "Preemptive (Priority)"]:
            results = sjf_non_preemptive(process_data) if selected_algorithm == "SJF (Non-Preemptive)" else \
                      sjf_preemptive(process_data) if selected_algorithm == "SJF (Preemptive)" else \
                      round_robin(process_data) if selected_algorithm == "RR" else \
                      preemptive_priority(process_data)

            # Draw ready queue
            x_offset = 10
            for process in results:
                process_id = process[0]
                canvas.create_rectangle(x_offset, 50, x_offset + 50, 100, fill="blue")
                canvas.create_text(x_offset + 25, 75, text=process_id, fill="white")
                x_offset += 60
    except Exception as e:
        print(f"Error in generate_ready_queue: {e}")

# Call the method to generate the Ready Queue
generate_ready_queue()

#================================================================================================
# Create a frame for the Gantt Chart
frame2 = Frame(window3, bg="white")
frame2.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Create a label for the Gantt Chart
gantt_label = Label(frame2, text="Gantt Chart", font=("Aharoni", 20, "bold"), fg= "black",bg="red")
gantt_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create a canvas for the Gantt Chart
canvas = Canvas(frame2,bg="black", width=700, height=100)
canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Create a method to generate the Gantt Chart
def generate_gantt_chart():
    # Clear existing canvas
    canvas.delete("all")

    # Fetch and process data for the Gantt chart
    process_data = shared_data.get('process_data', [])
    selected_algorithm = shared_data.get('selected_algorithm', '')

    if selected_algorithm in ["SJF (Non-Preemptive)", "SJF (Preemptive)", "RR", "Preemptive (Priority)"]:
        results = sjf_non_preemptive(process_data) if selected_algorithm == "SJF (Non-Preemptive)" else \
                  sjf_preemptive(process_data) if selected_algorithm == "SJF (Preemptive)" else \
                  round_robin(process_data) if selected_algorithm == "RR" else \
                  preemptive_priority(process_data)

        # Draw Gantt chart
        x_offset = 10
        for process in results:
            process_id = process[0]
            start_time = process[1]  # Replace with actual start time if available
            end_time = process[3]    # Completion Time (CT)
            canvas.create_rectangle(x_offset, 50, x_offset + (end_time - start_time) * 50, 100, fill="green")
            canvas.create_text(x_offset + ((end_time - start_time) * 25), 75, text=process_id, fill="white")
            x_offset += (end_time - start_time) * 50       
# Call the method to generate the Gantt Chart
generate_gantt_chart()
      
#================================================================================================

# Create a frame for the Averages: CT, TAT, WT
frame4 = Frame(window3, bg="white")
frame4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
label_avg = Label(frame4, text="Averages: ", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
label_avg.grid(row=0, column=0, padx=10, pady=10, sticky="w")
labels = ["CT", "TAT", "WT"]
# Create a label for the Averages
for i in range(len(labels)):
    Label(frame4, text=labels[i], font=("Aharoni", 20, "bold"), fg= "black",bg="white").grid(row=i+1, column=0, padx=20, pady=10, sticky="w")
    
# display boxes for the averages
for i in range(len(labels)):
    Entry(frame4, width=10).grid(row=i+1, column=1, padx=10, pady=10, sticky="w")   
# A label for information on calculating the averages
label_info1 = Label(frame4, text="Note:\n\tCT = Completion Time\n\tTAT = Turnaround Time\n\tWT = Waiting Time", font=("Aharoni", 15, "bold", "italic"), fg= "black",bg="white")
label_info1.grid(row=4, column=0, padx=5, pady=10, sticky="w",)
label_info2 = Label(frame4, text=" CT = FROM Gantt chart\nTAT = CT - AT\nWT = TAT - BT", font=("Aharoni", 15, "bold", "italic"), fg= "black",bg="white")
label_info2.grid(row=5, column=0, padx=5, pady=10, sticky="w")

#================================================================================================
# create a frame for the buttons
frame5 = Frame(window3, bg="white")
frame5.grid(row=2, column=1, padx=10, pady=20, sticky="nsew", rowspan=2)

# Create a button to go back to the Homepage
btn_complete = Button(frame5, text="Finish", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
btn_complete.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
def complete():
    window3.destroy()
    import WindowTwo
    WindowTwo.window2.mainloop()
#CALL
btn_complete.config(command=complete)

# Create a button to reload the data
btn_reload = Button(frame5, text="Reload", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
btn_reload.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
def reload_data():
    generate_table()
    generate_ready_queue()
    generate_gantt_chart()
#CALL
btn_reload.config(command=reload_data)


# Create a button to exit the application
btn_exit = Button(frame5, text="Exit", font=("Aharoni", 20, "bold"), fg= "black",bg="white")
btn_exit.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
def exit_app():
    window3.destroy()
#CALL
btn_exit.config(command=exit_app)

# Run the application
window3.mainloop()
