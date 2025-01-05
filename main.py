import json
from datetime import datetime


class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла"""
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        """Сохранение задач в файл"""
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=2)

    def add_task(self):
        """Добавление новой задачи"""
        task = input("Введите задачу: ")

        # Добавляем категорию
        print("\nДоступные категории: работа, дом, учеба, другое")
        category = input("Введите категорию задачи: ").lower()

        # Добавляем приоритет
        print("\nПриоритеты: 1 (высокий), 2 (средний), 3 (низкий)")
        while True:
            try:
                priority = int(input("Введите приоритет задачи (1-3): "))
                if 1 <= priority <= 3:
                    break
                print("Пожалуйста, введите число от 1 до 3")
            except ValueError:
                print("Пожалуйста, введите число!")

        # Добавляем срок выполнения
        while True:
            due_date = input("Введите срок выполнения (дд.мм.гггг): ")
            try:
                due_date = datetime.strptime(due_date, "%d.%m.%Y").strftime("%d.%m.%Y")
                break
            except ValueError:
                print("Неверный формат даты! Используйте формат дд.мм.гггг")

        new_task = {
            "task": task,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%d.%m.%Y")
        }

        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена!")

    def view_tasks(self):
        """Просмотр всех задач"""
        if not self.tasks:
            print("Список задач пуст!")
            return

        print("\nСписок задач:")
        for index, task in enumerate(self.tasks, 1):
            status = "✓" if task["completed"] else " "
            priority_symbol = "❗" * (4 - task["priority"])
            print(
                f"{index}. [{status}] {priority_symbol} "
                f"{task['task']} "
                f"(Категория: {task['category']}, "
                f"Срок: {task['due_date']})"
            )

    def mark_completed(self):
        """Отметка задачи как выполненной"""
        self.view_tasks()
        if not self.tasks:
            return

        try:
            task_index = int(input("Введите номер выполненной задачи: ")) - 1
            if 0 <= task_index < len(self.tasks):
                self.tasks[task_index]["completed"] = True
                self.save_tasks()
                print("Задача отмечена как выполненная!")
            else:
                print("Неверный номер задачи!")
        except ValueError:
            print("Пожалуйста, введите число!")

    def delete_task(self):
        """Удаление задачи"""
        self.view_tasks()
        if not self.tasks:
            return

        try:
            task_index = int(input("Введите номер задачи для удаления: ")) - 1
            if 0 <= task_index < len(self.tasks):
                deleted_task = self.tasks.pop(task_index)
                self.save_tasks()
                print(f"Задача '{deleted_task['task']}' удалена!")
            else:
                print("Неверный номер задачи!")
        except ValueError:
            print("Пожалуйста, введите число!")

    def view_by_category(self):
        """Просмотр задач по категориям"""
        category = input("Введите категорию для фильтрации: ").lower()
        filtered_tasks = [task for task in self.tasks if task["category"].lower() == category]

        if not filtered_tasks:
            print(f"Нет задач в категории '{category}'")
            return

        print(f"\nЗадачи в категории '{category}':")
        for index, task in enumerate(filtered_tasks, 1):
            status = "✓" if task["completed"] else " "
            priority_symbol = "❗" * (4 - task["priority"])
            print(
                f"{index}. [{status}] {priority_symbol} "
                f"{task['task']} "
                f"(Срок: {task['due_date']})"
            )


def main():
    todo = TodoList()

    while True:
        print("\n=== Менеджер задач ===")
        print("1. Добавить задачу")
        print("2. Посмотреть все задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Удалить задачу")
        print("5. Посмотреть задачи по категории")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ")

        if choice == "1":
            todo.add_task()
        elif choice == "2":
            todo.view_tasks()
        elif choice == "3":
            todo.mark_completed()
        elif choice == "4":
            todo.delete_task()
        elif choice == "5":
            todo.view_by_category()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 6.")


if __name__ == "__main__":
    main()