from operator import attrgetter


class Process:

    def __init__(self, pid, burst_time, arrival_time, familiarity, quanta=3):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.quanta = quanta
        self.familiarity = familiarity


class Scheduler:

    def __init__(self):
        self.process_queue = []

    def load_processes(self, processes):
        self.process_queue.extend(processes)

    def handle_processes(self):

        clock = 0  # the time the process enters the cpu
        sum_burst_time = 0  # zero uses so far :D
        processes = []  # no signifcant uses except keep track of number of processes
        total_turnaround_time = 0
        total_waiting_time = 0

        while self.process_queue:

            current_process = self.process_pick()

            # Entry time of a process

            if current_process.arrival_time > clock:
                # visualisation of output
                idle_time = abs(clock - current_process.arrival_time)
                spaces = round(idle_time // 2)
                print(f"[{clock}ms]", '-{', ' ' * spaces, '-', ' ' * spaces, '}-', end='')
                # new clock
                clock = current_process.arrival_time

            # waiting time calculation
            waiting_time = clock - current_process.arrival_time
            if waiting_time < 0:
                waiting_time = 0
            total_waiting_time += waiting_time

            sum_burst_time += current_process.burst_time  #

            # tunraround time calculation
            turnaround_time = abs(clock + current_process.burst_time - current_process.arrival_time)
            total_turnaround_time += turnaround_time

            # visualisation of output
            spaces = round(current_process.burst_time // 2)
            print(f"[{clock}ms]", '-{', ' ' * spaces, 'P', str(current_process.pid), ' ' * spaces, '}- ', end='')

            processes.append(current_process)
            clock += current_process.burst_time  # clock moves #burst_time# long

        print(f"[{clock}ms]")
        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / len(processes)), 4)}')
        print(f'Average Waiting Time: {round((total_waiting_time / len(processes)), 4)}')
        print(f'Average Response Time: {round((total_waiting_time / len(processes)), 4)}')


class FCFS(Scheduler):

    def handle_queue(self):
        print('\nFCFS Queue Scheduling:\n')
        self.handle_processes()

    def process_pick(self):
        # pick process with least arrival time then remove it from the queue
        picked_process = min(self.process_queue, key=attrgetter('arrival_time'))
        self.process_queue.remove(picked_process)
        return picked_process


class RR(Scheduler):

    def __init__(self):
        super().__init__()
        self.turn = -1
        self.RR_arrived_processes = []

    def handle_queue(self):
        print('\nRR Queue Scheduling:\n')
        self.RR_handle_processes()

    def RR_handle_processes(self):  # special handeling for RR

        processes_initial_bursttime = {}
        for process in self.process_queue:
            processes_initial_bursttime[process.pid] = process.burst_time

        global RR_clock
        RR_clock = 0
        waiting_time = 0
        sum_burst_time = 0
        processes = []
        total_turnaround_time = 0
        total_waiting_time = 0
        total_response_time = 0

        while self.process_queue:

            current_process = self.process_pick()

            if current_process.arrival_time > RR_clock:
                idle_time = abs(RR_clock - current_process.arrival_time)
                spaces = round(idle_time // 2)
                print(f"[{RR_clock}ms]", '-{', ' ' * spaces, '-', ' ' * spaces, '}-', end='')
                RR_clock = current_process.arrival_time

            initial_burst = processes_initial_bursttime[current_process.pid]
            if current_process.burst_time == initial_burst:
                response_time = RR_clock - current_process.arrival_time
                total_response_time += response_time

            # Time slice calculation
            if current_process.burst_time < current_process.quanta:
                # when process burst time is less than the quanta then
                # the time added to burst time is just the remaining burst
                sum_burst_time += current_process.burst_time
                time_slice = current_process.burst_time
            else:
                # otherwise it is the full quanta
                sum_burst_time += current_process.quanta
                time_slice = current_process.quanta

            current_process.burst_time -= current_process.quanta

            if current_process.burst_time <= 0 and current_process in self.process_queue:  # means the process is fully executed

                process_FULL_burst_time = processes_initial_bursttime[current_process.pid]
                waiting_time = RR_clock - current_process.arrival_time - process_FULL_burst_time + time_slice
                last_burst = current_process.burst_time + current_process.quanta
                total_waiting_time += waiting_time
                turnaround_time = abs(RR_clock + last_burst - current_process.arrival_time)
                total_turnaround_time += turnaround_time

                self.process_queue.remove(current_process)

                processes.append(current_process)  # just a tracker list (used for len() )

            else:
                self.RR_arrived_processes.append(current_process)

            spaces = round(current_process.quanta // 2)
            print(f"[{RR_clock}ms]", '-{', ' ' * spaces, 'P', str(current_process.pid), ' ' * spaces, '}- ', end='')
            RR_clock += time_slice

        print(f"[{RR_clock}ms]")
        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / len(processes)), 4)}')
        print(f'Average Waiting Time: {round((total_waiting_time / len(processes)), 4)}')
        print(f'Average Response Time: {round((total_response_time / len(processes)), 4)}')

    def process_pick(self):
        temp = None
        arrived = []
        for process in list(self.process_queue):
            if process.arrival_time <= RR_clock + 3 and process not in self.RR_arrived_processes:
                arrived.append(process)
                process__ = process

        arrived.sort(key=lambda process: process.arrival_time)

        for process in arrived:
            self.RR_arrived_processes.append(process)

        if self.RR_arrived_processes:
            picked_process = self.RR_arrived_processes.pop(0)
            return picked_process
        else:
            return min(self.process_queue, key=attrgetter('arrival_time'))


