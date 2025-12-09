from functools import partial
from pathlib import Path
import timeit


def boyer_moore(text: str, pattern: str) -> int:
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    table = {ch: i for i, ch in enumerate(pattern)}
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift
        move = j - table.get(text[shift + j], -1)
        shift += move if move > 0 else 1
    return -1


def kmp(text: str, pattern: str) -> int:
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp(text: str, pattern: str) -> int:
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    if m > n:
        return -1
    base = 256
    mod = 1_000_000_007
    pattern_hash = 0
    window_hash = 0
    power = 1
    for _ in range(m - 1):
        power = (power * base) % mod
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if pattern_hash == window_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash %= mod
    return -1


def benchmark(text: str, pattern: str, number: int = 10) -> dict:
    algorithms = {
        "Boyer-Moore": boyer_moore,
        "KMP": kmp,
        "Rabin-Karp": rabin_karp,
    }
    results = {}
    for name, func in algorithms.items():
        timer = timeit.Timer(partial(func, text, pattern))
        results[name] = timer.timeit(number=number) / number
    return results


def mean(values) -> float:
    return sum(values) / len(values)


def run():
    base = Path(__file__).resolve().parent
    text1 = (base / "стаття 1.txt").read_text(encoding="utf-8")
    text2 = (base / "стаття 2.txt").read_text(encoding="utf-8")
    datasets = {
        "Стаття 1": {
            "text": text1,
            "patterns": {
                "існуючий": "алгоритмів у бібліотеках мов програмування",
                "вигаданий": "вигаданий_підрядок_1",
            },
        },
        "Стаття 2": {
            "text": text2,
            "patterns": {
                "існуючий": "рекомендаційної системи",
                "вигаданий": "вигаданий_підрядок_2",
            },
        },
    }
    summary = {}
    for name, data in datasets.items():
        text = data["text"]
        pattern_results = {}
        for label, pattern in data["patterns"].items():
            pattern_results[label] = benchmark(text, pattern)
        summary[name] = pattern_results
    for name, results in summary.items():
        print(name)
        for label, metrics in results.items():
            print(label)
            for alg, value in metrics.items():
                print(f"{alg}: {value:.6f}")
    per_text_best = {}
    for name, results in summary.items():
        aggregated = {}
        for alg in next(iter(results.values())).keys():
            aggregated[alg] = mean(
                [metrics[alg] for metrics in results.values()]
            )
        best = min(aggregated.items(), key=lambda item: item[1])[0]
        per_text_best[name] = {"best": best, "averages": aggregated}
    overall_average = {}
    first_patterns = next(iter(summary.values()))
    first_algorithms = next(iter(first_patterns.values())).keys()
    for alg in first_algorithms:
        overall_average[alg] = mean(
            [
                summary[text][pattern][alg]
                for text in summary
                for pattern in summary[text]
            ]
        )
    fastest_overall = min(overall_average.items(), key=lambda item: item[1])[0]
    print("Найшвидші алгоритми за текстами:")
    for name, data in per_text_best.items():
        print(f"{name}: {data['best']}")
    print("Середні значення по всіх тестах:")
    for alg, value in overall_average.items():
        print(f"{alg}: {value:.6f}")
    print(f"Найшвидший загалом: {fastest_overall}")


if __name__ == "__main__":
    run()
