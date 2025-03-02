# Ricart-Agrawala Algorithm for Mutual Exclusion

This project demonstrates the **Ricart-Agrawala algorithm** for mutual exclusion using **Python and UDP sockets**. It simulates multiple processes running on different terminals, communicating with each other to ensure safe access to a critical section.

Features

Implements Ricart-Agrawala Algorithm for distributed mutual exclusion

Uses UDP sockets for inter-process communication

Maintains a request queue to handle simultaneous requests

Introduces 1-second delay for message transmission (simulating real-world delays)

Executes the critical section for 2 seconds

Handles deferred requests correctly

## Prerequisites
- **Ubuntu** (or any Linux-based OS)
- **Python 3** (Install using `sudo apt update && sudo apt install python3 -y`)

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ricart-agrawala.git
   cd ricart-agrawala
   ```
2. **Create the Python script:**
   ```bash
   nano ricart_agrawala.py
   ```
   - Copy & paste the code from `ricart_agrawala.py`
   - Save the file (`Ctrl + X`, then `Y`, then `Enter`)

3. **Run the program on multiple terminals:**
   ```bash
   python3 ricart_agrawala.py
   ```
   - Enter **Process ID (1, 2, or 3)** in each terminal.

## How It Works
- Each process can request access to a **critical section (CS)**.
- If multiple processes request CS at the same time, the algorithm follows these rules:
  - **Lowest timestamp wins** (earliest request gets priority)
  - Other requests are **deferred and queued**
  - Once the CS is released, deferred requests are granted access
- Communication is handled using **UDP sockets**.

## Usage
1. **Start 3 terminals** and run the script in each.
2. When prompted, enter a **Process ID (1, 2, or 3)**.
3. **Press ENTER** to request the critical section.
4. The algorithm will handle access and message passing automatically.

## Expected Output
```
[1709143201] Process 1 is REQUESTING critical section
[1709143202] Process 2 is REQUESTING critical section
[1709143203] Process 3 is REQUESTING critical section
[1709143204] Process 2 request is DEFERRED by 1
[1709143204] Process 3 request is DEFERRED by 1
[1709143206] Process 1 ENTERING critical section
[1709143208] Process 1 EXITING critical section
[1709143209] Process 1 sends REPLY to deferred Process 2
[1709143210] Process 1 sends REPLY to deferred Process 3
[1709143211] Process 2 ENTERING critical section
```



