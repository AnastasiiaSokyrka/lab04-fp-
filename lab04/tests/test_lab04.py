from random import Random

import pytest

from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    fib,
    fib_iter,
    inorder,
    postorder,
    preorder,
    quicksort,
)
from core import (
    is_palindrome,
    is_palindrome_iter,
    longest_palindrome,
    palindrome_solver,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", True),
        ("а", True),
        ("абба", True),
        ("аб", False),
        ("🙂🙃🙂", True),
        ("Яя", False),
        ("a a", True),
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) == is_palindrome_iter(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", ""),
        ("x", "x"),
        ("babad", "bab"),
        ("cbbd", "bb"),
        ("яїїяб", "яїїя"),
        ("a🙂🙃🙂b", "🙂🙃🙂"),
        ("abc", "a"),
    ],
)
def test_longest_palindrome(text: str, expected: str) -> None:
    assert (
        longest_palindrome(text) == longest_palindrome(text, cached=False) == expected
    )


def test_cache() -> None:
    solve, cache = palindrome_solver("abcdef")
    assert solve(0, 5) == (0, 0)
    assert cache.cache_info().hits > 0
    cache.cache_clear()
    assert cache.cache_info().currsize == 0


def test_long_iterative_input() -> None:
    assert is_palindrome_iter("а" * 5000)


def test_quicksort() -> None:
    rng = Random(13)
    for size in (0, 1, 2, 20, 100):
        values = [rng.randrange(-5, 6) for _ in range(size)]
        original = values.copy()
        assert quicksort(values, pivot_of=rng.choice) == sorted(values)
        assert values == original


def test_tree() -> None:
    tree = Node(4, Node(2, Node(1), Node(3)), Node(6))
    assert list(preorder(tree)) == list(dfs_preorder_iter(tree)) == [4, 2, 1, 3, 6]
    assert list(inorder(tree)) == [1, 2, 3, 4, 6]
    assert list(postorder(tree)) == [1, 3, 2, 6, 4]
    assert list(bfs_level_order(tree)) == [4, 2, 6, 1, 3]
    assert list(bfs_level_order(None)) == list(preorder(None)) == []


def test_fibonacci() -> None:
    assert [fib(n) for n in range(7)] == [0, 1, 1, 2, 3, 5, 8]
    assert fib(35) == fib_iter(35)
    fib.cache_clear()
    assert fib.cache_info().currsize == 0
    for func in (fib, fib_iter):
        with pytest.raises(ValueError):
            func(-1)
