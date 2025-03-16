import time
import asyncio
import threading
import multiprocessing
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# Display results
import pandas as pd
import for_jupter as tools

# CPU-bound task: Sum of squares
def cpu_intensive_task(n):
    return sum(i * i for i in range(n))

# I/O-bound task: Fetching multiple URLs
URLS = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.openai.com",
] * 3  # Repeat URLs to increase load

def fetch_url(url):
    response = requests.get(url)
    return len(response.content)

# Benchmark for CPU-bound task
def benchmark_cpu_task(n, workers=4):
    print("Benchmarking CPU-bound task...\n")
    
    # Sequential execution
    start = time.time()
    [cpu_intensive_task(n) for _ in range(workers)]
    sequential_time = time.time() - start

    # Multithreading
    start = time.time()
    threads = []
    for _ in range(workers):
        thread = threading.Thread(target=cpu_intensive_task, args=(n,))
        thread.start()
        threads.append(thread) # Start multiple threads
    for thread in threads:
        thread.join() # When .join the compiler waits for the thread to finish
    threading_time = time.time() - start

    # Multiprocessing
    start = time.time()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        executor.map(cpu_intensive_task, [n] * workers)
    multiprocessing_time = time.time() - start

    return {
        "sequential": sequential_time,
        "threading": threading_time,
        "multiprocessing": multiprocessing_time
    }

# Benchmark for I/O-bound task
async def async_fetch(url):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, fetch_url, url)

async def async_fetch_all():
    tasks = [async_fetch(url) for url in URLS]
    return await asyncio.gather(*tasks)

def benchmark_io_task():
    print("\nBenchmarking I/O-bound task...\n")
    
    # Sequential execution
    start = time.time()
    [fetch_url(url) for url in URLS]
    sequential_time = time.time() - start

    # Multithreading
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch_url, URLS)
    threading_time = time.time() - start

    # Asyncio
    start = time.time()
    asyncio.run(async_fetch_all())
    asyncio_time = time.time() - start

    return {
        "sequential": sequential_time,
        "threading": threading_time,
        "asyncio": asyncio_time
    }

# Running benchmarks
cpu_results = benchmark_cpu_task(10**7, workers=4)
io_results = benchmark_io_task()

cpu_df = pd.DataFrame.from_dict(cpu_results, orient='index', columns=['Time (s)'])
io_df = pd.DataFrame.from_dict(io_results, orient='index', columns=['Time (s)'])
cpu_df.head()
io_df.head()
tools.display_dataframe_to_user(name="CPU Performance Comparison", dataframe=cpu_df)
tools.display_dataframe_to_user(name="I/O Performance Comparison", dataframe=io_df)
