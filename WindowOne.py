from tkinter import *
from PIL import ImageTk, Image

# Initialize the Tkinter window
window1 = Tk()
window1.title("CPU Scheduling")
window1.configure(bg="white")
window1.resizable(False, False)

window_width, window_height = 1000, 670

# Center the window on the screen
screen_width, screen_height = window1.winfo_screenwidth(), window1.winfo_screenheight()
center_x, center_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2

# Set window geometry with centered position
window1.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


# Load, resize, and set logo image
logo = Image.open("/Users/majid/Desktop/operating systems/OSaPP/assets/logo1.png")
resized_logo = logo.resize((550, 450))
resized_logo_photo = ImageTk.PhotoImage(resized_logo)
logo_label = Label(window1, image=resized_logo_photo, bg="white").grid(row = 0, column = 0, pady = 10, sticky = "n")

# Create a container to hold the title and subtitle labels
container = Frame(window1, bg="white")
container.grid(row=0, column=1, pady=100, padx=10, sticky="n")
#Title Label
title_label = Label(container, 
                    text="CPU Scheduling", 
                    font=("Aharoni", 45, "bold"), 
                    fg="black", 
                    bg="white")
title_label.grid(row=0, column=0, pady=10, sticky="n", )
#Subtitle Label
subtitle_label = Label(container, 
                       text="SIMULATION", 
                       font=("Aharoni", 25, "italic"), 
                       fg="#910909", bg="white")
subtitle_label.grid(row=1, column=0, pady=0, sticky="n")

# Animation for the subtitle
text_to_display = "SIMULATION"
current_index = 0
def typewriter_effect():
    global current_index
    # Append one more character to the displayed text
    if current_index < len(text_to_display):
        subtitle_label.config(text=text_to_display[:current_index + 1])
        current_index += 1
        # typewriter effect for 300 ms
        window1.after(300, typewriter_effect)
credits_container = Frame(window1, bg="white")
typewriter_effect()
credits_container.grid(row=1, column=1, pady=10, padx=10, sticky="n")

#Credits Label
credits_label = Label(credits_container, 
                      text="By:\n\t\t• LISA (B09230013)\n\t\t• AINA (B09230011)\n\t\t• FIQA (B09230022)", 
                      font=("Aharoni", 20), 
                      fg="black", bg="white", 
                      justify="center").grid(row=0, column=0, pady=0, sticky="n")
credits_container.grid(row=1, column=1, pady=10, padx=10, sticky="n")

# Create a container to hold the loading label
loading_container = Frame(window1, bg="#910909", width=window1.winfo_screenwidth())
loading_container.grid(row=2, column=0, pady=5, padx=0, sticky="ew", columnspan=2)
window1.grid_columnconfigure(0, weight=1)
window1.grid_columnconfigure(1, weight=1)
# Loading Label
loading_label = Label(
    loading_container,
    text="Loading...",
    font=("Aharoni", 25, "italic"),
    fg="white", bg="#910909",
    bd=2,
    padx=5, pady=5
)
loading_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Transition to Window 2 after 5 seconds
def transition_to_window2():
    window1.destroy()
    import WindowTwo
    WindowTwo.window2.mainloop()
window1.after(5000, transition_to_window2)


window1.mainloop()