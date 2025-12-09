from typing import Iterable, Tuple, Optional


def binary_search_upper_bound(
    items: Iterable[float], target: float
) -> Tuple[int, Optional[float]]:
    sequence = list(items)
    left = 0
    right = len(sequence) - 1
    iterations = 0
    result = None
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if sequence[mid] >= target:
            result = sequence[mid]
            right = mid - 1
        else:
            left = mid + 1
    return iterations, result


if __name__ == "__main__":
    data = [1.2, 2.4, 2.6, 3.5, 5.0, 7.1]
    tests = [
        (2.5, (3, 2.6)),
        (1.0, (1, 1.2)),
        (7.1, (3, 7.1)),
        (10.0, (4, None)),
        (2.4, (2, 2.4)),
    ]
    for target, expected in tests:
        iterations, result = binary_search_upper_bound(data, target)
        print(
            f"Target: {target}, Iterations: {iterations}, Result: {result}"
        )
