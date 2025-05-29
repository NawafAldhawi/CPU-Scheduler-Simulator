# 🧠 CPU Scheduler Simulator

This project simulates multiple CPU scheduling algorithms and analyzes their performance. It calculates **average turnaround time**, **waiting time**, and **response time**, and also generates a **Gantt chart** to visualize the order of process execution.

## 💡 Features

- Simulates the following CPU scheduling algorithms:
  - **First-Come, First-Served (FCFS)**
  - **Round Robin (RR)**
  - **Shortest Time Remaining First (STRF)**
  - **Custom Priority Queue** (e.g., `Regular_Visitors_Priority_Queue`)
- Calculates key performance metrics:
  - **Average Turnaround Time**
  - **Average Waiting Time**
  - **Average Response Time**
- Displays a clear **Gantt Chart** of execution order

## 🚀 Getting Started

To run the simulation, simply modify the last few lines in the main file:

```python
# Choose your scheduling algorithm:
queueTest = Regular_Visitors_Priority_Queue()  
# Alternatives: FCFS(), RR(), STRF()

# Define your processes in the format:
# Process(pid, burst_time, arrival_time, familiarity)
p1 = Process(1, 3, 0, 0)
p2 = Process(2, 1, 3, 0)
p3 = Process(3, 4, 2, 0)
p4 = Process(4, 5, 0, 0)

# Add your processes to the list
lst = [p1, p2, p3, p4]

# Load and simulate
queueTest.load_processes(lst)
queueTest.handle_queue()
