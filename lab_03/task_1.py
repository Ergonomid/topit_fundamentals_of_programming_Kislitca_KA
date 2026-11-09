from __future__ import annotations

LEVELS = (
    "недостаточный",
    "удовлетворительный",
    "хороший",
    "отличный",
)
LEVEL_STEP = {name: index for index, name in enumerate(LEVELS)}

WORK_TYPE_TITLES = {
    "exam": "экзаменационная работа",
    "project": "проектная работа",
    "practice": "практическая работа",
}

RECORDS = [
    (90, "exam", 1),
    (75, "project", 2),
    (74, "practice", 0),
    (89, "exam", 4),
    (60, "project", 5),
    (59, "practice", 1),
    (100, "exam", 0),
    (90, "project", 3),
    (45, "practice", 4),
    (0, "exam", 2),
]


test_scenarios = [
        (0, "exam", 0),
        (59, "practice", 2),
        (60, "project", 0),
        (74, "exam", 3),
        (75, "practice", 4),
        (89, "project", 0),
        (90, "exam", 5),
        (100, "project", 1),
]

def check_ranges(score, absences):
    errors = []

    if score < 0:
        errors.append(f"Результат {score} меньше допустимого минимума 0.")
    elif score > 100:
        errors.append(f"Результат {score} больше допустимого максимума 100.")
    else:
        pass

    if absences < 0:
        errors.append(f"Количество пропусков {absences} не может быть отрицательным.")
    elif absences > 5:
        errors.append(f"Количество пропусков {absences} больше допустимого максимума 5.")
    else:
        pass

    return errors


def level_by_score(score):
    if not 0 <= score <= 100:
        raise ValueError(f"Результат должен быть в диапазоне 0–100, получено {score}")

    if score >= 90:
        return "отличный"
    elif score >= 75:
        return "хороший"
    elif score >= 60:
        return "удовлетворительный"
    else:
        return "недостаточный"


def shift_level(level, steps = 1):
    index = LEVEL_STEP[level]
    return LEVELS[max(0, index - steps)]


def classify(score, absences):
    level = level_by_score(score)
    if absences > 3:
        level = shift_level(level)
    return level

def explain_work_type(work_type):
    match work_type:
        case "exam":
            return "Экзаменационная работа"
        case "project":
            return "Проектная работа"
        case "practice":
            return "Практическая работа"
        case _:
            return f"Неизвестный тип работы: {work_type}"


def format_record(score, work_type, absences):
    errors = check_ranges(score, absences)
    if errors:
        reason = " ".join(errors)
        return f"ОШИБКА: {reason} Классификация не выполнена."

    level = classify(score, absences)
    explanation = explain_work_type(work_type)
    return (
        f"Результат {score:>3} | {explanation:<26} | "
        f"пропуски: {absences} | уровень: {level}"
    )



def demo_single_record(score: int, work_type: str, absences: int) -> None:
    print('=' * 78)
    print("Запись:", f"score={score}, work_type={work_type!r}, absences={absences}")
    print(format_record(score, work_type, absences))
    if not check_ranges(score, absences):
        print("Пояснение типа работы:", explain_work_type(work_type))
        if work_type not in WORK_TYPE_TITLES:
            print("Внимание: неизвестный тип работы, использована ветвь case _.")


def demo_boundaries():
    print('=' * 78)
    print("Граничные сценарии")
    for score, work_type, absences in test_scenarios:
        level = classify(score, absences)
        print(f"{score:>5} | {work_type:<9} | {absences:>5} | {level}")


def demo_invalid_records():
    print('=' * 78)
    print("Некорректные данные (классификация не выполняется)")
    for score, work_type, absences in [(-1, "exam", 0), (101, "exam", 0),
                                       (50, "exam", 6), (50, "exam", -1)]:
        print(format_record(score, work_type, absences))


def process_records(records):

    lines = []
    summary = {level: 0 for level in LEVELS}

    for index, (score, work_type, absences) in enumerate(records, start=1):
        line = format_record(score, work_type, absences)
        lines.append(f"{index:>2}. {line}")
        if not check_ranges(score, absences):
            summary[classify(score, absences)] += 1

    return lines, summary


def demo_records():
    print('=' * 7)
    lines, summary = process_records(RECORDS)
    for line in lines:
        print(line)
    for level in reversed(LEVELS):
        print(f"  {level:<21} {summary[level]}")
    print("Всего записей:", len(RECORDS))

def main():
    print("Задание 1. Условия и классификация данных")
    line=list(input().split())
    score, work_type, absences = int(line[0]), str(line[1]), int(line[2])
    demo_single_record(score, work_type, absences)
    demo_boundaries()
    demo_invalid_records()
    demo_records()


if __name__ == "__main__":
    main()