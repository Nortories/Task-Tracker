import tkinter as tk
import jsontasks as jsontasks
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from datetime import datetime, timedelta


class App(tb.Window):
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
            f"600x{getScreenHeight}+{self.winfo_screenwidth()-610}+0")

        self.first_time = True
        self.popup_label_active = False
        self.dark_mode = False
        self.task_frame_area_has_been_packed = False
        self.task_timers = {}  # Dictionary to store timer information for each task
        self.progressbars = {}  # Dictionary to store progress bar information for each task

        self.create_widgets()
        self.after(1000, self.update_display)

    def create_widgets(self):
        """
        Creates the widgets frame area for the main window.

        This method creates labels and entry fields for task, description, and time,
        as well as a submit button.
        """

        self.mainFrame = tb.Frame(self)
        self.mainFrame.pack(fill=tk.X, padx=5, pady=5)

        tb.Style("cosmo")  # Default theme

        dark_mode_button = tb.Button(
            self.mainFrame, text="Dark", width=5, command=self.toggle_dark_mode)
        dark_mode_button.pack(side="right")

        title_label = tb.Label(self.mainFrame, text="Task")
        title_label.pack(side="left")
        self.task_entry = tb.Entry(self.mainFrame)
        self.task_entry.pack(side="left")

        description_label = tb.Label(self.mainFrame, text="Description")
        description_label.pack(side="left")
        self.description_entry = tb.Entry(self.mainFrame)
        self.description_entry.pack(side="left")

        time_goal_label = tb.Label(self.mainFrame, text="Time for task")
        time_goal_label.pack(side="left")
        self.time_goal_entry = tb.Entry(self.mainFrame)
        self.time_goal_entry.pack(side="left")

        button_frame = tb.Frame(self)
        button_frame.pack(pady=5)
        self.submit_button = tb.Button(
            button_frame, text="Add task", command=self.submit_new_task)
        self.submit_button.pack(side="top")

        self.warning_label = tb.Label(button_frame)
        self.warning_label.pack(side="left")

        self.left_frame = tb.Frame(self)
        self.left_frame.pack(side="left")

        self.scrolled_frame = ScrolledFrame(self)

    def toggle_dark_mode(self):
        """
        Toggles the dark mode.

        This method toggles the dark mode for the application.
        """

        if self.dark_mode == False:
            tb.Style("darkly")
            self.dark_mode = True
        else:
            tb.Style("cosmo")
            self.dark_mode = False

    def create_task_widget(self, task):
        """
        Creates a task widget.

        This method creates a widget for a given task, including labels, checkboxes, and buttons.
        """
        task_frame = tb.Frame(self.task_frame_area,
                              borderwidth=2, relief="groove")
        task_frame.pack(padx=(5, 15), pady=5, fill="x")

        task_label = tb.Label(task_frame, text=task["title"])
        task_label.pack(side="top")

        task_description = tb.Label(
            task_frame, text="Description:   " + task["description"])
        task_description.pack(side="top")

        goal_label = tb.Label(
            task_frame, text="Goal:   " + task["time_goal"])
        goal_label.pack(side="top")

        task_id = task["taskID"]
        self.task_timers[task_id] = {"label": tb.Label(task_frame, text=task["timer"]),
                                     "start_time": None,
                                     "elapsed_time": timedelta(),
                                     "timer_running": False}
        self.task_timers[task_id]["label"].pack()

        # Create a progress bar for the task
        self.create_progressbar(task_frame, task)

        # Create a button to start or stop the timer
        toggle_timer_button = tb.Button(
            task_frame, text="Start Timer",
            # Very interesting way to pass arguments to a function within a lambda function.
            command=lambda id=task_id: self.toggle_timer(id))
        toggle_timer_button.pack(side="left", padx=(5, 0), pady=(0, 5))

        # Create a button to remove the task from task area (task data is not removed from json file)
        remove_task_button = tb.Button(
            task_frame, text="Remove", command=lambda id=task_id: self.remove_task(id))
        remove_task_button.pack(side="left", padx=(5, 0), pady=(0, 5))

        # Store the button reference
        self.task_timers[task_id]["toggle_timer_button"] = toggle_timer_button

        # Create a checkbox for each task
        checkbox = tk.Checkbutton(
            task_frame, text="Completed", onvalue=True, offvalue=False, command=lambda: jsontasks.update_task_completed(task_id))
        if task["completed"]:
            checkbox.select()
        else:
            checkbox.deselect()
        checkbox.pack(side="right")

    def remove_task(self, task_id):
        """
        Removes a task.

        This method removes a task from the tasks module and updates the display.
        """
        jsontasks.remove_task(task_id)
        self.task_timers.pop(task_id)
        self.update_display()
        

    def create_progressbar(self, task_frame, task):
        """
        Creates a progress bar for a given task.

        This method creates a progress bar based on the task's time goal and elapsed time.
        """
        task_id = task["taskID"]
        self.progressbars[task_id] = tb.Progressbar(
            task_frame,
            bootstyle="warning-striped",
            mode="determinate",
            value=101
        )
        self.progressbars[task_id].pack(fill="x", padx=5, pady=5)

        time_goal = datetime.strptime(task["time_goal"], "%H:%M:%S")
        time_elapsed = datetime.strptime(task["timer"], "%H:%M:%S")

        time_goal_deltaed = (((timedelta(hours=time_elapsed.hour, minutes=time_elapsed.minute,
                             seconds=time_elapsed.second).total_seconds()) * 100))
        time_elapsed_deltaed = (((timedelta(
            hours=time_goal.hour, minutes=time_goal.minute, seconds=time_goal.second).total_seconds()) * 100))

        print(f"goal:{time_goal_deltaed}")
        print(f"elapsed:{time_elapsed_deltaed}")

        if time_elapsed_deltaed != 0:
            if time_goal_deltaed >= time_elapsed_deltaed:
                self.progressbars[task_id]["value"] = 100
            else:
                self.progressbars[task_id]["value"] = (
                    time_goal_deltaed / time_elapsed_deltaed) * 100
        elif time_goal_deltaed > 0:
            self.progressbars[task_id]["value"] = 100
        else:
            self.progressbars[task_id]["value"] = 0

    def update_display(self):
        """
        Updates the display of tasks.

        This method retrieves the tasks from the tasks module and updates the display
        by creating task widgets for each task.
        """
        # Save the timers for each task before destroying the old frame and adding in the tasks
        for task_id in self.task_timers:
            self.toggle_timer(task_id)
            print("timers saved")

        # Check if scrolled frame exists and destroy it if it does
        if hasattr(self, "task_frame_area"):
            self.task_frame_area.pack_forget()
            self.task_frame_area.destroy()

        # Create a frame to hold the tasks labels and pack it
        self.task_frame_area = ScrolledFrame(self)
        self.task_frame_area.pack(fill="both", expand=True)

        # Create and pack new tasks inside the task_frame_area with checkboxes inside there frame
        for task in jsontasks.read_tasks():
            if task["show"] == False:
                
                continue
            else:
                self.create_task_widget(task)

        self.update_timer()

        # Scroll to the bottom of the scroll area
        if self.first_time:
            self.first_time = False
        else:
            self.update_idletasks()
            self.task_frame_area.yview_moveto(1.0)

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
            timer["toggle_timer_button"].config(text="Start Timer")

            jsontasks.update_task_time(task_id, str(
                timer["elapsed_time"]).split('.')[0])
        else:
            timer["timer_running"] = True
            timer["start_time"] = datetime.now()
            # Ensure this is a timedelta object
            elapsed_time_from_task = jsontasks.get_task_timer(task_id)
            if isinstance(elapsed_time_from_task, datetime):
                elapsed_time_from_task = timedelta(
                    hours=elapsed_time_from_task.hour, minutes=elapsed_time_from_task.minute, seconds=elapsed_time_from_task.second)
            timer["elapsed_time"] = elapsed_time_from_task
            timer["toggle_timer_button"].config(text="Stop Timer")
            jsontasks.update_task_time(task_id, str(
                timer["elapsed_time"]).split('.')[0])

    def update_timer(self):
        """
        Updates the timer labels for each task.

        This method updates the timer labels for each task by calculating the current duration
        and adding it to the elapsed time. It then updates the label with the formatted duration.
        """
        tasks = jsontasks.read_tasks()

        for i, timer in self.task_timers.items():
            if timer["timer_running"]:
                current_duration = datetime.now() - timer["start_time"]
                total_duration = current_duration + timer["elapsed_time"]
                formatted_duration = str(total_duration).split('.')[0]
                timer["label"].config(text=formatted_duration)
                time_goal = datetime.strptime(
                    tasks[i-1]["time_goal"], "%H:%M:%S")
                time_goal_deltaed = ((timedelta(
                    hours=time_goal.hour, minutes=time_goal.minute, seconds=time_goal.second).total_seconds()))
                total_duration_deltaed = total_duration.total_seconds()

                if time_goal_deltaed <= total_duration_deltaed:
                    self.progressbars[i]["value"] = 100
                    self.progressbars[i].config(bootstyle ="success-striped")
                else:
                    self.progressbars[i]["value"] = (
                        total_duration_deltaed / time_goal_deltaed)*100
                # print(f"time_goal: {time_goal}")
                # print(f"goal:{time_goal_deltaed}")
                # print(f"duration: {total_duration_deltaed}")

        self.after(1000, self.update_timer)

    def submit_new_task(self):
        """
        Submits a new task.

        This method retrieves the task, description, and time from the entry fields,
        adds the task to the tasks module, clears the entry fields, and displays the updated tasks.
        If the task field is empty, it shows an error message.
        """
        task = self.task_entry.get()
        description = self.description_entry.get()
        time_goal = self.time_goal_entry.get()

        if task:
            jsontasks.add_task(task, description, time_goal)
            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.time_goal_entry.delete(0, tk.END)
            self.update_display()
        else:
            if not self.popup_label_active:

                if hasattr(self, "warning_label"):
                    popup_label = self.warning_label
                    popup_label.config(
                        text="Please enter a task.", foreground="red")

                    popup_label.pack(side="left")
                    self.popup_label_active = True
                    self.after(5000, lambda: (popup_label.config(
                        text=""), setattr(self, "popup_label_active", False)))


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
