import multiprocessing

bind = "127.0.0.1:9080"

workers = multiprocessing.cpu_count() * 2 + 1