#!/usr/bin/env python3
''' 0-basic_async_syntax.py '''

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    ''' asynchronous coroutine that waits random delay and returns it '''
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
