import tkinter as tk
from tkinter import filedialog
from backend.functions import start_connection_controller, disconnect
import threading
import time

class GUI:
    def __init__(self):    

        # Create a new instance of Tkinter application
        self.app = tk.Tk()

        # Config parameters
        self.PATH_CONFIG_MODEL = "Path"
        self.VALUES=['example1','example2','example3']
        self.NEWLINE=';'
        self.SEPARATOR=','
        self.BAUDRATE=9600
        self.UDP_PORT=5000
        self.SERIAL_PORT='/dev/ttyUSB0'

        # Flag
        self.connected = False

        global controller_thread
        controller_thread = None

    # ---------- WINDOW SETTINGS ---------------------------------------
        self.app.title("Serial CSV to UDP JSON Translator")

        # Set the width and height of the window
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.window_width = 500
        self.window_height = 580
        self.x_coordinate = (self.screen_width - self.window_width) // 2
        self.y_coordinate = (self.screen_height - self.window_height) // 2

        # Set the geometry of the window to position it on the center of the screen
        self.app.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.frame = tk.Frame(self.app)
        self.frame.pack(pady=20)

    # ---------- GUI ELEMENTS --------------------------------------------
        self.label = tk.Label(self.frame, text="Press connect to start converting CSV Serial messages \nto JSON and stream them to UDP (localhost).")
        self.label.grid(row=0, column=1, columnspan=10, pady=10)

        # Path to CONFIG
        self.label_path_config_model = tk.Label(self.frame, text="Select path to CONFIG model to use:")
        self.label_path_config_model.grid(row=1, column=1, columnspan=10)
        self.textbox_path_config_model = tk.Text(self.frame, height=1, width=50)
        self.textbox_path_config_model.grid(row=2, column=1, columnspan=10)
        self.textbox_path_config_model.insert("1.0", self.PATH_CONFIG_MODEL)
        self.browse_button_config_model = tk.Button(self.frame, text="Browse", command=self.browse_file_config_model)
        self.browse_button_config_model.grid(row=3, column=1, columnspan=10, pady=10)

        # Values
        self.label_values = tk.Label(self.frame, text="Insert data label values, separated by spaces:")
        self.label_values.grid(row=4, column=1, columnspan=10)
        self.textbox_values = tk.Text(self.frame, height=1, width=50)
        self.textbox_values.insert("1.0", self.VALUES)                        
        self.textbox_values.grid(row=5, column=1, columnspan=10)

        # Newline
        self.label_newline = tk.Label(self.frame, text="Insert newline separator for the upcoming CSV stream. \nInsert LF->'\\n' and CRLF->'\\r\\n':")
        self.label_newline.grid(row=6, column=1, columnspan=10)
        self.textbox_newline = tk.Text(self.frame, height=1, width=30)
        self.textbox_newline.insert("1.0", self.NEWLINE)                        
        self.textbox_newline.grid(row=7, column=1, columnspan=10)

        # Separator
        self.label_separator = tk.Label(self.frame, text="Insert single data separator for the upcoming CSV stream:")
        self.label_separator.grid(row=8, column=1, columnspan=10)
        self.textbox_separator = tk.Text(self.frame, height=1, width=30)
        self.textbox_separator.insert("1.0", self.SEPARATOR)                        
        self.textbox_separator.grid(row=9, column=1, columnspan=10)

        # Baudrate
        self.label_baudrate = tk.Label(self.frame, text="Insert baudrate of the serial signal:")
        self.label_baudrate.grid(row=10, column=1, columnspan=10)
        self.textbox_baudrate = tk.Text(self.frame, height=1, width=30)
        self.textbox_baudrate.insert("1.0", self.BAUDRATE)                        
        self.textbox_baudrate.grid(row=11, column=1, columnspan=10)

        # Local UDP Port
        self.label_udp_port = tk.Label(self.frame, text="Local UDP port:")
        self.label_udp_port.grid(row=12, column=1, columnspan=10)
        self.textbox_udp_port = tk.Text(self.frame, height=1, width=30)
        self.textbox_udp_port.insert("1.0", self.UDP_PORT)                        
        self.textbox_udp_port.grid(row=13, column=1, columnspan=10)

        # Serial Port
        self.label_serial_port = tk.Label(self.frame, text="Serial port:")
        self.label_serial_port.grid(row=14, column=1, columnspan=10)
        self.textbox_serial_port = tk.Text(self.frame, height=1, width=30)
        self.textbox_serial_port.insert("1.0", self.SERIAL_PORT)                       
        self.textbox_serial_port.grid(row=15, column=1, columnspan=10)

        # Connect button
        self.connect_button = tk.Button(self.frame, text="Connect", command=self.connect_thread, font=("Arial", 14, "bold"), width=7, height=2)
        self.connect_button.grid(row=16, column=0, columnspan=5, pady=15)

        # Disconnect button
        self.disconnect_button = tk.Button(self.frame, text="Disconnect", command=self.disconnect, font=("Arial", 14, "bold"), width=7, height=2, state="disabled")
        self.disconnect_button.grid(row=16, column=7, columnspan=5, pady=15)

        # Connected status
        self.label_connected = tk.Label(self.frame, text="CONNECTED!", font=("Arial", 14, "bold"))
        self.label_connected.grid_forget()

        # CONFIG status
        self.label_config_loaded = tk.Label(self.frame, text="CONFIG loaded!", font=("Arial", 14, "bold"))
        self.label_config_loaded.grid_forget()

        # Start the Tkinter event loop
        self.app.mainloop()

    # ---------- FUNCTIONS ---------------------------------------------
    def browse_file_config_model(self):
        global PATH_CONFIG_MODEL

        self.PATH_CONFIG_MODEL = filedialog.askopenfilename()
        self.textbox_path_config_model.delete("1.0", tk.END)
        self.textbox_path_config_model.insert("1.0", self.PATH_CONFIG_MODEL)

        self.label_config_loaded.grid(row=17, column=1, columnspan=10)
        self.startup()

    def connect_thread(self):
        global controller_thread
        # Start a new thread for the connect function
        controller_thread = threading.Thread(target=self.connect, daemon=True)
        controller_thread.start()

    def connect(self):
        # Get the port from the textbox
        self.UDP_PORT = self.textbox_udp_port.get("1.0", "end-1c")
        self.SERIAL_PORT = self.textbox_serial_port.get("1.0", "end-1c")
        self.VALUES = self.textbox_values.get("1.0", "end-1c").replace(" ", ",").split(",")
        self.NEWLINE = self.textbox_newline.get("1.0", "end-1c")
        self.SEPARATOR = self.textbox_separator.get("1.0", "end-1c")
        self.BAUDRATE = self.textbox_baudrate.get("1.0", "end-1c")
        self.save_to_config_file() # Save the data to the CONFIG file for future reuse

        start_connection_controller(self.UDP_PORT, self.SERIAL_PORT, self.VALUES, self.NEWLINE, self.SEPARATOR, self.BAUDRATE, self.label_connected, self.connect_button, self.disconnect_button)  
    
    def disconnect(self):
        global controller_thread
        # Stop the controller thread if it's running
        if controller_thread:
            disconnect()
            time.sleep(1)
            controller_thread.join()
            self.connect_button.config(state="active")
            self.disconnect_button.config(state="disabled")
            self.label_connected.grid_forget()
            self.label_config_loaded.grid_forget()
            controller_thread = None
            print("Disconnected")
        else:
            return

    def startup(self):
        with open(self.PATH_CONFIG_MODEL, 'r') as f:
            for line in f:
                name, value = line.strip().split('=')
                if name == 'BAUDRATE':
                    self.BAUDRATE = value
                elif name == 'NEWLINE':
                    self.NEWLINE = value
                elif name == 'SEPARATOR':
                    self.SEPARATOR = value
                elif name == 'UDP_PORT':
                    self.UDP_PORT = value
                elif name == 'SERIAL_PORT':
                    self.SERIAL_PORT = value
                elif name == 'VALUES':
                    self.VALUES = value

        # Update the interface with new values
        self.update_interface()

    def update_interface(self):
        self.textbox_udp_port.delete("1.0", tk.END)
        self.textbox_udp_port.insert("1.0", str(self.UDP_PORT))
        self.textbox_serial_port.delete("1.0", tk.END)
        self.textbox_serial_port.insert("1.0", str(self.SERIAL_PORT))
        self.textbox_values.delete("1.0", tk.END)
        self.textbox_values.insert("1.0", str(self.VALUES))
        self.textbox_newline.delete("1.0", tk.END)
        self.textbox_newline.insert("1.0", str(self.NEWLINE))
        self.textbox_separator.delete("1.0", tk.END)
        self.textbox_separator.insert("1.0", str(self.SEPARATOR))
        self.textbox_baudrate.delete("1.0", tk.END)
        self.textbox_baudrate.insert("1.0", str(self.BAUDRATE))
    
    def save_to_config_file(self):
        values_string = " ".join(self.VALUES)

        if self.PATH_CONFIG_MODEL != "Path":
            with open(self.PATH_CONFIG_MODEL, 'w') as f:
                f.write(f'VALUES={values_string}\n')
                f.write(f'NEWLINE={self.NEWLINE}\n')
                f.write(f'SEPARATOR={self.SEPARATOR}\n')
                f.write(f'BAUDRATE={self.BAUDRATE}\n')
                f.write(f'UDP_PORT={self.UDP_PORT}\n')
                f.write(f'SERIAL_PORT={self.SERIAL_PORT}')

GUI()