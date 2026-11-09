from __future__ import annotations

SUBMISSIONS= [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]


class SubmissionIndex:

    def __init__(self, submissions):
        self.attempts = {}
        self.best = {}
        self.counts = {}
        self.students = set()
        self.laboratories = set()
        self._submissions = list(submissions)
        for student, laboratory, result in submissions:
            self.add(student, laboratory, result)

    def add(self, student, laboratory, result):
        self.students.add(student)
        self.laboratories.add(laboratory)
        self._submissions.append((student, laboratory, result))

        self.attempts.setdefault(student, []).append((laboratory, result))

        key = (student, laboratory)
        self.counts[key] = self.counts.get(key, 0) + 1
        if key not in self.best or result > self.best[key]:
            self.best[key] = result

    def student_attempts(self, student):
        return list(self.attempts.get(student, []))

    def best_result(self, student, laboratory):
        return self.best.get((student, laboratory))

    def attempt_count(self, student, laboratory):
        return self.counts.get((student, laboratory), 0)

    def students_who_did_both(self, first, second):
        first_set = {student for (student, lab) in self.best if lab == first}
        second_set = {student for (student, lab) in self.best if lab == second}
        return first_set & second_set

    def completed_students(self, laboratory):
        return {student for (student, lab) in self.counts if lab == laboratory}


def build_structures(submissions):
    students: set[str] = set()
    laboratories: set[str] = set()
    attempts: dict[str, list[tuple[str, int]]] = {}
    best: dict[tuple[str, str], int] = {}
    counts: dict[tuple[str, str], int] = {}

    for student, laboratory, result in submissions:
        students.add(student)
        laboratories.add(laboratory)
        attempts.setdefault(student, []).append((laboratory, result))

        key = (student, laboratory)
        counts[key] = counts.get(key, 0) + 1
        if key not in best or result > best[key]:
            best[key] = result

    return students, laboratories, attempts, best, counts


def run_query(index, query):
   
    parts = query.split()
    if not parts:
        return "Пустой запрос. Доступно: student, best, attempts, completed"

    command, *arguments = parts

    match command:
        case "student":
            if len(arguments) != 1:
                return "Использование: student <имя>"
            attempts = index.student_attempts(arguments[0])
            if not attempts:
                return f"Нет данных для студента {arguments[0]}"
            return f"{arguments[0]}: попытки {attempts}"

        case "best":
            if len(arguments) != 2:
                return "Использование: best <имя> <работа>"
            student, laboratory = arguments
            result = index.best_result(student, laboratory)
            if result is None:
                return f"Нет данных для {student} / {laboratory}"
            return f"Лучший результат {student} / {laboratory}: {result}"

        case "attempts":
            if len(arguments) != 2:
                return "Использование: attempts <имя> <работа>"
            student, laboratory = arguments
            count = index.attempt_count(student, laboratory)
            if count == 0:
                return f"Нет данных для {student} / {laboratory}"
            return f"Попыток {student} / {laboratory}: {count}"

        case "completed":
            if len(arguments) != 1:
                return "Использование: completed <работа>"
            laboratory = arguments[0]
            students = index.completed_students(laboratory)
            if not students:
                return f"Работу {laboratory} никто не сдавал"
            return f"Работу {laboratory} сдавали: {', '.join(sorted(students))}"

        case _:
            return (f"Неизвестная команда: {command!r}. "
                    "Доступно: student, best, attempts, completed")


def demo_structures():
    print("=" * 78)
    print("Задание 3. Коллекции и выбор структуры данных")
    print("Исходные данные:", SUBMISSIONS)

    students, laboratories, attempts, best, counts = build_structures(SUBMISSIONS)

    print("\n1. Множество студентов:", sorted(students))
    print("2. Множество работ:   ", sorted(laboratories))
    print("3. Попытки по студентам:")
    for student in sorted(attempts):
        print(f"   {student:<6} {attempts[student]}")
    print("4. Лучшие результаты:")
    for key in sorted(best):
        print(f"   {key[0]:<6} {key[1]} -> {best[key]}")
    print("5. Количество попыток:")
    for key in sorted(counts):
        print(f"   {key[0]:<6} {key[1]} -> {counts[key]}")

    index = SubmissionIndex(SUBMISSIONS)
    both = index.students_who_did_both("lab_01", "lab_02")
    print("\nСтуденты, сдававшие обе работы:", sorted(both))


def demo_incremental_update():
    print( "=" * 78)
    print("Добавление новой записи без полного перестроения")
    index = SubmissionIndex(SUBMISSIONS)
    print("До:    daria / lab_02 ->", index.best_result("daria", "lab_02"))
    index.add("daria", "lab_02", 4)
    index.add("daria", "lab_02", 2)
    print("После: daria / lab_02 ->", index.best_result("daria", "lab_02"),
          "| попыток:", index.attempt_count("daria", "lab_02"))


def demo_queries():
    print( "=" * 78)
    print("Текстовые запросы")
    index = SubmissionIndex(SUBMISSIONS)
    queries = [
        "student anna",
        "best anna lab_01",
        "attempts boris lab_02",
        "completed lab_01",
        "best daria lab_02",
        "student roman",
        "average anna",
        "",
    ]
    for query in queries:
        print(f"  > {query!r}")
        print(f"    {run_query(index, query)}")


def main() -> None:
    demo_structures()
    demo_incremental_update()
    demo_queries()


if __name__ == "__main__":
    main()