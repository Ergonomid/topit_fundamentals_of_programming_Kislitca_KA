from __future__ import annotations

from collections.abc import Iterable

STUDENTS: dict[str, list[int]] = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}

NO_DATA = "без результатов"

CATEGORY_BOUNDS: tuple[tuple[int, str], ...] = (
    (90, "отличный"),
    (75, "хороший"),
    (60, "удовлетворительный"),
    (0, "недостаточный"),
)
CATEGORIES: tuple[str, ...] = tuple(name for _, name in CATEGORY_BOUNDS) + (NO_DATA,)


def mean(values):
    if not values:
        return None
    total = 0.0
    count = 0
    for value in values:
        count += 1
        total += value
    return total / count


def minimum(values):
    iterator = iter(values)
    first = next(iterator, None)
    if first is None:
        return None
    result = first
    for value in iterator:
        if value < result:
            result = value
    return result


def maximum(values):
    iterator = iter(values)
    first = next(iterator, None)
    if first is None:
        return None
    result = first
    for value in iterator:
        if value > result:
            result = value
    return result


def classify(score):
    if score is None:
        return NO_DATA
    for lower_bound, name in CATEGORY_BOUNDS:
        if score >= lower_bound:
            return name
    return CATEGORY_BOUNDS[-1][1]


def student_summary(name, results):
    if not name or not name.strip():
        raise ValueError("Имя студента не может быть пустым")

    snapshot = list(results)
    average = mean(snapshot)
    category = classify(average)

    return {
        "name": name,
        "count": len(snapshot),
        "mean": average,
        "min": minimum(snapshot),
        "max": maximum(snapshot),
        "category": category,
    }


def group_summary(students):
    summaries = [student_summary(name, results) for name, results in students.items()]
    all_scores = [score for results in students.values() for score in results]

    categories = {name: 0 for name in CATEGORIES}
    for summary in summaries:
        categories[str(summary["category"])] += 1

    return {
        "students_total": len(students),
        "grades_total": len(all_scores),
        "overall_mean": mean(all_scores),
        "students": summaries,
        "categories": categories,
        "top_students": find_top_students(students),
        "ranking": build_ranking(students),
    }


def find_top_students(students):
    best_average: float | None = None
    leaders: list[str] = []

    for name, results in students.items():
        average = mean(list(results))
        if average is None:
            continue
        if best_average is None or average > best_average:
            best_average = average
            leaders = [name]
        elif average == best_average:
            leaders.append(name)

    return leaders


def build_ranking(students):
    items = [(name, mean(list(results))) for name, results in students.items()]
    ordered = []
    for item in items:
        position = 0
        while position < len(ordered) and _ranks_before(ordered[position], item):
            position += 1
        ordered.insert(position, item)
    return ordered


def _ranks_before(left, right):
    left_value, right_value = left[1], right[1]
    if left_value is None:
        return False
    if right_value is None:
        return True
    return left_value >= right_value


def format_report(student_data, group_data):
    lines: list[str] = []
    lines.append("АНАЛИЗ УЧЕБНЫХ РЕЗУЛЬТАТОВ")
    lines.append(f"{'Студент':<10} {'Оценок':>6} {'Среднее':>9} "
                 f"{'Мин':>5} {'Макс':>5}  Категория")
    for data in student_data:
        average = data["mean"]
        mean_text = "—" if average is None else f"{average:>9.2f}"
        minimum_text = "—" if data["min"] is None else f"{data['min']:>5}"
        maximum_text = "—" if data["max"] is None else f"{data['max']:>5}"
        lines.append(
            f"{str(data['name']):<10} {data['count']:>6} {mean_text:>9} "
            f"{minimum_text:>5} {maximum_text:>5}  {data['category']}"
        )

    overall = group_data["overall_mean"]
    lines.append(f"Студентов в группе: {group_data['students_total']}, "
                 f"оценок: {group_data['grades_total']}")
    lines.append("Общий средний результат: "
                 + ("—" if overall is None else f"{overall:.2f}"))

    leaders = group_data["top_students"]
    if leaders:
        leader_mean = next(
            (data["mean"] for data in student_data if data["name"] == leaders[0]),
            None,
        )
        mean_text = "—" if leader_mean is None else f"{float(leader_mean):.2f}"
        lines.append(f"Лидер(ы): {', '.join(leaders)} (среднее {mean_text})")
    else:
        lines.append("Лидер не определён: нет студентов с результатами.")

    lines.append("\nРаспределение по категориям:")
    categories = group_data["categories"]
    for name, count in categories.items():
        lines.append(f"  {name:<21} {count}")

    lines.append("\nРейтинг по среднему результату:")
    for position, (name, average) in enumerate(group_data["ranking"], start=1): 
        value = "—" if average is None else f"{float(average):.2f}"
        lines.append(f"  {position:>2}. {name:<10} {value}")

    return "\n".join(lines)


def demo_main_data():
    print("Задание 5. Анализатор учебных результатов")
    print("Исходные данные:", STUDENTS)
    snapshot = {name: list(results) for name, results in STUDENTS.items()}

    group_data = group_summary(STUDENTS)
    student_data = group_data["students"]
    print()
    print(format_report(student_data, group_data))

    assert STUDENTS == snapshot, "исходный словарь не изменён"


build_scenarios = [
        ("обычный набор данных", STUDENTS),
        ("один студент", {"Анна": [78, 91]}),
        ("несколько лидеров", {"Анна": [90, 90], "Борис": [90, 90], "Илья": [55]}),
        ("пустая группа", {}),
        ("студент без результатов", {"Анна": [80], "Илья": []}),
        ("границы категорий", {"A": [59], "B": [60], "C": [74], "D": [75],
                              "E": [89], "F": [90], "G": [100]}),
]


def demo_scenarios():
    print( "=" * 78)
    print("Сценарии проверки")
    print(f"{'Сценарий':<27} {'Студентов':>9} {'Оценок':>7} {'Среднее':>8}  Лидеры")
    for title, data in build_scenarios:
        summary = group_summary(data)
        overall = summary["overall_mean"]
        overall_text = "—" if overall is None else f"{float(overall):.2f}"
        leaders = ", ".join(summary["top_students"]) or "—"
        print(f"{title:<27} {summary['students_total']:>9} "
              f"{summary['grades_total']:>7} {overall_text:>8}  {leaders}")



def main():
    demo_main_data()
    demo_scenarios()


if __name__ == "__main__":
    main()