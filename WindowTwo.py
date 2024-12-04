from tkinter import *
from PIL import ImageTk, Image

shared_data = {
    "process_data": [],
    "scheduler": None,
    "algorithm": None,
    "selected_algorithm": None
}

# Initialize the Tkinter window
window2 = Tk()
window2.title("Homepage")
window2.configure(bg="white")
window2.resizable(False, False)
window_width, window_height = 1200, 900  # Increased from 1000, 750
# Center the window on the screen
screen_width, screen_height = window2.winfo_screenwidth(), window2.winfo_screenheight()
center_x, center_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
# Set window geometry with centered position
window2.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Title Frame (Red Bar)
loading_container = Frame(window2, bg="#910909", width=window2.winfo_screenwidth())
loading_container.grid(row=0, column=0, pady=5, padx=0, sticky="ew", columnspan=2)
window2.grid_columnconfigure(0, weight=1)
window2.grid_columnconfigure(1, weight=1)
# title label
loading_label = Label(
    loading_container,
    text="Data Entry...",
    font=("Aharoni", 25, "italic"),
    fg="white", bg="#910909",
    bd=2,
    padx=5, pady=5
)
loading_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# A frame to hold the logo title and subtitle labels and the logo image
header_container = Frame(window2, bg="white")
header_container.grid(row=1, column=0, pady=10, padx=10, rowspan=3, sticky="n")
# Title Label
title_label = Label(
    header_container,
    text="CPU Scheduling",
    font=("Aharoni", 45, "bold"),
    fg="black",
    bg="white"
)
title_label.grid(row=0, column=0, pady=5, sticky="n")
# Subtitle Label
subtitle_label = Label(
    header_container,
    text="SIMULATION",
    font=("Aharoni", 25, "italic"),
    fg="#910909",
    bg="white"
)
subtitle_label.grid(row=1, column=0, pady=0, sticky="n")

# Image Section
image = Image.open("logo1.png")
image = image.resize((300, 300), Image.LANCZOS)
image_tk = ImageTk.PhotoImage(image)
image_label = Label(header_container, image=image_tk, bg="white")
image_label.grid(row=2, column=0, pady=30, sticky="n")

#================================================================================================

# A frame to hold the user input section and the button to generate the table
input_container = Frame(window2, bg="white")
input_container.grid(row=1, column=1, pady=30, padx=40, sticky="n")  # Increased padding
# Label 1: Processor
processor_label = Label(
    input_container,
    text="Processor:",
    font=("Aharoni", 20),
    fg="black",
    bg="white"
)
processor_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")
# Input Box for Processor
processor_entry = Entry(input_container, 
                        font=("Arial", 16), 
                        width=25,  # Increased from 20
                        bg="white", fg="black",
                        bd=2, relief="groove")

processor_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
# Sub-label for Processor
processor_note = Label(
    input_container,
    text="Max: 10 processes.",
    font=("Aharoni", 14),
    fg="gray",
    bg="white"
)
processor_note.grid(row=1, column=0, pady=5, padx=30, columnspan=2, sticky="w")

# Label 2: Algorithm
algorithm_label = Label(
    input_container,
    text="Algorithm:",
    font=("Aharoni", 20),
    fg="black",
    bg="white"
)
algorithm_label.grid(row=2, column=0, pady=20, sticky="w")
# Dropdown Menu for Algorithm

algorithm_options = [
    "SJF (Non-Preemptive)",
    "SJF (Preemptive)",
    "RR",
    "Preemptive (Non-Priority)",
    "Preemptive (Priority)"
]
algorithm_var = StringVar(window2)
algorithm_var.set("Select")  # Default value
algorithm_dropdown = OptionMenu(input_container, algorithm_var, *algorithm_options)
algorithm_dropdown.config(font=("Arial", 16), width=45)  # Increased from 40
algorithm_dropdown.grid(row=2, column=1, pady=10, padx=10, sticky="w")

# Button to Generate Table
# Create label for the info icon to be placed in the button "info"
gen_icon = Image.open("testimonial-1.png")
gen_icon = gen_icon.resize((300, 150), Image.LANCZOS)
gen_icon_tk = ImageTk.PhotoImage(gen_icon)

generate_button = Button(
    input_container,
    image=gen_icon_tk,
    borderwidth=0,
    width=150, height=40,
    padx=10, pady=20,
)
generate_button.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="w")

#================================================================================================

# A frame to hold the dynamic data section
data_container = Frame(window2, bg="white")
data_container.grid(row=2, column=1, pady=30, padx=30, sticky="n")  # Increased padding
# Instruction Label
instruction_label = Label(
    data_container,
    text="Fill in the data below:",
    font=("Aharoni", 20),
    fg="black",
    bg="white"
)
instruction_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")


