
from operator import attrgetter
class Process:

    def __init__(self,pid,burst_time,arrival_time,prio,quanta=3):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.prio = prio
        self.quanta = quanta

class Scheduler:

    def __init__(self):
        self.process_queue= []

    def load_processes(self,processes):
        self.process_queue.extend(processes)

    def handle_processes(self):

        clock = 0                   #the time the process enters the cpu
        sum_burst_time = 0          #used mainly to calculate the clock
        processes = []               #no signifcant uses except keep track of number of processes
        total_turnaround_time = 0
        total_waiting_time = 0

        while self.process_queue:


            current_process = self.process_pick()


                #Entry time of a process

            if  current_process.arrival_time > clock:
                idle_time = abs(clock - current_process.arrival_time)
                spaces = round(idle_time // 2)
                print(f"[{clock}ms]",'-{', ' ' * spaces, '-', ' ' * spaces, '}-', end='')
                clock = current_process.arrival_time





            #nonpremitve wait time of each process
            waiting_time = clock - current_process.arrival_time
            if waiting_time <0:
                waiting_time = 0
            total_waiting_time += waiting_time


            sum_burst_time += current_process.burst_time


            turnaround_time = abs(clock +current_process.burst_time - current_process.arrival_time)
            total_turnaround_time += turnaround_time


            #visualisation of output
            spaces = round(current_process.burst_time // 2)
            print(f"[{clock}ms]",'-{', ' ' * spaces,'P', str(current_process.pid), ' ' * spaces, '}- ', end='')


            processes.append(current_process)
            clock += current_process.burst_time #clock moves #burst_time# long

        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time/len(processes)),4)}')
        print(f'Average Waiting Time: {round((total_waiting_time/len(processes)),4)}')
        print(f'Average Response Time: {round((total_waiting_time / len(processes)), 4)}')

class FCFS(Scheduler):

    def handle_queue(self):
        print('\nFCFS Queue Scheduler:\n')
        self.handle_processes()

    def process_pick(self):
        #pick process with least arrival time then remove it from the queue
        picked_process = min(self.process_queue, key=attrgetter('arrival_time'))
        self.process_queue.remove(picked_process)
        return picked_process


class SJF(Scheduler):

    def handle_queue(self):
        print('\nSJF Queue Scheduler:\n')
        self.handle_processes()


    def process_pick(self):
        min_process = min(self.process_queue, key=attrgetter('arrival_time'))
        arrived_processes = []
        for process in self.process_queue:
            if process.arrival_time == min_process.arrival_time:
                arrived_processes.append(process)
        picked_process = min(arrived_processes, key=attrgetter('burst_time'))
        arrived_processes.remove(picked_process)
        self.process_queue.remove(picked_process)
        return picked_process


class PriorityQueue(Scheduler):


    def handle_queue(self):
        print('\nPriority Queue Scheduler:\n')
        self.handle_processes()


    def process_pick(self):
        min_process = min(self.process_queue, key=attrgetter('arrival_time'))
        arrived_processes = []
        for process in self.process_queue:
            if process.arrival_time == min_process.arrival_time:
                arrived_processes.append(process)
        picked_process = min(arrived_processes, key=attrgetter('prio'))
        arrived_processes.remove(picked_process)
        self.process_queue.remove(picked_process)
        return picked_process

class RR(Scheduler):

    def handle_queue(self):
        print('\nRR Queue Scheduler:\n')
        self.RR_handle_processes()

    def RR_handle_processes(self): #special handeling for RR

        waiting_time = 0
        sum_burst_time = 0
        processes = []
        total_turnaround_time = 0


        while self.process_queue:

            current_process = self.process_pick()


            if current_process.burst_time < current_process.quanta:
                #when process burst time is less than the quanta then
                #the time added to burst time is just the remaining burst
                sum_burst_time += current_process.burst_time
            else:
                #otherwise it is the full quanta
                sum_burst_time += current_process.quanta


            current_process.burst_time -= current_process.quanta

            if current_process.burst_time <= 0: #means the process is fully executed

                turn_around_time = sum_burst_time - current_process.arrival_time
                total_turnaround_time += turn_around_time
                self.process_queue.remove(current_process)

                processes.append(current_process) #just a tracker list (used for len() )


            else:
                #otherwise process is not finished send it back to the queue
                self.process_queue.remove(current_process)
                self.process_queue.append(current_process)

            #after all processes are done, the total waiting time = total turnaround time + total burst time
            total_waiting_time = total_turnaround_time - sum_burst_time
            spaces = round(current_process.quanta // 2)
            print('-{', ' ' * spaces, current_process.pid, ' ' * spaces, '}-', end='')

        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / len(processes)), 3)}')
        print(f'Average Waiting Time: {round((total_waiting_time / len(processes)), 3)}')

    def process_pick(self):
        picked_process = self.process_queue[0]
        return picked_process



sjf = SJF()
p1 = Process(1,4,4,1)
p2 = Process(2,35,15,2)
p3 = Process(3,12,19,3)
p4 = Process(4,4,0,4)
lst = [p1,p2,p3,p4]
sjf.load_processes(lst)
sjf.handle_queue()
