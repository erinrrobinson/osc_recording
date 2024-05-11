import csv
import os
from pythonosc import dispatcher
from pythonosc import osc_server
from datetime import datetime

# Initialize variables
start_time = None
daily_counts = {}
records_dir = "PUT PATH HERE WHERE YOU WANT TO STORE FILES"
csv_recordinglog = os.path.join(records_dir, 'record_times.csv')
csv_counter = os.path.join(records_dir, 'counter.csv')
todays_date = datetime.now().strftime('%Y-%m-%d')

# os.makedirs(records_dir, exist_ok=True)

def record_handler(address, value):
    global start_time
    print(f"Received {value} on {address}")
    if value == 1:
        start_time = datetime.now()
    elif value == 0 and start_time:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        start_time_formatted = start_time.strftime('%H:%M:%S')
        end_time_formatted = end_time.strftime('%H:%M:%S')

        with open(csv_recordinglog, 'a', newline='') as file:
            writer = csv.writer(file)
            print(start_time_formatted + ' ' + end_time_formatted)
            writer.writerow([todays_date, start_time_formatted, end_time_formatted, duration])
        start_time = None  

def counter_handler(address, value):
    if value == 1:
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        if date in daily_counts:
            daily_counts[date] += 1
        else:
            daily_counts[date] = 1
        with open(csv_counter, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, time, 1, daily_counts[date]])

# OSC server setup
ip = 'YOUR COMPUTERS NETWORK IP ADDRESS (INTERNET NOT LOCAL)'
port = 12345
disp = dispatcher.Dispatcher()
disp.map("/record", record_handler)
disp.map("/counter", counter_handler)
server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print(f"Serving on {server.server_address}")
server.serve_forever()
