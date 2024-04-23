import tkinter as tk
from tkinter import filedialog
from backend.functions import start_connection_controller
import threading

class GUI:
    PATH_JSON_MODEL = "Path"
    connected = False

    def __init__(self):
        # Create a new instance of Tkinter application
        self.app = tk.Tk()

    # ---------- WINDOW SETTINGS ---------------------------------------
        self.app.title("Serial CSV to UDP JSON Translator")

        # Set the width and height of the window
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.window_width = 500
        self.window_height = 320
        self.x_coordinate = (self.screen_width - self.window_width) // 2
        self.y_coordinate = (self.screen_height - self.window_height) // 2

        # Set the geometry of the window to position it on the center of the screen
        self.app.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.app.iconbitmap('img/icon.ico')

    # ---------- GUI ELEMENTS --------------------------------------------
        self.label = tk.Label(self.app, text="Press connect to start converting Serial messages \nto JSON and stream them to UDP (localhost).")
        self.label.pack(pady=10)

        # Local UDP Port
        self.label_udp_port = tk.Label(self.app, text="Local UDP port:")
        self.label_udp_port.pack()
        self.textbox_udp_port = tk.Text(self.app, height=1, width=30)
        self.textbox_udp_port.insert("1.0", "1000")                        # Default UDP port
        self.textbox_udp_port.pack()

        # Serial Port
        self.label_serial_port = tk.Label(self.app, text="Serial port:")
        self.label_serial_port.pack()
        self.textbox_serial_port = tk.Text(self.app, height=1, width=30)
        self.textbox_serial_port.insert("1.0", "COM3")                        # Default Serial port
        self.textbox_serial_port.pack()

        # Path JSON model
        self.label_path_json_model = tk.Label(self.app, text="Select path to JSON data model to use:")
        self.label_path_json_model.pack()
        self.textbox_path_json_model = tk.Text(self.app, height=1, width=50)
        self.textbox_path_json_model.pack()
        self.textbox_path_json_model.insert("1.0", self.PATH_JSON_MODEL)
        self.browse_button_json_model = tk.Button(self.app, text="Browse", command=self.browse_file_json_model)
        self.browse_button_json_model.pack()

        # Connect button
        self.connect_button = tk.Button(self.app, text="Connect", command=self.connect_thread, font=("Arial", 14, "bold"), width=15, height=2)
        self.connect_button.pack(pady=15)

        # Connected status
        self.label_connected = tk.Label(self.app, text="CONNECTED!", font=("Arial", 14, "bold"))
        self.label_connected.forget()

        # Start the Tkinter event loop
        self.app.mainloop()

    # ---------- FUNCTIONS ---------------------------------------------
    def browse_file_json_model(self):
        self.file_path_json_model = filedialog.askopenfilename()
        self.textbox_path_json_model.delete("1.0", tk.END)
        self.textbox_path_json_model.insert("1.0", self.file_path_json_model)

        global PATH_JSON_MODEL
        self.PATH_JSON_MODEL = self.file_path_json_model

    def connect_thread(self):
        # Start a new thread for the connect function
        threading.Thread(target=self.connect, daemon=True).start()

    def connect(self):
        # Get the port from the textbox
        udp_port = self.textbox_udp_port.get("1.0", "end-1c")
        serial_port_name = self.textbox_serial_port.get("1.0", "end-1c")

        start_connection_controller(udp_port, serial_port_name, self.PATH_JSON_MODEL)

        self.label_connected.pack()

GUI()