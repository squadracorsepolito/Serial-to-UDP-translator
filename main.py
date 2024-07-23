import tkinter as tk
from tkinter import filedialog
from backend.functions import start_connection_controller, disconnect
import threading
import time
import argparse

class GUI:
    def __init__(self, config_path=None, autodetect=None,direct_connect=False):    
        # Config parameters
        self.PATH_CONFIG_MODEL = "Path"
        self.VALUES=''
        self.NEWLINE=';'
        self.SEPARATOR=','
        self.BAUDRATE=9600
        self.UDP_PORT=5000
        self.SERIAL_PORT='/dev/ttyUSB0'
        self.AUTO_DETECT=False
        self.AUTO_DETECT_FLAG="###"

        global controller_thread
        controller_thread = None
        self.connect_button = None
        self.label_connected = None
        self.label_connected = None
        self.disconnect_button = None
        
        # Load configuration if a path was provided
        if config_path:
            self.PATH_CONFIG_MODEL = config_path
            self.startup()

        if autodetect:
            self.AUTO_DETECT = True
            self.AUTO_DETECT_FLAG = autodetect

        if direct_connect:
            self.connect_thread(direct=True)
            return

        # Create a new instance of Tkinter application
        self.app = tk.Tk()

    # ---------- WINDOW SETTINGS ---------------------------------------
        self.app.title("Serial CSV to UDP JSON Translator")

        # Set the width and height of the window
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.window_width = 500
        self.window_height = 650
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

        # Autodetect values
        self.label_autodetect_values = tk.Label(self.frame, text="Check the box if you want to autodetect the values, \nspecify the special line starter value:")
        self.label_autodetect_values.grid(row=4, column=1, columnspan=10)
        self.auto_detect_var = tk.BooleanVar()
        if self.AUTO_DETECT == True:
            self.auto_detect_var.set(True)
        self.checkbox_autodetect = tk.Checkbutton(self.frame, text="Autodetect", variable=self.auto_detect_var)
        self.checkbox_autodetect.grid(row=5, column=0, columnspan=10)
        self.textbox_autodetect_values = tk.Text(self.frame, height=1, width=10)
        self.textbox_autodetect_values.insert("1.0", self.AUTO_DETECT_FLAG)                        
        self.textbox_autodetect_values.grid(row=5, column=6, columnspan=10)

        # Values
        self.label_values = tk.Label(self.frame, text="OR insert data label values, separated by the value you specify below:")
        self.label_values.grid(row=6, column=1, columnspan=10)
        self.textbox_values = tk.Text(self.frame, height=1, width=50)
        self.textbox_values.insert("1.0", self.VALUES)                        
        self.textbox_values.grid(row=7, column=1, columnspan=10)

        # Newline
        self.label_newline = tk.Label(self.frame, text="Insert newline separator for the upcoming CSV stream. \nInsert LF->'\\n' and CRLF->'\\r\\n':")
        self.label_newline.grid(row=8, column=1, columnspan=10)
        self.textbox_newline = tk.Text(self.frame, height=1, width=30)
        self.textbox_newline.insert("1.0", self.NEWLINE)                        
        self.textbox_newline.grid(row=9, column=1, columnspan=10)

        # Separator
        self.label_separator = tk.Label(self.frame, text="Insert single data separator for the upcoming CSV stream:")
        self.label_separator.grid(row=10, column=1, columnspan=10)
        self.textbox_separator = tk.Text(self.frame, height=1, width=30)
        self.textbox_separator.insert("1.0", self.SEPARATOR)                        
        self.textbox_separator.grid(row=11, column=1, columnspan=10)

        # Baudrate
        self.label_baudrate = tk.Label(self.frame, text="Insert baudrate of the serial signal:")
        self.label_baudrate.grid(row=12, column=1, columnspan=10)
        self.textbox_baudrate = tk.Text(self.frame, height=1, width=30)
        self.textbox_baudrate.insert("1.0", self.BAUDRATE)                        
        self.textbox_baudrate.grid(row=13, column=1, columnspan=10)

        # Local UDP Port
        self.label_udp_port = tk.Label(self.frame, text="Local UDP port:")
        self.label_udp_port.grid(row=14, column=1, columnspan=10)
        self.textbox_udp_port = tk.Text(self.frame, height=1, width=30)
        self.textbox_udp_port.insert("1.0", self.UDP_PORT)                        
        self.textbox_udp_port.grid(row=15, column=1, columnspan=10)

        # Serial Port
        self.label_serial_port = tk.Label(self.frame, text="Serial port:")
        self.label_serial_port.grid(row=16, column=1, columnspan=10)
        self.textbox_serial_port = tk.Text(self.frame, height=1, width=30)
        self.textbox_serial_port.insert("1.0", self.SERIAL_PORT)                       
        self.textbox_serial_port.grid(row=17, column=1, columnspan=10)

        # Connect button
        self.connect_button = tk.Button(self.frame, text="Connect", command=self.connect_thread, font=("Arial", 14, "bold"), width=8, height=2)
        self.connect_button.grid(row=18, column=0, columnspan=5, pady=15)

        # Disconnect button
        self.disconnect_button = tk.Button(self.frame, text="Disconnect", command=self.disconnect, font=("Arial", 14, "bold"), width=8, height=2, state="disabled")
        self.disconnect_button.grid(row=18, column=7, columnspan=5, pady=15)

        # Connected status
        self.label_connected = tk.Label(self.frame, text="CONNECTED!", font=("Arial", 14, "bold"))
        self.label_connected.grid_forget()

        # CONFIG status
        self.label_config_loaded = tk.Label(self.frame, text="CONFIG loaded!", font=("Arial", 14, "bold"))
        self.label_config_loaded.grid_forget()

        # Load config if provided
        if config_path:
            self.PATH_CONFIG_MODEL = config_path
            self.startup()
            self.update_interface()

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
        # Update the interface with new values
        self.update_interface()

    def connect_thread(self, direct=False):
        global controller_thread
        # Start a new thread for the connect function
        controller_thread = threading.Thread(target=self.connect, args=(direct,), daemon=True)
        controller_thread.start()

    def connect(self, direct=False):
        if not direct:
            # Get the port from the textbox
            if hasattr(self, 'textbox_udp_port'):
                self.UDP_PORT = self.textbox_udp_port.get("1.0", "end-1c")
            if hasattr(self, 'textbox_serial_port'):
                self.SERIAL_PORT = self.textbox_serial_port.get("1.0", "end-1c")
            if hasattr(self, 'textbox_values'):
                self.VALUES = self.textbox_values.get("1.0", "end-1c").replace(" ", ",").split(",")
            if hasattr(self, 'textbox_newline'):
                self.NEWLINE = self.textbox_newline.get("1.0", "end-1c")
            if hasattr(self, 'textbox_separator'):
                self.SEPARATOR = self.textbox_separator.get("1.0", "end-1c")
            if hasattr(self, 'textbox_baudrate'):
                self.BAUDRATE = self.textbox_baudrate.get("1.0", "end-1c")
            if hasattr(self, 'auto_detect_var'):
                self.AUTO_DETECT = self.auto_detect_var.get()
            if hasattr(self, 'textbox_autodetect_values'):
                self.AUTO_DETECT_FLAG = self.textbox_autodetect_values.get("1.0", "end-1c")
            self.save_to_config_file() # Save the data to the CONFIG file for future reuse

        try:
            start_connection_controller(self.UDP_PORT, self.SERIAL_PORT, self.VALUES, self.NEWLINE, self.SEPARATOR, self.BAUDRATE, 
                                        self.AUTO_DETECT, self.AUTO_DETECT_FLAG, self.label_connected, self.connect_button, self.disconnect_button)
        except Exception as e:
            print(f"Connection failed: {e}")

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
                    self.VALUES = value.replace(' ', '_').strip()
                elif name == 'AUTO_DETECT':
                    self.AUTO_DETECT = value
                elif name == 'AUTO_DETECT_FLAG':
                    self.AUTO_DETECT_FLAG = value

    def update_interface(self):
        self.textbox_path_config_model.delete("1.0", tk.END)
        self.textbox_path_config_model.insert("1.0", self.PATH_CONFIG_MODEL)
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
        self.textbox_autodetect_values.delete("1.0", tk.END)
        self.textbox_autodetect_values.insert("1.0", str(self.AUTO_DETECT_FLAG))
    
    def save_to_config_file(self):
        values_string = ",".join(self.VALUES)

        if self.PATH_CONFIG_MODEL != "Path":
            with open(self.PATH_CONFIG_MODEL, 'w') as f:
                f.write(f'VALUES={values_string}\n')
                f.write(f'AUTO_DETECT={self.AUTO_DETECT}\n')
                f.write(f'AUTO_DETECT_FLAG={self.AUTO_DETECT_FLAG}\n')
                f.write(f'NEWLINE={self.NEWLINE}\n')
                f.write(f'SEPARATOR={self.SEPARATOR}\n')
                f.write(f'BAUDRATE={self.BAUDRATE}\n')
                f.write(f'UDP_PORT={self.UDP_PORT}\n')
                f.write(f'SERIAL_PORT={self.SERIAL_PORT}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Serial CSV to UDP JSON Translator GUI.")
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    parser.add_argument('--autodetect', type=str, help='Autodetect values from the serial stream, specify the special line starter value')
    parser.add_argument('--nogui', action='store_true', default=False, help='Connect directly without showing the GUI')
    args = parser.parse_args()

    gui = GUI(config_path=args.config, autodetect=args.autodetect,direct_connect=args.nogui)