###############################################################################
import threading
import sys
import subprocess
import Queue
import time
import os
###############################################################################
'''
Get all weather data from Weather Underground.
Threading for speed.
All bash functions is weather-func.sh
'''
###############################################################################
exit_flag = False
###############################################################################


class GetWeatherThread(threading.Thread):
    def __init__(self, n, queue):
        threading.Thread.__init__(self)
        self.n = n
        self.q = queue
        return

    def run(self):
        global lock
        global exit_flag
        while not exit_flag:
            lock.acquire()
            if not self.q.empty():
                year = self.q.get()
                print 'Starting thread {}, on year {}'.format(self.n, year)
                lock.release()
                process = subprocess.Popen([
                    'bash', '-c',
                    'source weather-funcs.sh && SFO-year {}'.format(year)
                ])
                process.wait()
                print 'Stopping thread {}, on year {}'.format(self.n, year)
            else:
                lock.release()
        return


n_threads = 4
threads = []
queue = Queue.Queue()
lock = threading.Lock()

for n in range(n_threads):
    thread = GetWeatherThread(n, queue)
    thread.start()
    threads.append(thread)

lock.acquire()
for year in range(2003, 2016):
    queue.put(year)
lock.release()

while not queue.empty():
    pass

exit_flag = True

for thread in threads:
    thread.join()

subprocess.Popen([
    'bash', '-c',
    'source weather-funcs.sh && SFO-cleanup {}'.format(year)
])

