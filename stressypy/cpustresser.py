
# ------------------- #
# Third Party Imports #
# ------------------- #
import time
import random
import subprocess
import multiprocessing as mp
from types import *

stress_string = 'stress -c {0} -t {1}s'

class JobBlock:
    """

    """

    total_blocks = 0
    queued_blocks = 0
    waiting_blocks = 0

    def __init__(self, n_cpu, t_run, delta_t_run=0.025, q_name='default'):
        self.n_cpu = n_cpu
        self.time = t_run
        self.delta_time = delta_t_run
        self.state = 'waiting'
        self.func = None
        self.func_args = ''
        self.area = n_cpu*t_run
        self.total_blocks += 1
        self.queue = q_name
        self.job = None
        if self.n_cpu > mp.cpu_count():
            self.n_cpu = mp.cpu_count()

    def set_job(self, func, *args):
        if type(func) == FunctionType:
            self.func = func
            self.args = args
            self.job = func( *args )
        else:
            raise ValueError('for setjob(func, arg): func is not a function')

    def run(self):
        if self.job is not None:
            exec(self.job)


def get_time_used(func, *args):
    start_time = time.perf_counter()
    func( *args )
    return time.perf_counter()-start_time


def create_job(cpu_width, time_height):
    """
    :param cpu_width:
    :param time_height:
    :return:
    """
    shell_command = stress_string.format(cpu_width, time_height)
    job = JobBlock(cpu_width, time_height)
    job.set_job(lambda: subprocess.call(shell_command, shell=True))
    return job



def test_loader(rand_list=[], cpuse = True):
    machine_available_cores = mp.cpu_count()

    num_tests = 1

    if not rand_list:
        rand_list = [(random.randint(1, machine_available_cores), random.randint(1, 3) ) for _ in range(num_tests)]

    bash_commands = ['stress -c {0} -t {1}s'.format(i, n) for i, n in rand_list]


    if cpuse:
        tused = [get_time_used(lambda: subprocess.call(command, shell=True)) for command in bash_commands]

        total = 0
        for it in tused:
            print('time used ', it)
            total += it
        print('total time for entire queue ', total)
    else:
        return rand_list