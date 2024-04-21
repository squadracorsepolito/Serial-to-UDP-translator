import tkinter as tk
from backend.functions import open_stream_udp
import threading

class GUI:
    PATH_DBC_CAN0 = None
    PATH_DBC_CAN1 = None
    connected = False

    def __init__(self):
        # Create a new instance of Tkinter application
        self.app = tk.Tk()

    # ---------- WINDOW SETTINGS ---------------------------------------
        self.app.title("SCanner Adapter")

        # Set the width and height of the window
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.window_width = 500
        self.window_height = 210
        self.x_coordinate = (self.screen_width - self.window_width) // 2
        self.y_coordinate = (self.screen_height - self.window_height) // 2

        # Set the geometry of the window to position it on the center of the screen
        self.app.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.app.iconbitmap('img/icon.ico')

    # ---------- GUI ELEMENTS --------------------------------------------
        self.label = tk.Label(self.app, text="Press connect to start converting Serial messages \nto JSON and stream them to UDP.")
        self.label.pack(pady=10)

        # Local UDP Port
        self.label_udp_port = tk.Label(self.app, text="Local UDP port:")
        self.label_udp_port.pack()
        self.textbox_udp_port = tk.Text(self.app, height=1, width=30)
        self.textbox_udp_port.insert("1.0", "1000")                        # Default UDP port
        self.textbox_udp_port.pack()

        # Connect button
        self.connect_button = tk.Button(self.app, text="Connect", command=self.connect_thread, font=("Arial", 14, "bold"), width=15, height=2)
        self.connect_button.pack(pady=15)

        # Connected status
        self.label_connected = tk.Label(self.app, text="CONNECTED!", font=("Arial", 14, "bold"))
        self.label_connected.forget()

        # Start the Tkinter event loop
        self.app.mainloop()

    # ---------- FUNCTIONS ---------------------------------------------
    def connect_thread(self):
        # Start a new thread for the connect function
        threading.Thread(target=self.connect, daemon=True).start()

    def connect(self):
        # Get the port from the textbox
        udp_port = self.textbox_udp_port.get("1.0", "end-1c")

        # TO DO: Add Serial connect functionality
        open_stream_udp(int(udp_port))

        self.label_connected.pack()

GUI()