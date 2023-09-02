import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
from tkinter import ttk

class TrafficSignRecognitionUI:
    def __init__(self, master):
        self.master = master
        master.title(" ")
        master.attributes("-alpha", True)  # set the window to full-screen

        style = ttk.Style()
        style.configure('TButton', background='#00AA8D', foreground='white', font=('Arial', 14))
        style.map("TButton", foreground=[('active', 'white')], background=[('active', 'GREEN')])

        # Create a label for the main title
        self.main_label = ttk.Label(master, text="TRAFFIC SIGN RECOGNITION AND VOICE ALERT SYSTEM", font=('Arial', 30, 'bold'))
        self.main_label.pack(pady=20)

        # Create a label and button to browse for the .h5 model
        self.model_label = ttk.Label(master, text="LOAD THE MODEL BELOW :", font=('Arial', 17, 'bold'))
        self.model_label.pack(pady=50)

        self.model_path = tk.StringVar()
        self.model_textbox = ttk.Entry(master, textvariable=self.model_path, width=40, font=('Arial', 16))
        self.model_textbox.pack()

        style.configure('Blue.TButton', background='#0074D9', foreground='white', font=('Arial', 12))
        style.map("Blue.TButton", foreground=[('active', 'white')], background=[('active', 'green')])

        style.configure('Red.TButton', background='#ED2939', foreground='white', font=('Arial', 12))
        style.map("Red.TButton", foreground=[('active', 'white')], background=[('active', 'green')])

        self.model_button = ttk.Button(master, text="Browse", command=self.browse_model, style='Blue.TButton')
        self.model_button.pack(pady=20)

        # Create a label for output textarea
        self.textarea_label = ttk.Label(master, text="PREDICTED TRAFFIC SIGN :", font=('Arial', 17, 'bold'))
        self.textarea_label.pack(pady=10)

        # Create a text area to display the output
        self.text_area = tk.Text(master, height=10, width=80, font=('Arial Unicode MS', 12))
        self.text_area.pack(pady=20)

        # Create a frame to hold the buttons in the same row
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=20)

        # Create start and stop buttons to run and stop the detection code
        self.start_button = ttk.Button(button_frame, text="START REAL-TIME DETECTION", command=self.start_detection, style='TButton', state='disabled')
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.clear_button = ttk.Button(button_frame, text="CLEAR OUTPUT", command=self.clear_text_area, style='Red.TButton')
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = ttk.Button(button_frame, text="QUIT", command=self.confirm_quit, style='TButton')
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Store the detection process as an instance variable
        self.detection_process = None

    def browse_model(self):
        # Open a file dialog to browse for the .h5 model
        model_path = filedialog.askopenfilename(filetypes=[("HDF5 files", "*.h5")])
        self.model_path.set(model_path)
        self.start_button.config(state='normal')  # enable the start detection button

    def confirm_quit(self):
        # Display a confirmation dialog before quitting
        result = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if result == tk.YES:
            self.master.quit()

    def start_detection(self):
        # Get the selected model path and pass it to detect.py
        model_path = self.model_path.get()
        command = ["python3", "detect.py", "-m", model_path]

        # Start the detection process and capture the output in real-time
        self.detection_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Start a new thread to read the output of the detection process and update the text area in real-time
        self.detection_thread = threading.Thread(target=self.read_output)
        self.detection_thread.start()

    def read_output(self):
    # Read the output of the detection process and display it in the text area
        while True:
            output = self.detection_process.stdout.readline()
            if not output:
                break
            self.text_area.insert(tk.END, output)
            self.text_area.see(tk.END)  # Scroll to the end of the text area
        self.master.update()



    def stop_detection(self):
        if self.detection_process:
            # Send a 'quit' message to the detection process to stop it
            self.detection_conn.send("quit")

            # Kill the detection process
            self.detection_process.kill()

            # Destroy the detection window
            self.detection_window.destroy()
            self.detection_window = None

    def clear_text_area(self):
        # Clear the text area
        self.text_area.delete('1.0', tk.END)


root = tk.Tk()
gui = TrafficSignRecognitionUI(root)
root.mainloop()

