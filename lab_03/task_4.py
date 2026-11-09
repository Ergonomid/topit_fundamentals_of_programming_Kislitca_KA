from __future__ import annotations

from collections.abc import Callable, Iterable

course = "Python"


def arithmetic_mean(values):
    if not values:
        return float("nan")
    total = 0.0
    count = 0
    for value in values:
        count += 1
        total += value
    return total / count


def normalize_name(name):
    if not name or not name.strip():
        return ""
    parts = name.split()
    return " ".join(part[0].upper() + part[1:].lower() for part in parts)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    if not results:
        return f"{prefix}: {student} — нет данных"
    if precision < 0:
        precision = 0

    total = 0
    minimum = maximum = results[0]
    count = 0

    for value in results:
        count += 1
        total += value
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value

    average = total / count
    return (
        f"{prefix}: {student} — среднее {average:.{precision}f}, "
        f"минимум {minimum}, максимум {maximum}, попыток {len(results)}"
    )


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned:  # пустые значения пропускаются
            continue
        key = cleaned.lower() if lowercase else cleaned
        if key in seen:
            continue
        seen.add(key)
        result.append(key)
    return tuple(result)

def run_asserts():
    print( "=" * 78)
    print("Проверки assert")

    # arithmetic_mean
    assert arithmetic_mean([2, 4, 6]) == 4.0
    assert arithmetic_mean([5]) == 5.0
    assert arithmetic_mean([1, 2]) == 1.5
    nan = arithmetic_mean([])
    assert nan != nan, "для пустого списка возвращается NaN"

    # normalize_name
    assert normalize_name("  иВАН   иВАНОВ ") == "Иван Иванов"
    assert normalize_name("анна") == "Анна"
    assert normalize_name("   ") == ""
    assert normalize_name("") == ""

    # build_report
    report = build_report("Анна", [78, 91, 84, 88], precision=2)
    assert "среднее 85.25" in report
    assert "минимум 78" in report and "максимум 91" in report
    assert build_report("Илья", []) == "Результат: Илья — нет данных"
    assert build_report("Илья", [61], prefix="Итог") == \
        "Итог: Илья — среднее 61.00, минимум 61, максимум 61, попыток 1"

    # collect_tags
    assert collect_tags("a", "A", "b") == ("a", "b")
    assert collect_tags("a", "A", "b", lowercase=False) == ("a", "A", "b")
    assert collect_tags("", "  ", "x") == ("x",)
    assert collect_tags() == ()

    print("Все assert-проверки пройдены.")


def demo_calls():
    print( "=" * 78)
    print("Вызовы функций")

    print("Позиционные:", build_report("Анна", [78, 91, 84, 88]))
    print("Именованные:", build_report(student="Борис", results=[60, 72, 68],
                                     precision=1, prefix="Итог"))

    positional_values = [95, 93, 97, 90]
    print("Распаковка списка *:", build_report("Дарья", *[positional_values]))
    print("Распаковка словаря **:", build_report(
        **{"student": "Илья", "results": [55, 61, 70], "precision": 1}
    ))

    tags = ["  Python ", "GIT "]
    print("collect_tags(*tags):", collect_tags(*tags, lowercase=False))
    options = {"lowercase": True}
    print("collect_tags(**options):", collect_tags("Python", "Git", **options))

    print("normalize_name:", normalize_name("  дАРЬЯ    кУЗНЕЦОВА  "))
    print("arithmetic_mean:", arithmetic_mean([10, 20, 30]))


def outer_scope_demo():
    count = 0 

    def inner() -> str:
        nonlocal count   
        count += 1
        label = f"inner call #{count}"   
        return f"{label}, course={course}"  

    first = inner()
    second = inner()
    result_from_inner = f"{first} | {second}"
    return result_from_inner, str(count), course


def demo_legb() -> None:
    print("\n" + "=" * 78)
    print("Исследование LEGB")
    result, counter, global_course = outer_scope_demo()
    print("Результат вложенной функции:", result)
    print("Значение counter после двух вызовов:", counter)
    print("Глобальное имя course:", global_course, "(не изменялось)")
    assert global_course == "Python"
    assert counter == "2"


def add_result(value, results: list[int] | None = None):
    if results is None:
        return [value]
    if not isinstance(results, list):
        raise TypeError("results должен быть списком или None")
    return [*results, value]


def demo_default_argument():
    print( "=" * 78)
    print("Ошибка изменяемого значения по умолчанию")
    def broken(value, results = []):
        results.append(value)
        return results
    first = broken(1)
    second = broken(2)
    print("Ошибочная функция: broken(1) ->", first, "| broken(2) ->", second)
    print("Оба вызова вернули ОДИН и тот же объект: id =", id(first), id(second))
    assert first is second, "ошибка воспроизведена: список общий"

    fixed_first = add_result(1)
    fixed_second = add_result(2)
    print("Исправленная функция: ->", fixed_first, "| ->", fixed_second)
    assert fixed_first == [1] and fixed_second == [2]
    assert fixed_first is not fixed_second

    explicit: list[int] = [10]
    returned = add_result(3, explicit)
    print("С переданным списком:", explicit, "-> вернулось", returned)
    assert explicit == [10], "переданный список не изменяется"
    assert returned == [10, 3]
    assert add_result.__defaults__ == (None,)


def apply_to_results(operation, values):
    return [operation(value) for value in values]


def make_threshold_checker(threshold):
    if threshold < 0:
        raise ValueError("Порог должен быть неотрицательным")

    def checker(value: int) -> bool:
        return value >= threshold

    return checker


def is_excellent(value):
    return value >= 90


def demo_higher_order() -> None:
    print( "=" * 78)
    print("Функции высших порядков и замыкания")
    results = [78, 91, 84, 88, 59]

    print("Именованная функция is_excellent:",
          apply_to_results(is_excellent, results))
    print("lambda x: x >= 80:",
          apply_to_results(lambda value: value >= 80, results))
    print("Без изменения исходных данных:", results)

    passed_60 = make_threshold_checker(60)
    passed_85 = make_threshold_checker(85)
    print("Порог 60:", apply_to_results(passed_60, results))
    print("Порог 85:", apply_to_results(passed_85, results))
    print("Замыкания независимы:",
          [value for value in results if passed_60(value) and not passed_85(value)])

    assert passed_60.__closure__ is not None
    assert passed_60.__closure__[0].cell_contents == 60
    assert passed_85.__closure__[0].cell_contents == 85


def main() -> None:
    print("Задание 4. Функции, параметры и области видимости")
    run_asserts()
    demo_calls()
    demo_legb()
    demo_default_argument()
    demo_higher_order()


if __name__ == "__main__":
    main()