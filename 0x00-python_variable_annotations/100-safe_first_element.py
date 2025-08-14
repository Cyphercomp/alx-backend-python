#!/usr/bin/env python3
''' 100-safe_first_element.py '''

from typing import Sequence, Any, Union, Optional


def safe_first_element(lst: Sequence[Any]) -> Union[Any, Optional[None]]:
    '''takes a sequence of any and returns any type or none '''
    if lst:
        return lst[0]
    else:
        return None
