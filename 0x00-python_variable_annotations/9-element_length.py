#!/usr/bin/env python3
''' 9-element_length.py '''

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''
    takes a list with sequence and returns a tuple of
    sequence and int
    '''
    return [(i, len(i)) for i in lst]
