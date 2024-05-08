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

udp_socket = None
ser_socket = None

# Controller
def start_connection_controller(UDP_PORT, SERIAL_PORT, VALUES, NEWLINE, SEPARATOR, BAUDRATE, label_connected, connect_button, disconnect_button):
    global udp_socket, ser_socket
    udp_socket = open_stream_udp(int(UDP_PORT))
    ser_socket = open_stream_serial(SERIAL_PORT, BAUDRATE)
    time.sleep(1)
    
    if udp_socket and ser_socket:
        print("Connection established")
        read_serial_data(ser_socket, udp_socket, VALUES, NEWLINE, SEPARATOR, UDP_PORT)
        label_connected.grid(row=18, column=1, columnspan=10)
        connect_button.config(state="disabled")
        disconnect_button.config(state="active")
    else:
        disconnect()
        print("Failed to establish connection, disconnecting...")
    
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
def read_serial_data(ser_socket, udp_socket, VALUES, NEWLINE, SEPARATOR, UDP_PORT):
    data_buffer = ""

    # NEWLINE translation of special characters
    if NEWLINE == "LF":
        NEWLINE = "\n"
    elif NEWLINE == "CRLF":
        NEWLINE = "\r\n"

    def read_data_handler(data_buffer):
        while True:
            try:
                # Read data from the serial port
                data = ser_socket.read(BUFFER_SIZE).decode('utf-8')
            
                if data:
                    # Append the received data to the buffer
                    data_buffer += data
                    
                    # Check if there's a complete line terminated by a newline character
                    while NEWLINE in data_buffer:
                        # Find the index of the first newline character
                        line_index = data_buffer.find(NEWLINE)
                    
                        # Extract the line up to the newline character
                        line = data_buffer[:line_index + 1]
                        
                        # Remove the extracted line from the buffer
                        data_buffer = data_buffer[line_index + len(NEWLINE):]

                        #print(f"Received line: {line}") #DEBUG
                        
                        # Process the line (convert to json and send it to the UDP server)
                        csv_to_json(udp_socket, line, UDP_PORT, VALUES, SEPARATOR)

            except serial.SerialException as e:
                break
            except Exception as e:
                print(f"Error occurred in the serial data handler: {e}")
                break
    
    # Start the thread to read data from the serial port
    read_serial_thread = threading.Thread(target=read_data_handler, args=(data_buffer,), daemon=True)
    read_serial_thread.start()

# Converter Serial CSV stream to JSON converter
def csv_to_json(udp_socket, line_csv, UDP_PORT, VALUES, SEPARATOR):
    try:
        # Split the CSV data by comma
        csv_parts = line_csv.strip().split(SEPARATOR)

        # Initialize a dictionary to hold the JSON data
        json_data = {}

        # Loop through each value and its corresponding csv part
        for value, csv_part in zip(VALUES, csv_parts):
            # Check if the csv part is not NULL
            if value != "NOPE":
                # Convert value to int or float if possible
                try:
                    csv_part = int(csv_part)  # Try converting to integer
                except ValueError:
                    try:
                        csv_part = float(csv_part)  # Try converting to float
                    except ValueError:
                        pass  # If not convertible, keep the value as string

                # Add the value and csv part to the json_data dictionary
                json_data[value] = csv_part

        # Send the data to the UDP server
        send_json_to_udp(udp_socket, json_data, UDP_PORT)

    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")

# Send JSON data to the UDP server
def send_json_to_udp(udp_socket, json_data, UDP_PORT):
    try:
        # Serialize the JSON data to a string
        json_bytes = json.dumps(json_data).encode('utf-8')
        # Send JSON data to the server
        udp_socket.sendto(json_bytes, (LOCALHOST_IP, int(UDP_PORT)))    # Check with cmd:  nc -ul <UDP_PORT>
        #print(f"Sending JSON data: {json_data}")  #DEBUG

    except Exception as e:
        print(f"Error sending JSON data to UDP server: {e}")

# Disconnect from the serial and UDP servers
def disconnect():
    try:
        global udp_socket, ser_socket
        if udp_socket:
            udp_socket.close()
        if ser_socket:
            ser_socket.close()
    except Exception as e:
        print(f"Error disconnecting: {e}")