import json
from datetime import datetime

def save_tasks(file_name, tasks):
    with open(file_name, 'w') as f:
        json.dump(tasks, f, indent=4)

def load_tasks(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class Task:
    def __init__(self, title, category, due_date, status="Pending"):
        self.title = title
        self.category = category
        self.due_date = due_date
        self.status = status

    def mark_completed(self):
        self.status = "Completed"

    def __repr__(self):
        return f"{self.title} ({self.category}) - Due: {self.due_date} [{self.status}]"

class TaskManager:
    def __init__(self, file_name="task_data.json"):
        self.file_name = file_name
        self.tasks = load_tasks(file_name)

    def add_task(self, title, category, due_date):
        if not title or not validate_date(due_date):
            print("Invalid title or date format. Use YYYY-MM-DD.")
            return
        new_task = Task(title, category, due_date)
        self.tasks.append(vars(new_task))
        save_tasks(self.file_name, self.tasks)
        print(f"Task '{title}' added successfully!")

    def update_task(self, title, new_status):
        for task in self.tasks:
            if task["title"] == title:
                task["status"] = new_status
                save_tasks(self.file_name, self.tasks)
                print(f"Task '{title}' updated to '{new_status}'.")
                return
        print("Task not found.")

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task["title"] != title]
        save_tasks(self.file_name, self.tasks)
        print(f"Task '{title}' deleted.")

    def view_tasks(self, filter_by=None):
        filtered_tasks = self.tasks if not filter_by else [t for t in self.tasks if t["status"] == filter_by]
        if not filtered_tasks:
            print("No tasks found.")
        else:
            for task in filtered_tasks:
                print(f"{task['title']} ({task['category']}) - Due: {task['due_date']} [{task['status']}]")

    def view_due_today(self):
        today = datetime.today().strftime('%Y-%m-%d')
        due_today = [task for task in self.tasks if task["due_date"] == today]
        if due_today:
            print("Tasks due today:")
            for task in due_today:
                print(f"- {task['title']} ({task['category']})")
        else:
            print("No tasks due today!")

if __name__ == "__main__":
    manager = TaskManager()
    while True:
        print("\n1. Add Task  2. Update Task  3. Delete Task  4. View Tasks  5. View Due Today  6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            title = input("Task Title: ")
            category = input("Category: ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            manager.add_task(title, category, due_date)
        elif choice == "2":
            title = input("Task Title to Update: ")
            new_status = input("New Status (Pending/Completed): ")
            manager.update_task(title, new_status)
        elif choice == "3":
            title = input("Task Title to Delete: ")
            manager.delete_task(title)
        elif choice == "4":
            filter_by = input("Filter by (Pending/Completed) or press Enter to view all: ")
            manager.view_tasks(filter_by if filter_by else None)
        elif choice == "5":
            manager.view_due_today()
        elif choice == "6":
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid choice. Try again!")
