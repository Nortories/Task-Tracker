import tkinter as tk
import customtkinter
import tasks as t
from datetime import datetime, timedelta
from tasks import read_tasks


class App(tk.Tk):
    """
    The main application class for the Task Tracker.
    """

    def __init__(self):
        """
        Initializes the App class.

        This method sets up the main window, sets the appearance mode and color theme,
        creates the widgets, and displays the tasks.
        """
        super().__init__()
        self.title("Task Tracker")
        getScreenHeight = (self.winfo_screenheight()-80)
        self.wm_geometry(
            f"500x{getScreenHeight}+{self.winfo_screenwidth()-510}+0")
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("dark-blue")
        self.create_widgets()
        self.display_tasks()

    def create_widgets(self):
        """
        Creates the widgets for the main window.

        This method creates labels and entry fields for task, description, and time,
        as well as a submit button.
        """
        container = tk.Frame(self)
        container.pack(fill=tk.X, padx=5, pady=5)

        title_label = tk.Label(container, text="Task")
        title_label.pack(side="left")
        self.task_entry = tk.Entry(container)
        self.task_entry.pack(side="left")

        description_label = tk.Label(container, text="Description")
        description_label.pack(side="left")
        self.description_entry = tk.Entry(container)
        self.description_entry.pack(side="left")

        self.warning_label = tk.Label(container)
        self.warning_label.pack(side="top")
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)
        self.submit_button = tk.Button(
            button_frame, text="Submit", command=self.submit_task)
        self.submit_button.pack(side="top")

        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left")

        self.popup_label_active = False
        self.task_timers = {}  # Dictionary to store timer information for each task

    def display_tasks(self):
        """
        Displays the tasks in the main window.

        This method retrieves the tasks from the tasks module and creates labels
        for each task, displaying them in the main window.
        """
        tasks = read_tasks()

        # Destroy old task_frame if it exists (to prevent duplicate tasks on refresh)
        if hasattr(self, "task_frame_area"):
            self.task_frame_area.destroy()

        # Create a frame to hold the task labels and pack it
        self.task_frame_area = tk.Frame(self)
        self.task_frame_area.pack(fill=tk.BOTH, expand=True)

        # Create and pack new task labels with checkboxes inside the frame
        for task in tasks:
            self.task_frame = tk.Frame(self.task_frame_area, bg="white", borderwidth=2, relief="groove")
            self.task_frame.pack(padx=5, pady=5, fill=tk.X)

            task_label = tk.Label(
                self.task_frame, bg="white", text=task["title"])
            task_label.pack(side="top")
            
            task_description = tk.Label(
                self.task_frame, bg="white", text="Description:   " + task["description"])
            task_description.pack(side="top")

            task_id = task["taskID"]
            self.task_timers[task_id] = {"label": tk.Label(self.task_frame, bg="white", text=task["timer"]),
                                         "start_time": None,
                                         "elapsed_time": timedelta(),
                                         "timer_running": False}
            self.task_timers[task_id]["label"].pack()

            toggle_button = tk.Button(
            self.task_frame, text="Start Timer",
            command=lambda id=task_id: self.toggle_timer(id)
            )
            toggle_button.pack(side="left")

            # Store the button reference
            self.task_timers[task_id]["toggle_button"] = toggle_button
            
            # Create a checkbox for each task
            if task["completed"]:
                checkmark = tk.BooleanVar(value=True)
                print("task completed")
            else:
                checkmark = tk.BooleanVar(value=False)
                print("task not completed")
            checkbox = tk.Checkbutton(self.task_frame, text="Completed", variable=checkmark)
            checkbox.pack(side="right")

        self.update_timer()

    def toggle_timer(self, task_id):
        """
        Toggles the timer for a specific task.

        This method starts or stops the timer for a specific task based on its task ID.
        If the timer is running, it stops the timer and updates the elapsed time.
        If the timer is not running, it starts the timer and initializes the elapsed time.
        """
        timer = self.task_timers[task_id]
        if timer["timer_running"]:
            timer["timer_running"] = False
            timer["elapsed_time"] += datetime.now() - timer["start_time"]
            timer["start_time"] = None
            timer["toggle_button"].config(text="Start Timer")
 
            t.update_task_time(task_id, str(timer["elapsed_time"]).split('.')[0])
        else:
            timer["timer_running"] = True
            timer["start_time"] = datetime.now()
            # Ensure this is a timedelta object
            elapsed_time_from_task = t.get_task_timer(task_id)
            if isinstance(elapsed_time_from_task, datetime):
                elapsed_time_from_task = timedelta(hours=elapsed_time_from_task.hour, minutes=elapsed_time_from_task.minute, seconds=elapsed_time_from_task.second)
            timer["elapsed_time"] = elapsed_time_from_task
            timer["toggle_button"].config(text="Stop Timer")
            t.update_task_time(task_id, str(timer["elapsed_time"]).split('.')[0])
            
    def update_timer(self):
        """
        Updates the timer labels for each task.

        This method updates the timer labels for each task by calculating the current duration
        and adding it to the elapsed time. It then updates the label with the formatted duration.
        """
        for each, timer in self.task_timers.items():
            if timer["timer_running"]:
                current_duration = datetime.now() - timer["start_time"]
                total_duration = current_duration + timer["elapsed_time"]
                formatted_duration = str(total_duration).split('.')[0]
                timer["label"].config(text=formatted_duration)
        self.after(1000, self.update_timer)


    def submit_task(self):
        """
        Submits a new task.

        This method retrieves the task, description, and time from the entry fields,
        adds the task to the tasks module, clears the entry fields, and displays the updated tasks.
        If the task field is empty, it shows an error message.
        """
        task = self.task_entry.get()
        description = self.description_entry.get()

        if task:
            t.add_task(task, description)
            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.display_tasks()
        else:
            if not self.popup_label_active:

                if hasattr(self, "warning_label"):
                    popup_label = self.warning_label
                    popup_label.config(text="Please enter a task.", fg="red")

                    popup_label.pack(side="top")
                    self.popup_label_active = True
                    self.after(5000, lambda: self.remove_popup(popup_label))

    def remove_popup(self, label):
        """
        Removes the error message popup.

        This method removes the error message label from the main window.
        """
        label.config(text="")
        self.popup_label_active = False

def on_quit():
    """
    Function called when the application is closed.

    This function is called when the application is closed. It calls the toggle_timer method
    for each task to stop the timers before closing the application.
    """
    for task_id in app.task_timers:
        app.toggle_timer(task_id)
        print("timers saved")
    app.destroy()


app = App()
app.protocol("WM_DELETE_WINDOW", on_quit)
app.mainloop()
