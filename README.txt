# CPU-Scheduler-Simulator
This program aims to simulate multiple different CPU scheduling algorithms (FCFS, RR, STRF,  Custom Queue), and
calulate their Average turnaround, waiting, and response times, while also showing the order of execution
through a Gaut Chart representation.

To run the program you can simply modify the last 8 lines of the code accordingly:

##########################
queueTest = Regular_Visitors_Priority_Queue() #change to other queues: FCFS(), RR(), STRF()

#you can adjust processes attributes in this order#
# pid, burst time, arrival time, familiarity# 
p1 = Process(1, 3, 0, 0)
p2 = Process(2, 1, 3, 0)
p3 = Process(3, 4, 2, 0)
p4 = Process(4, 5, 0, 0)

#add/remove processes 
lst = [p1, p2, p3, p4]
queueTest.load_processes(lst)
queueTest.handle_queue()
##########################
