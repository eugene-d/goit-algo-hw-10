import random
import numpy as np
import scipy.integrate as spi
from typing import Callable, Tuple


def f(x: float) -> float:
    """Функція для інтегрування: f(x) = x²"""
    return x ** 2


def monte_carlo_integration(func: Callable[[float], float], a: float, b: float, n_points: int) -> float:
    """Обчислення інтеграла методом Монте-Карло."""
    x_vals: np.ndarray = np.linspace(a, b, 1000)
    y_vals: list[float] = [func(x) for x in x_vals]
    max_y: float = max(y_vals)

    points_under_curve: int = 0

    for _ in range(n_points):
        x: float = random.uniform(a, b)
        y: float = random.uniform(0, max_y)

        if y <= func(x):
            points_under_curve += 1

    rectangle_area: float = (b - a) * max_y
    integral_estimate: float = (points_under_curve / n_points) * rectangle_area

    return integral_estimate


def monte_carlo_multiple_experiments(func: Callable[[float], float], a: float, b: float,
                                    n_points: int, n_experiments: int) -> Tuple[float, list[float]]:
    """Виконання кількох експериментів методом Монте-Карло для підвищення точності."""
    results: list[float] = []

    for experiment in range(n_experiments):
        result: float = monte_carlo_integration(func, a, b, n_points)
        results.append(result)

    average_result: float = sum(results) / len(results)
    return average_result, results


def analytical_solution(a: float, b: float) -> float:
    """Аналітичне розв'язання інтеграла від a до b"""
    return (b**3 - a**3) / 3


def compare_with_scipy(func: Callable[[float], float], a: float, b: float) -> Tuple[float, float]:
    """Порівняння з результатом scipy.integrate.quad"""
    result: float
    error: float
    result, error = spi.quad(func, a, b)
    return result, error


if __name__ == "__main__":
    a: float = 0
    b: float = 2

    print("=" * 60)
    print("Обчислення інтеграла f(x) = x² від 0 до 2 методом Монте-Карло")
    print("=" * 60)

    analytical_result: float = analytical_solution(a, b)
    print(f"1. Аналітичне розв'язання:  {analytical_result:.6f}")

    scipy_result: float
    scipy_error: float
    scipy_result, scipy_error = compare_with_scipy(f, a, b)
    print(f"2. Результат SciPy: {scipy_result:.6f} ± {scipy_error:.2e}")

    print("\n3. Метод Монте-Карло з різною кількістю точок:")
    point_counts: list[int] = [1000, 10000, 100000, 500000]

    for n_points in point_counts:
        mc_result: float = monte_carlo_integration(f, a, b, n_points)
        error: float = abs(mc_result - analytical_result)
        relative_error: float = (error / analytical_result) * 100
        print(f"   N = {n_points:7d}: Результат = {mc_result:.6f}, "
              f"Помилка = {error:.6f} ({relative_error:.2f}%)")

    print(f"\n4. Виконання 50 експериментів по 10000 точок:")
    avg_result: float
    all_results: list[float]
    avg_result, all_results = monte_carlo_multiple_experiments(f, a, b, 10000, 50)

    error = abs(avg_result - analytical_result)
    relative_error = (error / analytical_result) * 100
    std_dev: float = np.std(all_results)

    print(f"   Середній результат: {avg_result:.6f}")
    print(f"   Стандартне відхилення: {std_dev:.6f}")
    print(f"   Помилка: {error:.6f} ({relative_error:.3f}%)")

    print(f"\n5. Залежність точності від кількості експериментів (по 5000 точок кожен):")
    experiment_counts: list[int] = [1, 10, 50, 100]

    for n_exp in experiment_counts:
        avg_result, _ = monte_carlo_multiple_experiments(f, a, b, 5000, n_exp)
        error = abs(avg_result - analytical_result)
        relative_error = (error / analytical_result) * 100
        print(f"   {n_exp:3d} експериментів: Результат = {avg_result:.6f}, "
              f"Помилка = {relative_error:.3f}%")

    print("\n" + "=" * 60)
    print("ВИСНОВКИ:")
    print("=" * 60)
    print(f"Аналітичний результат:        {analytical_result:.6f}")
    print(f"SciPy результат:              {scipy_result:.6f}")
    print(f"Монте-Карло (50 експ.):       {avg_result:.6f}")
    print(f"Відносна помилка МК:          {relative_error:.3f}%")
