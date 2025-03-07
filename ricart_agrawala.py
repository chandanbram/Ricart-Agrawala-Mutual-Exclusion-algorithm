import socket
import threading
import time
import json

# Process details
processes = {
    1: ('127.0.0.1', 5001),
    2: ('127.0.0.1', 5002),
    3: ('127.0.0.1', 5003)
}

# Initialize process variables
REQUESTING = False
REPLY_COUNT = 0
timestamp = 0
deferred_requests = []

# Get process ID from user
pid = int(input("Enter Process ID (1, 2, or 3): "))
assert pid in processes, "Invalid Process ID"

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(processes[pid])

def send_message(target_pid, message):
    """ Send message to a process with 1-second delay """
    time.sleep(1)  # Introduce delay before sending
    sock.sendto(json.dumps(message).encode(), processes[target_pid])

def listener():
    """ Listens for incoming messages """
    global REQUESTING, REPLY_COUNT, timestamp, deferred_requests
    while True:
        data, addr = sock.recvfrom(1024)
        msg = json.loads(data.decode())

        time.sleep(1)  # Introduce 1-second delay for message processing

        if msg["type"] == "REQUEST":
            print(f"[{time.time()}] Process {msg['pid']} requests CS with timestamp {msg['timestamp']}")

            # If not requesting, or other process has a smaller timestamp
            if not REQUESTING or (msg["timestamp"], msg["pid"]) < (timestamp, pid):
                print(f"[{time.time()}] Process {msg['pid']} gets immediate REPLY from {pid}")
                send_message(msg["pid"], {"type": "REPLY", "pid": pid})
            else:
                print(f"[{time.time()}] Process {msg['pid']} request is DEFERRED by {pid}")
                deferred_requests.append(msg["pid"])

        elif msg["type"] == "REPLY":
            print(f"[{time.time()}] Received REPLY from Process {msg['pid']}")
            REPLY_COUNT += 1

threading.Thread(target=listener, daemon=True).start()

def request_critical_section():
    """ Request access to critical section """
    global REQUESTING, REPLY_COUNT, timestamp
    REQUESTING = True
    REPLY_COUNT = 0
    timestamp = int(time.time())

    print(f"[{timestamp}] Process {pid} is REQUESTING critical section")

    for p in processes:
        if p != pid:
            send_message(p, {"type": "REQUEST", "pid": pid, "timestamp": timestamp})

    # **Added Delay to Wait for Other Requests**
    time.sleep(5)

    while REPLY_COUNT < len(processes) - 1:
        time.sleep(0.1)

    print(f"[{time.time()}] Process {pid} ENTERING critical section")
    time.sleep(2)  # Reduced to 2 seconds for execution
    print(f"[{time.time()}] Process {pid} EXITING critical section")

    REQUESTING = False

    # Send replies to all deferred processes
    for p in deferred_requests:
        send_message(p, {"type": "REPLY", "pid": pid})
        print(f"[{time.time()}] Process {pid} sends REPLY to deferred Process {p}")

    deferred_requests.clear()

# Main loop
while True:
    cmd = input("Press ENTER to request critical section...\n")
    request_critical_section()