#================================================================================================
def generate_table():
       # Clear previous table contents
    for widget in table_frame1.winfo_children():
        widget.destroy()
               # Clear previous table contents
    for widget in table_frame2.winfo_children():
        widget.destroy()

    try:
        # Get the number of processes and selected algorithm
        num_processes = int(processor_entry.get())
        selected_algorithm = algorithm_var.get()

        # Validate input
        if num_processes <= 0 or num_processes > 10:
            raise ValueError("Number of processes must be between 1 and 10.")

        if selected_algorithm == "Select":
            raise ValueError("Please select an algorithm.")
        
        # Update instruction label based on selected algorithm
        #instruction_label.config(text=f"Input parameters for: {selected_algorithm}")

        if selected_algorithm in [
            "SJF (Non-Preemptive)",
            "SJF (Preemptive)",
            "RR"
        ]:

            # Generate Table 1
            Label(table_frame1, text="ID", width=10).grid(row=0, column=0)
            Label(table_frame1, text="AT", width=10).grid(row=0, column=1)
            Label(table_frame1, text="BT", width=10).grid(row=0, column=2)
            for i in range(num_processes):
                process_id = f"P{i + 1}"
                Label(table_frame1, text=process_id, width=10).grid(row=i + 1, column=0)
                Entry(table_frame1, width=10).grid(row=i + 1, column=1)
                Entry(table_frame1, width=10).grid(row=i + 1, column=2)

        elif selected_algorithm in [
            "Preemptive (Non-Priority)",
        ]:
            # Clear previous table contents
            for widget in table_frame1.winfo_children(): widget.destroy()
            # Generate Table 2
            Label(table_frame2, text="ID", width=10).grid(row=0, column=0)
            Label(table_frame2, text="Pr", width=10).grid(row=0, column=1)
            Label(table_frame2, text="AT", width=10).grid(row=0, column=2)
            Label(table_frame2, text="BT", width=10).grid(row=0, column=3)
            for i in range(num_processes):
                process_id = f"P{i + 1}"
                Label(table_frame2, text=process_id, width=10).grid(row=i + 1, column=0)
                Entry(table_frame2, width=10).grid(row=i + 1, column=1)
                Entry(table_frame2, width=10).grid(row=i + 1, column=2)
                Entry(table_frame2, width=10).grid(row=i + 1, column=3)
                
        # Update instruction label
        instruction_label.config(text=f"Input parameters for: {selected_algorithm}")

    except ValueError as e: error_label.config(text=f"Error: NOT A VALID INPUT")


# Create frames for tables dynamically
def create_table_frames():
    global table_frame1, table_frame2
    table_frame1 = Frame(data_container, bg="white")
    table_frame1.grid(row=1, column=0, pady=10, padx=10, sticky="w")
    table_frame2 = Frame(data_container, bg="white")
    table_frame2.grid(row=2, column=0, pady=10, padx=10, sticky="w")

# Initialize Frames
create_table_frames()

# Instruction Label
instruction_label = Label(data_container, text="Select an algorithm and generate a table", font=("Aharoni", 20), fg="black", bg="white")
instruction_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

error_label = Label(data_container, text="", fg="red", bg="white")
error_label.grid(row=3, column=0, pady=10, padx=10)


# Assign functionality to the button
generate_button.config(command=generate_table)



#Create a function to open the WindowThree AND pass the data to the to it
'''
Things to be carried out:
    1. Collects Input: Collects processor count, algorithm, and process details.
    2. Stores Data: Stores the collected data in a global variable shared_data for transfer.
    3. Passes Data: Sends the data to WindowThree via the simulate button. Let me know when you're ready to handle WindowThree.
'''
# After collecting data in open_simulation_window():
def open_simulation_window():
    try:
        # Get inputs
        num_processes = int(processor_entry.get())
        selected_algorithm = algorithm_var.get()
        
        # Initialize scheduler and process data list
        from cpu_scheduler import CPUScheduler
        scheduler = CPUScheduler()
        process_data = []
        
        # Process table data...
        # ... (keep existing table processing code)
        
        # Update shared data BEFORE importing WindowThree
        global shared_data 
        shared_data.update({
            "scheduler": scheduler,
            "algorithm": selected_algorithm,
            "process_data": process_data,
            "selected_algorithm": selected_algorithm
        })
        
        # Now import WindowThree
        window2.destroy()
        import WindowThree
        WindowThree.window3.mainloop(shared_data)

    except ValueError as e:
        error_label.config(text=f"Error: {str(e)}", fg="red")

#================================================================================================
# create a label for image to be placed in the button "simulate"
simulate_icon = Image.open("Simulate.png")
simulate_icon = simulate_icon.resize((300, 150), Image.LANCZOS)
simulate_icon_tk = ImageTk.PhotoImage(simulate_icon)


# Simulate Button
simulate_button = Button(
    header_container,
    image=simulate_icon_tk,
    borderwidth=0,
    width=150, height=40,
    padx=10, pady=20,
    
)
simulate_button.grid(row=4, column=0, pady=20, padx=10, sticky="w")

#call the function to open the simulation window
simulate_button.config(command=open_simulation_window)

    



#Create an info button about table generation and its headings abreveations
# Create label for the info icon to be placed in the button "info"
info_icon = Image.open("info.png")
info_icon = info_icon.resize((320, 80), Image.LANCZOS)
info_icon_tk = ImageTk.PhotoImage(info_icon)



info_button = Button(
    header_container,
    image=info_icon_tk,
    borderwidth=0,
    width=150, height=40,
    padx=10, pady=20,
)
info_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")
# Create a function to display the info
def display_info():
    info_window = Toplevel(window2)
    info_window.title("Info")
    info_window.geometry("400x300")
    info_window.resizable(False, False)
    info_window.configure(bg="white")
    info_label = Label(
        info_window,
        text="ID: Process ID\nAT: Arrival Time\nBT: Burst Time\nPr: Priority\nNOTE: Time Quantum is FIXED TO 3 ms",
        font=("Aharoni", 20, "italic", "bold"),
        fg="black",
        bg="white"
    )
    info_label.pack(pady=20)

info_button.config(command=display_info)

window2.mainloop()