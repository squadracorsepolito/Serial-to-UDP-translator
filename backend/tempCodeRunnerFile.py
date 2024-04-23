import socket
import threading
import json
import time
import serial
import json

# Constants
LOCALHOST_IP = "127.0.0.1"
BUFFER_SIZE = 1024
TIMEOUT = 1

# Controller
def start_connection_controller(UDP_PORT, SERIAL_PORT, VALUES, NEWLINE, SEPARATOR, BAUDRATE):
    udp_socket = open_stream_udp(int(UDP_PORT))
    ser_socket = open_stream_serial(SERIAL_PORT, BAUDRATE)
    time.sleep(1)
    if udp_socket and ser_socket:
        print("Connection established")
        read_serial_data(ser_socket, VALUES, NEWLINE, SEPARATOR, UDP_PORT)

    
# Open serial connection to the specified port
def open_stream_serial(SERIAL_PORT, BAUDRATE):
    try:
        # Open serial connection
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
        if ser:
            print(f"Serial port {SERIAL_PORT} is open")
        return ser
    except serial.SerialException as e:
        print(f"Failed to open serial port {SERIAL_PORT}: {e}")

# Open a UDP JSON streaming server on the specified port
def open_stream_udp(UDP_PORT):
    try:
        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if server_socket:
            print(f"UDP JSON server is active on port {UDP_PORT}")
        return server_socket

    except Exception as e:
        print(f"Error opening JSON streaming server: {e}")

# Read data from the serial port
def read_serial_data(ser, VALUES, NEWLINE, SEPARATOR, UDP_PORT):
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
                    while NEWLINE in data_buffer:
                        # Find the index of the first comma
                        line_index = data_buffer.find(NEWLINE)
                        
                        # Extract the line up to the comma
                        line = data_buffer[:line_index + 1]
                        
                        # Remove the extracted line from the buffer
                        data_buffer = data_buffer[line_index + len(NEWLINE):]
                        
                        # Process the line (conver to json and send it to the UDP server)
                        csv_to_json(line, UDP_PORT, VALUES, SEPARATOR)

            except serial.SerialException as e:
                print(f"Serial error occurred: {e}")
                break
        return data_buffer
    
    # Start the thread to read data from the serial port
    read_serial_thread = threading.Thread(target=read_data_handler, daemon=True)
    read_serial_thread.start()

# Converter Serial CSV stream to JSON converter
def csv_to_json(message_csv, UDP_PORT, VALUES, SEPARATOR):
    # Read the configuration from the JSON file
    config_data = read_config(config_file)
    if config_data is None:
        return
    
    # Split the CSV data by comma
    csv_parts = message_csv.strip().split(SEPARATOR)

    # Initialize a dictionary to hold the JSON data
    json_data = {}

    # Loop through each value and its corresponding csv part
    for value, csv_part in zip(VALUES, csv_parts):
        # Check if the csv part is not NULL
        if csv_part != "NULL":
            # Add the value and csv part to the json_data dictionary
            json_data[value] = int(csv_part)

    # Send the data to the UDP server
    send_json_to_udp(json_data, UDP_PORT)

# Send JSON data to the UDP server
def send_json_to_udp(json_data, UDP_PORT):
    try:
        # Send JSON data to the server
        client_socket.sendto(json_data.encode(), (LOCALHOST_IP, UDP_PORT))    # Check with cmd:  nc -ul <UDP_PORT>

    except Exception as e:
        print(f"Error sending JSON data to UDP server: {e}")