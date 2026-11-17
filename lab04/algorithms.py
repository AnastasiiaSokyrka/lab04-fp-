from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from functools import lru_cache
from random import choice


def quicksort(
    items: Sequence[int], *, pivot_of: Callable[[Sequence[int]], int] = choice
) -> list[int]:
    if len(items) < 2:
        return list(items)
    pivot = pivot_of(items)
    lower = [item for item in items if item < pivot]
    equal = [item for item in items if item == pivot]
    upper = [item for item in items if item > pivot]
    return (
        quicksort(lower, pivot_of=pivot_of)
        + equal
        + quicksort(upper, pivot_of=pivot_of)
    )


@dataclass(frozen=True)
class Node:
    key: int
    left: Node | None = None
    right: Node | None = None


def preorder(node: Node | None) -> Iterator[int]:
    if node is not None:
        yield node.key
        yield from preorder(node.left)
        yield from preorder(node.right)


def inorder(node: Node | None) -> Iterator[int]:
    if node is not None:
        yield from inorder(node.left)
        yield node.key
        yield from inorder(node.right)


def postorder(node: Node | None) -> Iterator[int]:
    if node is not None:
        yield from postorder(node.left)
        yield from postorder(node.right)
        yield node.key


def bfs_level_order(node: Node | None) -> Iterator[int]:
    queue = deque([node] if node is not None else [])
    while queue:
        current = queue.popleft()
        yield current.key
        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)


def dfs_preorder_iter(node: Node | None) -> Iterator[int]:
    stack = [node] if node is not None else []
    while stack:
        current = stack.pop()
        yield current.key
        if current.right is not None:
            stack.append(current.right)
        if current.left is not None:
            stack.append(current.left)


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    current, following = 0, 1
    for _ in range(n):
        current, following = following, current + following
    return current
