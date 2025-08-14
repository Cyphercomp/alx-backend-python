#!/usr/bin/env python3
''' 2-measure_runtime.py '''

import time
import asyncio

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    ''' computes and returns average time to execute '''
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    elapsed_time = time.time() - start_time
    return elapsed_time / n
