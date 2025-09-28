COINS_LIST = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(sum_to_change: int, coins: list[int] = COINS_LIST) -> dict[int, int]:
    """Жадібний алгоритм для розміну монет."""
    result: dict[int, int] = {}
    remaining: int = sum_to_change

    for coin in coins:
        if remaining >= coin:
            count: int = remaining // coin
            if count > 0:
                result[coin] = count
                remaining -= coin * count

        if remaining == 0:
            break

    return result


def find_min_coins(sum_to_change: int, coins: list[int] = COINS_LIST) -> dict[int, int]:
    """Динамічне програмування для знаходження мінімальної кількості монет."""
    dp: list[float] = [float('inf')] * (sum_to_change + 1)
    dp[0] = 0
    parent: list[int] = [-1] * (sum_to_change + 1)

    for amount in range(1, sum_to_change + 1):
        for coin in coins:
            if coin <= amount and dp[amount - coin] + 1 < dp[amount]:
                dp[amount] = dp[amount - coin] + 1
                parent[amount] = coin

    if dp[sum_to_change] == float('inf'):
        return {}

    result: dict[int, int] = {}
    current: int = sum_to_change

    while current > 0:
        coin: int = parent[current]
        result[coin] = result.get(coin, 0) + 1
        current -= coin

    return result


if __name__ == "__main__":
    import time
    import timeit

    test_amount: int = 113

    print(f"Розмін суми {test_amount}:")
    print("=" * 50)

    greedy_time = timeit.timeit(lambda: find_coins_greedy(test_amount), number=1000) / 1000
    greedy_result: dict[int, int] = find_coins_greedy(test_amount)
    print(f"Жадібний алгоритм: {greedy_result}")
    print(f"Загальна кількість монет: {sum(greedy_result.values())}")
    print(f"Час виконання: {greedy_time:.8f} секунд")

    dp_time = timeit.timeit(lambda: find_min_coins(test_amount), number=1000) / 1000
    dp_result: dict[int, int] = find_min_coins(test_amount)
    print(f"Динамічне програмування: {dp_result}")
    print(f"Загальна кількість монет: {sum(dp_result.values())}")
    print(f"Час виконання: {dp_time:.8f} секунд")

    greedy_sum: int = sum(coin * count for coin, count in greedy_result.items())
    dp_sum: int = sum(coin * count for coin, count in dp_result.items())

    print(f"\nПеревірка:")
    print(f"Жадібний: {greedy_sum} == {test_amount} -> {greedy_sum == test_amount}")
    print(f"ДП: {dp_sum} == {test_amount} -> {dp_sum == test_amount}")

    print(f"\nПорівняння продуктивності:")
    if greedy_time > 0:
        print(f"Жадібний алгоритм швидший у {dp_time/greedy_time:.2f} разів")
    else:
        print("Жадібний алгоритм виконується занадто швидко для точного вимірювання")

    print(f"\nТестування на великих сумах:")
    large_amounts = [1000, 5000, 10000]

    for amount in large_amounts:
        print(f"\nСума: {amount}")

        greedy_large_time = timeit.timeit(lambda: find_coins_greedy(amount), number=100) / 100
        greedy_large = find_coins_greedy(amount)

        dp_large_time = timeit.timeit(lambda: find_min_coins(amount), number=10) / 10
        dp_large = find_min_coins(amount)

        print(f"Жадібний: {sum(greedy_large.values())} монет, час: {greedy_large_time:.8f}с")
        print(f"ДП: {sum(dp_large.values())} монет, час: {dp_large_time:.8f}с")

        if greedy_large_time > 0:
            print(f"Різниця в швидкості: {dp_large_time/greedy_large_time:.2f}x")
        else:
            print("Жадібний алгоритм занадто швидкий для точного порівняння")
