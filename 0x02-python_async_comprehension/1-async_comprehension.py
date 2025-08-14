#!/usr/bin/env python3
''' 1-async_comprehension.py '''

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    ''' creates a list of 10 numbers from a generator '''
    return [i async for i in async_generator()]