class SRTF(Scheduler):

    def handle_queue(self):

        clock = 0
        arrived_processes = []

        last_process = None  # This variable is to keep track of preemptive change of processes
        # Uses: detect process change point

        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        processes_initial_bursttime = {}
        finished_processes = []
        count = 0
        idle_flag = False
        print("\nSRTF Queue Scheduling:\n")

        for process in self.process_queue:
            processes_initial_bursttime[process.pid] = process.burst_time

        while True:

            if self.process_queue:
                min_process = min(self.process_queue, key=attrgetter('arrival_time'))

            for process in self.process_queue:
                if process.arrival_time <= clock:
                    arrived_processes.append(process)
                    count += 1
                    self.process_queue.remove(process)

            if arrived_processes == []:
                arrived_processes.append(min_process)
                idle_time = min_process.arrival_time - clock
                spaces = idle_time
                print(f"[{clock}ms]", '-{', ' ' * spaces, '-', ' ' * spaces, '}- ', end='')
                clock = min_process.arrival_time
                idle_flag = True

            # for process in arrived_processes:
            #     print(process.pid,end=' ')

            picked_process = min(arrived_processes, key=attrgetter('burst_time'))

            if last_process != picked_process:
                process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                spaces = process_FULL_burst_time - picked_process.burst_time
                print(f"[{clock}ms]", '-{', ' ' * spaces, 'P', str(picked_process.pid), ' ' * spaces, '}- ', end='')

            initial_burst = processes_initial_bursttime[picked_process.pid]
            if picked_process.burst_time == initial_burst:
                response_time = clock - picked_process.arrival_time
                total_response_time += response_time

            picked_process.burst_time -= 1

            if picked_process.burst_time <= 0:

                process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                if len(finished_processes) <= 3:
                    waiting_time = abs(clock + 1 - process_FULL_burst_time - picked_process.arrival_time)
                    turnaround_time = abs(clock + 1 - picked_process.arrival_time)
                    total_waiting_time += waiting_time
                    total_turnaround_time += turnaround_time
                    process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                    spaces = process_FULL_burst_time - picked_process.burst_time

                    finished_processes.append(picked_process)
                arrived_processes.remove(picked_process)
                if not arrived_processes and not self.process_queue:

                    break

            clock += 1
            last_process = picked_process

        if idle_flag == True:
            clock -= 1
        print(f"[{clock + 1}ms]")
        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / count), 4)}')
        print(f'Average Waiting Time: {round((total_waiting_time / count), 4)}')
        print(f'Average Response Time: {round((total_response_time / count), 4)}')


class Regular_Visitors_Priority_Queue(Scheduler):

    def handle_queue(self):

        clock = 0
        arrived_processes = []
        last_process = None
        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        processes_initial_bursttime = {}
        count = 0
        idle_flag = False
        finished_processes = []


        print("\nRVP (Custom) Queue Scheduling:\n")
        for process in self.process_queue:
            processes_initial_bursttime[process.pid] = process.burst_time

        while True:

            if self.process_queue:
                min_process = min(self.process_queue, key=attrgetter('arrival_time'))

            for process in self.process_queue:
                if process.arrival_time <= clock:
                    arrived_processes.append(process)
                    count += 1
                    self.process_queue.remove(process)

            if arrived_processes == []:
                arrived_processes.append(min_process)
                idle_time = min_process.arrival_time - clock
                print(f"[{clock}ms]", '-{', ' ' * spaces, '-', ' ' * spaces, '}- ', end='')
                clock = min_process.arrival_time

            # for process in arrived_processes:
            #     print(process.pid,end=' ')

            picked_process = max(arrived_processes, key=attrgetter('familiarity'))

            if last_process != picked_process:
                process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                spaces = process_FULL_burst_time - picked_process.burst_time
                print(f"[{clock}ms]", '-{', ' ' * spaces, 'P', str(picked_process.pid), ' ' * spaces, '}- ', end='')

            initial_burst = processes_initial_bursttime[picked_process.pid]
            if picked_process.burst_time == initial_burst:
                response_time = clock - picked_process.arrival_time
                total_response_time += response_time

            picked_process.burst_time -= 1

            if picked_process.burst_time <= 0:

                process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                if len(finished_processes) <= 3:
                    waiting_time = abs(clock + 1 - process_FULL_burst_time - picked_process.arrival_time)
                    turnaround_time = abs(clock + 1 - picked_process.arrival_time)
                    total_waiting_time += waiting_time
                    total_turnaround_time += turnaround_time
                    process_FULL_burst_time = processes_initial_bursttime[picked_process.pid]
                    spaces = process_FULL_burst_time - picked_process.burst_time

                    finished_processes.append(picked_process)
                arrived_processes.remove(picked_process)
                if not arrived_processes and not self.process_queue:
                    break

            clock += 1
            last_process = picked_process

        if idle_flag == True:
            clock -= 1

        print(f"[{clock + 1}ms]")
        print(f'\n\nAverage Turnaround Time: {round((total_turnaround_time / count), 4)}')
        print(f'Average Waiting Time: {round((total_waiting_time / count), 4)}')
        print(f'Average Response Time: {round((total_response_time / count), 4)}')

#TO RUN THE PROGRAM:
queueTest = RR() #YOU CAN CHANGE THIS TO: FCFS(), RR(), Regular_Visitors_Priority_Queue()

#CHANGE PROCESSES ATTRIBUTES IN THIS ORDER:
# pid, burst time, arrival time, familiarity#
p1 = Process(1, 4, 1, 0)
p2 = Process(2, 6, 0, 1)
p3 = Process(3, 3, 8, 2)
p4 = Process(4, 6, 5, 0)

#HERE ADD/REMOVE PROCESSES
lst = [p1, p2, p3, p4]
queueTest.load_processes(lst)
queueTest.handle_queue()
