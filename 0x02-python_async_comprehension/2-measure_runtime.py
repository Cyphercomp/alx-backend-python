#!/usr/bin/env python3
''' 2-measure_runtime.py '''

from time import time
from asyncio import gather

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''
    execute async_comprehension four times in parallel using asyncio.gather
    and returns the total runtime
    '''
    start_time = time()
    await gather(*(async_comprehension() for _ in range(4)))
    run_time = time() - start_time

    return run_time
