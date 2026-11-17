from sys import getrecursionlimit
from timeit import repeat

from algorithms import Node, bfs_level_order, fib, fib_iter, quicksort
from core import is_palindrome, longest_palindrome, palindrome_solver


def main() -> None:
    for text in ("радарадар", "кіт і тік", "🙂🙃🙂", "babad"):
        print(
            f"{text!r}: palindrome={is_palindrome(text)}, best={longest_palindrome(text)!r}"
        )

    example = "forgeeksskeegfor"
    solve, cache = palindrome_solver(example)
    solve(0, len(example) - 1)
    print(f"cache after first run: {cache.cache_info()}")
    cache.cache_clear()
    print(f"cache after clear: {cache.cache_info()}")
    text = "abcdefghijklmnop"
    for cached in (False, True):
        seconds = min(
            repeat(lambda: longest_palindrome(text, cached=cached), number=10, repeat=3)
        )
        print(f"longest, cached={cached}: {seconds * 100:.3f} ms/call")
    print(f"Recursion limit: {getrecursionlimit()}")
    print(f"Quicksort: {quicksort([3, 1, 2, 1])}")
    print(f"BFS: {list(bfs_level_order(Node(2, Node(1), Node(3))))}")
    print(f"Fibonacci(20): {fib(20)} / {fib_iter(20)}")


if __name__ == "__main__":
    main()
