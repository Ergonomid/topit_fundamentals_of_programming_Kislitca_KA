
from __future__ import annotations

MEASUREMENTS = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]


def aggregate(values):

    if not values:
        return {"total": 0, "minimum": None, "maximum": None, "even": 0, "average": None, 'above_average': None}

    total = 0
    minimum = values[0]
    maximum = values[0]
    even = 0
    count = 0


    for value in values:
        count += 1
        total += value
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
        if value % 2 == 0:
            even += 1

    average = total/count
    above_average = 0

    for value in values:
        if value > average:
            above_average += 1


    return {"total": total, "minimum": minimum, "maximum": maximum, "even": even, "average": average, "above_average": above_average}


def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def linear_search_counted(values, target):
    comparisons = 0
    for index, value in enumerate(values):
        comparisons += 1
        if value == target:
            return index, comparisons
    return -1, comparisons


def is_prime(number):

    if number < 2:
        return False

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def selection_sort(values):
  
    result = list(values)
    size = len(result)
    for i in range(size - 1):
        min_index = i
        for j in range(i + 1, size):
            if result[j] < result[min_index]:
                min_index = j
        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]
    return result


def binary_search_counted(values, target):

    low = 0
    high = len(values) - 1
    comparisons = 0

    while low <= high:
        middle = (low + high) // 2
        comparisons += 1
        if values[middle] == target:
            return middle, comparisons
        comparisons += 1
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1, comparisons


def demo_aggregate():
    print("=" * 78)
    print("Один проход по измерениям:", MEASUREMENTS)
    stats = aggregate(MEASUREMENTS)
    print(f"Сумма:              {stats['total']}")
    print(f"Минимум:            {stats['minimum']}")
    print(f"Максимум:           {stats['maximum']}")
    print(f"Чётных значений:    {stats['even']}")
    print(f"Среднее:            {stats['average']}")
    print(f"Выше среднего:      {stats['above_average']}")


def demo_search():
    print( "=" * 78)
    print("Линейный поиск первого вхождения")
    for target in (18, 7, 42):
        index, comparisons = linear_search_counted(MEASUREMENTS, target)
        print(f"  ищем {target:>2}: индекс = {index:>2}, сравнений = {comparisons}")

    raw = input("Введите число для поиска: ").strip()
    target = int(raw)
    index = linear_search(MEASUREMENTS, target)
    print(f"  введено {target}: результат {index}")


def demo_prime():
    print( "=" * 78)
    print("Проверка простоты (делители до sqrt(n))")
    for number in (1, 2, 17, 25, 97, 99, 7919, 7917):
        print(f"  {number:>5}: {'простое' if is_prime(number) else 'составное'}")


def build_dataset(size):
    values = [((index * 37) % size) for index in range(size)]
    target = size + 1
    return values, target


def demo_comparison_table():
    print( "=" * 78)
    print("Сравнение числа сравнений: линейный и бинарный поиск")
    print(f"{'n':>5} | {'линейный':>9} | {'бинарный':>9} | данные")
    for size in (10, 100, 1000):
        values, target = build_dataset(size)
        _, linear_comparisons = linear_search_counted(values, target)
        ordered = selection_sort(values)
        _, binary_comparisons = binary_search_counted(ordered, target)
        print(f"{size:>5} | {linear_comparisons:>9} | {binary_comparisons:>9} | "
              f"ищем отсутствующее значение {target}")

    sample = [18, 7, 21, 9, 15]
    ordered = selection_sort(sample)
    print("\nСортировка выбором:", sample, "->", ordered)
    assert ordered == [7, 9, 15, 18, 21]
    assert binary_search_counted(ordered, 18)[0] == 3


def main():
    print("Задание 2. Циклы и базовые алгоритмы")
    demo_aggregate()
    demo_search()
    demo_prime()
    demo_comparison_table()


if __name__ == "__main__":
    main()