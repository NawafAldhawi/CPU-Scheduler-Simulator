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
        print(f'\nAverage Burst Time: {round(sum_burst_time * 1000 / len(processes),4)}')
        print(f'Average Arrival Time: {round(sum_arrival_time * 1000 / len(processes),4)}')

class FCFS(Scheduler):

    def FCFS_handle_queue(self):
        #clock start
        print('FCFS Queue Scheduler:')
        self.handle_processes()

    def process_pick(self):
        return self.process_queue.pop(0)



class SJF(Scheduler):

    def SJF_handle_queue(self):
        print('SFJ Queue Scheduler:')
        self.handle_processes()


    def process_pick(self):
        picked_process = self.process_queue[0]
        for process in self.process_queue:
            if process.burst_time < picked_process.burst_time:
                picked_process = process
        self.process_queue.remove(picked_process)
        return picked_process

class RR(Scheduler):

    def RR_handle_queue(self):
        pass

class PriorityQueue(Scheduler):

    def PriorityQueue_handle_queue(self):
        pass


sjf = SJF()
p1 = Process(1,5,0,0)
p2 = Process(2,2,0,0)
p3 = Process(3,3,0,0)
lst = [p1,p2,p3]
sjf.load_processes(lst)
sjf.SJF_handle_queue()
