import socket
import threading
import json
import time

# Constants
LOCALHOST_IP = "127.0.0.1"
    
# Open serial connection to the specified port
def open_stream_serial(port):
    return True

# Opens a UDP JSON streaming server on the specified port
def open_stream_udp(port):
    try:
        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print(f"UDP JSON streaming server is streaming on port {port}")

        def handle_client():
            try:
                while True:
                    # Generate JSON data (replace with your actual data)
                    example_json_data = {'Engine_Speed': 0, 'Inlet_Manifold_Pressure': 97.6, 'Inlet_Air_Temperature': 32, 'Throttle_Position': 17.3}
                    print(f"Sending JSON data to port {port}: {example_json_data}")
                    
                    # Convert JSON data to string
                    json_str = json.dumps(example_json_data)

                    # Send JSON data to the client
                    server_socket.sendto(json_str.encode(), (LOCALHOST_IP, port))   # Check with cmd:  nc -ul 9870

                    time.sleep(1)
            except Exception as e:
                print(f"Error handling client connection: {e}")

        # Start the thread to handle PlotJuggler connections
        stream_udp_thread = threading.Thread(target=handle_client, daemon=True)
        stream_udp_thread.start()

    except Exception as e:
        print(f"Error opening JSON streaming server: {e}")

# Serial CSV stream to UDP JSON converter
def csv_to_json(message_csv):
    return True
