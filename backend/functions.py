import socket
import threading
import json
import time
import serial
import json

# Constants
LOCALHOST_IP = "127.0.0.1"
LINE_SEPARATOR = b'\n'
BAUDRATE = 9600
TIMEOUT = 1
BUFFER_SIZE = 1024

# Controller
def start_connection_controller(udp_port, serial_port_name, path_json_model):
    udp_socket = open_stream_udp(int(udp_port))
    ser_socket = open_stream_serial(serial_port_name)
    time.sleep(1)
    if udp_socket and ser_socket:
        print("Connection established")
        read_serial_data(ser_socket, path_json_model) 

    
# Open serial connection to the specified port
def open_stream_serial(port):
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate=BAUDRATE, timeout=TIMEOUT)
        if ser:
            print(f"Serial port {port} is open")
        return ser
    except serial.SerialException as e:
        print(f"Failed to open serial port {port}: {e}")

# Open a UDP JSON streaming server on the specified port
def open_stream_udp(port):
    try:
        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if server_socket:
            print(f"UDP JSON server is streaming on port {port}")
        return server_socket

    except Exception as e:
        print(f"Error opening JSON streaming server: {e}")

# Read data from the serial port
def read_serial_data(ser, config_file):
    data_buffer = bytearray()  # Initialize an empty buffer to store data
    def read_data_handler():
        while True:
            try:
                # Read data from the serial port
                data = ser.read(BUFFER_SIZE)
                if data:
                    # Append the received data to the buffer
                    data_buffer.extend(data)
                    
                    # Check if there's a complete line terminated by a comma
                    while LINE_SEPARATOR in data_buffer:
                        # Find the index of the first comma
                        line_index = data_buffer.find(LINE_SEPARATOR)
                        
                        # Extract the line up to the comma
                        line = data_buffer[:line_index + 1]
                        
                        # Remove the extracted line from the buffer
                        data_buffer = data_buffer[line_index + len(LINE_SEPARATOR):]
                        
                        # Process the line (conver to json and send it to the UDP server)
                        csv_to_json(line, udp_port, config_file)

            except serial.SerialException as e:
                print(f"Serial error occurred: {e}")
                break
        return data_buffer
    
    # Start the thread to read data from the serial port
    read_serial_thread = threading.Thread(target=read_data_handler, daemon=True)
    read_serial_thread.start()

# Converter Serial CSV stream to JSON converter
def csv_to_json(message_csv, udp_port, config_file):
    # Read the configuration from the JSON file
    config_data = read_config(config_file)
    if config_data is None:
        return
    
    # Split the CSV data by comma
    csv_parts = message_csv.strip().split(b',')

    # Initialize a dictionary to hold the JSON data
    json_data = {}

    # Populate the JSON data using the configuration
    for idx, csv_part in enumerate(csv_parts):
        signal_name = f"nome_segnale{idx}"
        if signal_name in config_data:
            key = config_data[signal_name]
            json_data[signal_name] = csv_part.decode()

    # Send the data to the UDP server
    send_json_to_udp(json_data, udp_port)

# Send JSON data to the UDP server
def send_json_to_udp(json_data, udp_port):
    try:
        # Send JSON data to the server
        client_socket.sendto(json_data.encode(), (LOCALHOST_IP, udp_port))    # Check with cmd:  nc -ul 9870

    except Exception as e:
        print(f"Error sending JSON data to UDP server: {e}")

# Read the JSON configuration from the provided file
def read_config(config_file):
    try:
        with open(config_file) as f:
            config_data = json.load(f)
        return config_data
    except FileNotFoundError:
        print("Config file not found.")
        return None