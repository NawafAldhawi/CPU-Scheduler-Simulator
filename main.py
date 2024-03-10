class Process:
    def __init__(self,pid,burst_time,arrival_time,prio):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.prio = prio

class Scheduler:
    def __init__(self):
        self.process_queue= []

    def load_processes(self,processes):
        self.process_queue.extend(processes)

    def handle_processes(self):

        sum_burst_time = 0
        processes = []
        total_turnaround_time = 0
        total_waiting_time = 0

        while self.process_queue:

            current_process = self.process_pick()

            waiting_time = sum_burst_time - current_process.arrival_time
            total_waiting_time += waiting_time
            sum_burst_time += current_process.burst_time

            turnaround_time = sum_burst_time - current_process.arrival_time
            total_turnaround_time += turnaround_time



            spaces = round(current_process.burst_time // 2)
            print('-{', ' ' * spaces, current_process.pid, ' ' * spaces, '}-', end='')
            processes.append(current_process)

        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time/len(processes)),3)}')
        print(f'Average Waiting Time: {round((total_waiting_time/len(processes)),3)}')
        print(total_turnaround_time)


class FCFS(Scheduler):

    def handle_queue(self):
        #clock start
        print('\nFCFS Queue Scheduler:\n')
        self.handle_processes()

    def process_pick(self):
        picked_process = self.process_queue[0]
        for process in self.process_queue:
            if process.arrival_time < picked_process.arrival_time:
                picked_process = process
        self.process_queue.remove(picked_process)
        return picked_process


class SJF(Scheduler):

    def handle_queue(self):
        print('\nSJF Queue Scheduler:\n')
        self.handle_processes()


    def process_pick(self):
        picked_process = self.process_queue[0]
        for process in self.process_queue:
            if process.burst_time < picked_process.burst_time:
                picked_process = process
        self.process_queue.remove(picked_process)
        return picked_process


class PriorityQueue(Scheduler):


    def handle_queue(self):
        print('\nPriority Queue Scheduler:\n')
        self.handle_processes()


    def process_pick(self):
        picked_process = self.process_queue[0]
        for process in self.process_queue:
            if process.prio < picked_process.prio:
                picked_process = process
        self.process_queue.remove(picked_process)
        return picked_process

class RR(Scheduler):

    def handle_queue(self):
        print('\nRR Queue Scheduler:\n')
        self.handle_processes()

    def RR_handle_queue(self):

        waiting_time = 0
        sum_burst_time = 0
        processes = []
        total_turnaround_time = 0



        while self.process_queue:

            current_process = self.process_pick()

            if current_process.burst_time < current_process.quanta:
                sum_burst_time += current_process.burst_time
            else:
                sum_burst_time += current_process.quanta

            current_process.burst_time -= current_process.quanta
            if current_process.burst_time <= 0:
                current_process.quanta = current_process.burst_time + current_process.quanta

                turn_around_time = sum_burst_time - current_process.arrival_time
                waiting_time = turn_around_time - current_process.burst_time

                total_turnaround_time += turn_around_time
                self.process_queue.remove(current_process)
                processes.append(current_process)
            else:
                self.process_queue.remove(current_process)
                self.process_queue.append(current_process)


            spaces = round(current_process.quanta // 2)
            print('-{', ' ' * spaces, current_process.pid, ' ' * spaces, '}-', end='')

        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / len(processes)), 3)}')

    def process_pick(self):
        picked_process = self.process_queue[0]
        for process in self.process_queue:
            process.quanta = 3
        return picked_process



sjf = PriorityQueue()
p1 = Process(1,3,0,1)
p2 = Process(2,5,2,4)
p3 = Process(3,9,3,2)
p4 = Process(4,12,4,5)
lst = [p1,p2,p3,p4]
sjf.load_processes(lst)
sjf.handle_queue()
