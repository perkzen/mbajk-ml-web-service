from typing import TypeVar, List

T = TypeVar('T')


def intersecting_elements(list1: List[T], list2: List[T]) -> List[T]:
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1.intersection(set2)
    return list(intersection)
