import time
class Process:
    def __init__(self,pid,burst_time,arrival_time,prio):
        self.pid = pid
        self.burst_time = burst_time/1000
        self.arrival_time = arrival_time
        self.prio = prio

class Scheduler:
    def __init__(self):
        self.process_queue= []

    def load_processes(self,processes):
        self.process_queue.extend(processes)

    def handle_processes(self):
        start_time = time.time()
        sum_arrival_time = 0
        sum_burst_time = 0
        processes = []
        while self.process_queue:
            current_process = self.process_pick()

            current_process.arrival_time = round(time.time() - start_time,4)
            sum_arrival_time += current_process.arrival_time
            sum_burst_time += current_process.burst_time
            spaces = round(current_process.burst_time * 1000 // 2)
            time.sleep(current_process.burst_time)
            print('-{', ' ' * spaces, current_process.pid, ' ' * spaces, '}-', end='')
            processes.append(current_process)
        print(f'\nAverage Burst Time: {sum_burst_time * 1000 / len(processes)}')
        print(f'Average Arrival Time: {sum_arrival_time * 1000 / len(processes)}')

class FCFS(Scheduler):

    def FCFS_handle_queue(self):
        #clock start
        print('FCFS Queue Scheduler:')
        self.handle_processes()

    def process_pick(self):
        return self.process_queue.pop(0)



class SJF(Scheduler):

    def SFJ_handle_queue(self):
        print(min(self.process_queue))
        self.process_queue.remove(min(self.process_queue))

class RR(Scheduler):

    def RR_handle_queue(self):
        pass

class PriorityQueue(Scheduler):

    def PriorityQueue_handle_queue(self):
        pass


fcfs = FCFS()
p1 = Process(1,1,0,0)
p2 = Process(2,1,0,0)
p3 = Process(3,1,0,0)
lst = [p1,p2,p3]
fcfs.load_processes(lst)
fcfs.FCFS_handle_queue()
