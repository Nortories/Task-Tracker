import os
import json
from datetime import timedelta

file_name = "task.json"
file_path = os.path.join(os.path.dirname(__file__), file_name)


def check_task_file():

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({"tasks": []}, file)
            print("task.json created successfully!")
    return


def add_task(title, description):
    check_task_file()
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing tasks
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])

        # Get the taskID of the last task
        last_task = tasks[-1] if tasks else None
        last_task_id = last_task["taskID"] if last_task else 0

        # Create a new task
        new_task = {
            "title": title,
            "description": description,
            "taskID": last_task_id + 1,
            "timer": "00:00:00",
            "completed": True
        }

        # Add the new task to the tasks list
        tasks.append(new_task)

        # Update the file with the new tasks
        with open(file_path, "w") as file:
            json.dump({"tasks": tasks}, file)
            print("Task added successfully!")
    else:
        print("task.json does not exist.")


def read_tasks():
    check_task_file()
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing tasks
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])
            return tasks
    else:
        print("task.json does not exist.")
        return []


def update_task_time(task_id, time):
    check_task_file()
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing tasks
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])

        # Find the task with the given task_id
        for task in tasks:
            if task["taskID"] == task_id:
                task["timer"] = time
                break

        # Update the file with the modified tasks
        with open(file_path, "w") as file:
            json.dump({"tasks": tasks}, file)
            print("Task time updated successfully!")
    else:
        print("task.json does not exist.")


def get_task_timer(task_id):
    check_task_file()
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing tasks
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])

        # Find the task with the given task_id
        for task in tasks:
            if task["taskID"] == task_id:
                timer_str = task["timer"]
                timer_parts = timer_str.split(":")
                timer = timedelta(hours=int(timer_parts[0]), minutes=int(timer_parts[1]), seconds=int(timer_parts[2]))
                return timer

        print("Task not found.")
        return None
    else:
        print("task.json does not exist.")
        return None


def count_tasks():
    check_task_file()
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing tasks
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])
            return len(tasks)
    else:
        print("task.json does not exist.")
        return 0
