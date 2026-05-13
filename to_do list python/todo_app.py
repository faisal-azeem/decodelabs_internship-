import json
import os
import sys
from datetime import datetime

# --- Constants & Configuration ---
DATA_FILE = "tasks.json"

# ANSI Color Codes for a premium CLI experience
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Core Logic (Process) ---

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except IOError as e:
        print(f"{Colors.FAIL}Error saving tasks: {e}{Colors.ENDC}")

def add_task(tasks, title):
    """Add a new task to the list."""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"\n{Colors.OKGREEN}Done: Task added successfully!{Colors.ENDC}")

def view_tasks(tasks):
    """Display all tasks in a formatted table."""
    if not tasks:
        print(f"\n{Colors.WARNING}No tasks found. Your to-do list is empty!{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}{Colors.OKBLUE}{'='*60}")
    print(f"{'ID':<5} {'Status':<10} {'Task Title':<30} {'Created At'}")
    print(f"{'='*60}{Colors.ENDC}")

    for task in tasks:
        status_color = Colors.OKGREEN if task["status"] == "Done" else Colors.WARNING
        print(f"{task['id']:<5} {status_color}{task['status']:<10}{Colors.ENDC} {task['title']:<30} {task['created_at']}")
    
    print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")

def mark_task_done(tasks, task_id):
    """Mark a specific task as completed."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Done"
            save_tasks(tasks)
            print(f"\n{Colors.OKGREEN}Done: Task #{task_id} marked as done!{Colors.ENDC}")
            return
    print(f"\n{Colors.FAIL}Error: Task ID {task_id} not found.{Colors.ENDC}")

def delete_task(tasks, task_id):
    """Delete a task from the list."""
    original_len = len(tasks)
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) < original_len:
        # Re-index IDs to keep them sequential
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        save_tasks(tasks)
        print(f"\n{Colors.OKGREEN}Done: Task #{task_id} deleted.{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}Error: Task ID {task_id} not found.{Colors.ENDC}")

# --- User Interface (Output/Input) ---

def show_menu():
    """Display the main interaction menu."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("+------------------------------------------+")
    print("|         DECODELABS TO-DO ENGINE          |")
    print("+------------------------------------------+")
    print(f"{Colors.ENDC}")
    print(f"{Colors.OKCYAN}1.{Colors.ENDC} View Tasks")
    print(f"{Colors.OKCYAN}2.{Colors.ENDC} Add New Task")
    print(f"{Colors.OKCYAN}3.{Colors.ENDC} Mark Task as Done")
    print(f"{Colors.OKCYAN}4.{Colors.ENDC} Delete Task")
    print(f"{Colors.OKCYAN}5.{Colors.ENDC} Exit")
    print("-" * 44)

def main():
    """Main application loop."""
    # Ensure terminal supports ANSI colors on Windows
    if os.name == 'nt':
        os.system('color')

    tasks = load_tasks()

    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}Select an option (1-5): {Colors.ENDC}").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            title = input(f"{Colors.OKCYAN}Enter task title: {Colors.ENDC}").strip()
            if title:
                add_task(tasks, title)
            else:
                print(f"{Colors.FAIL}Task title cannot be empty!{Colors.ENDC}")
        elif choice == '3':
            view_tasks(tasks)
            try:
                tid = int(input(f"{Colors.OKCYAN}Enter Task ID to complete: {Colors.ENDC}"))
                mark_task_done(tasks, tid)
            except ValueError:
                print(f"{Colors.FAIL}Invalid ID. Please enter a number.{Colors.ENDC}")
        elif choice == '4':
            view_tasks(tasks)
            try:
                tid = int(input(f"{Colors.OKCYAN}Enter Task ID to delete: {Colors.ENDC}"))
                delete_task(tasks, tid)
            except ValueError:
                print(f"{Colors.FAIL}Invalid ID. Please enter a number.{Colors.ENDC}")
        elif choice == '5':
            print(f"\n{Colors.OKBLUE}Saving data... Goodbye!{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please try again.{Colors.ENDC}")
        
        input(f"\n{Colors.OKBLUE}Press Enter to continue...{Colors.ENDC}")
        # Clear screen for better experience (optional)
        # os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Program interrupted. Exiting...{Colors.ENDC}")
        sys.exit(0)
