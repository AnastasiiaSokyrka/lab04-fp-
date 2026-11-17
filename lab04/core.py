from functools import lru_cache
from typing import Callable, NamedTuple, Protocol


def is_palindrome(text: str) -> bool:
    def check(left: int, right: int) -> bool:
        return left >= right or (
            text[left] == text[right] and check(left + 1, right - 1)
        )

    return check(0, len(text) - 1)


def is_palindrome_iter(text: str) -> bool:
    for left in range(len(text) // 2):
        if text[left] != text[-left - 1]:
            return False
    return True


class CacheInfo(Protocol):
    @property
    def hits(self) -> int: ...
    @property
    def misses(self) -> int: ...
    @property
    def currsize(self) -> int: ...


class CacheControls(NamedTuple):
    cache_info: Callable[[], CacheInfo]
    cache_clear: Callable[[], None]


def palindrome_solver(
    text: str, *, cached: bool = True
) -> tuple[Callable[[int, int], tuple[int, int]], CacheControls]:
    def check(left: int, right: int) -> bool:
        return left >= right or (
            text[left] == text[right] and palindrome(left + 1, right - 1)
        )

    def best(left: int, right: int) -> tuple[int, int]:
        if palindrome(left, right):
            return left, right
        first = solve(left, right - 1)
        second = solve(left + 1, right)
        return first if first[1] - first[0] >= second[1] - second[0] else second

    cached_check = lru_cache(maxsize=None)(check)
    cached_best = lru_cache(maxsize=None)(best)
    palindrome = cached_check if cached else check
    solve = cached_best if cached else best

    def clear() -> None:
        cached_best.cache_clear()
        cached_check.cache_clear()

    return solve, CacheControls(cached_best.cache_info, clear)


def longest_palindrome(text: str, *, cached: bool = True) -> str:
    solve, _ = palindrome_solver(text, cached=cached)
    left, right = solve(0, len(text) - 1)
    return text[left : right + 1]
