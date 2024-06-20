import psutil
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(filename='system_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set threshold values
CPU_THRESHOLD = 80
MEM_THRESHOLD = 52
DISK_THRESHOLD = 80

# Variables to track if threshold exceeded
cpu_above_threshold = False
mem_above_threshold = False
disk_above_threshold = False

def check_cpu_usage():
    global cpu_above_threshold
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        if not cpu_above_threshold:
            print(f'CPU usage exceeded threshold: {cpu_usage}%')
            logging.info(f'CPU usage exceeded threshold: {cpu_usage}%')
            cpu_above_threshold = True
            log_top_processes()
    else:
        if cpu_above_threshold:
            logging.info(f'CPU usage returned to normal: {cpu_usage}%')
            cpu_above_threshold = False

def check_memory_usage():
    global mem_above_threshold
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    if mem_usage > MEM_THRESHOLD:
        if not mem_above_threshold:
            print(f'Memory usage exceeded threshold: {mem_usage}%')
            logging.info(f'Memory usage exceeded threshold: {mem_usage}%')
            mem_above_threshold = True
            log_top_processes()
    else:
        if mem_above_threshold:
            logging.info(f'Memory usage returned to normal: {mem_usage}%')
            mem_above_threshold = False

def check_disk_usage():
    global disk_above_threshold
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    if disk_usage > DISK_THRESHOLD:
        if not disk_above_threshold:
            print(f'Disk usage exceeded threshold: {disk_usage}%')
            logging.info(f'Disk usage exceeded threshold: {disk_usage}%')
            disk_above_threshold = True
            log_top_processes()
    else:
        if disk_above_threshold:
            logging.info(f'Disk usage returned to normal: {disk_usage}%')
            disk_above_threshold = False

def log_top_processes():
    logging.info('Top 5 CPU-consuming processes:')
    processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    top_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
    for pid, name, cpu_percent in top_processes:
        logging.info(f'PID: {pid}, Name: {name}, CPU: {cpu_percent}%')

def main():
    logging.info('System Health Monitoring started')
    count = 1
    while True:
        print(f'Checking Stats... {count}')
        count += 1
        check_cpu_usage()
        check_memory_usage()
        check_disk_usage()
        time.sleep(10)  # Check every 10 seconds

if __name__ == '__main__':
    main()
