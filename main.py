import tkinter as tk
from tkinter import filedialog
from backend.functions import start_connection_controller
import threading

class GUI:
    # Config parameters
    PATH_CONFIG_MODEL = "Path"
    VALUES=["example1", "example2", "example3"]
    NEWLINE=b'\n'
    SEPARATOR=b','
    BAUDRATE=9600
    UDP_PORT=5000
    SERIAL_PORT=b'/dev/ttyUSB0'

    # Flag
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

    # ---------- GUI ELEMENTS --------------------------------------------
        self.label = tk.Label(self.app, text="Press connect to start converting CSV Serial messages \nto JSON and stream them to UDP (localhost).")
        self.label.pack(pady=10)

        # Path to CONFIG
        self.label_path_config_model = tk.Label(self.app, text="Select path to CONFIG model to use:")
        self.label_path_config_model.pack()
        self.textbox_path_config_model = tk.Text(self.app, height=1, width=50)
        self.textbox_path_config_model.pack()
        self.textbox_path_config_model.insert("1.0", self.PATH_CONFIG_MODEL)
        self.browse_button_config_model = tk.Button(self.app, text="Browse", command=self.browse_file_config_model)
        self.browse_button_config_model.pack()

        # Local UDP Port
        self.label_udp_port = tk.Label(self.app, text="Local UDP port:")
        self.label_udp_port.pack()
        self.textbox_udp_port = tk.Text(self.app, height=1, width=30)
        self.textbox_udp_port.insert("1.0", self.UDP_PORT)                        
        self.textbox_udp_port.pack()

        # Serial Port
        self.label_serial_port = tk.Label(self.app, text="Serial port:")
        self.label_serial_port.pack()
        self.textbox_serial_port = tk.Text(self.app, height=1, width=30)
        self.textbox_serial_port.insert("1.0", self.SERIAL_PORT)                       
        self.textbox_serial_port.pack()

        # Connect button
        self.connect_button = tk.Button(self.app, text="Connect", command=self.connect_thread, font=("Arial", 14, "bold"), width=15, height=2)
        self.connect_button.pack(pady=15)

        # Connected status
        self.label_connected = tk.Label(self.app, text="CONNECTED!", font=("Arial", 14, "bold"))
        self.label_connected.forget()

        # Start the Tkinter event loop
        self.app.mainloop()

    # ---------- FUNCTIONS ---------------------------------------------
    def browse_file_config_model(self):
        global PATH_CONFIG_MODEL

        self.PATH_CONFIG_MODEL = filedialog.askopenfilename()
        self.textbox_path_config_model.delete("1.0", tk.END)
        self.textbox_path_config_model.insert("1.0", self.PATH_CONFIG_MODEL)

        self.startup()

    def connect_thread(self):
        # Start a new thread for the connect function
        threading.Thread(target=self.connect, daemon=True).start()

    def connect(self):
        # Get the port from the textbox
        UDP_PORT = self.textbox_udp_port.get("1.0", "end-1c")
        SERIAL_PORT = self.textbox_serial_port.get("1.0", "end-1c")
        self.save_to_config_file() # Save the paths to the CONFIG file for future reuse

        start_connection_controller(UDP_PORT, SERIAL_PORT, self.VALUES, self.NEWLINE, self.SEPARATOR, self.BAUDRATE)  

        self.label_connected.pack()
    
    def startup(self):
        config = {
            'VALUES': '',
            'NEWLINE': '',
            'SEPARATOR': '',
            'BAUDRATE': '',
            'UDP_PORT': '',
            'SERIAL_PORT': ''
        }
        with open(self.PATH_CONFIG_MODEL, 'r') as f:
            lines = f.readlines()
            if lines:
                for line in lines:
                    for key in config.keys():
                        if line.startswith(f'{key}='):
                            config[key] = line.split('=')[1].strip()
        self.VALUES = config['VALUES']
        self.NEWLINE = config['NEWLINE']
        self.SEPARATOR = config['SEPARATOR']
        self.BAUDRATE = config['BAUDRATE']
        self.UDP_PORT = config['UDP_PORT']
        self.SERIAL_PORT = config['SERIAL_PORT']

        # Update the interface with new values
        self.update_interface()

    def update_interface(self):
        self.textbox_udp_port.delete("1.0", tk.END)
        self.textbox_udp_port.insert("1.0", str(self.UDP_PORT))
        self.textbox_serial_port.delete("1.0", tk.END)
        self.textbox_serial_port.insert("1.0", str(self.SERIAL_PORT))
    
    def save_to_config_file(self):
        with open(self.PATH_CONFIG_MODEL, 'w') as f:
            f.write(f'VALUES={self.VALUES}\n')
            f.write(f'NEWLINE={self.NEWLINE}\n')
            f.write(f'SEPARATOR={self.SEPARATOR}\n')
            f.write(f'BAUDRATE={self.BAUDRATE}\n')
            f.write(f'UDP_PORT={self.UDP_PORT}\n')
            f.write(f'SERIAL_PORT={self.SERIAL_PORT}\n')

GUI()