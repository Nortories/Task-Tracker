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

        self.create_widgets()
        self.update_display()

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

        time_for_task_label = tb.Label(self.mainFrame, text="Time for task")
        time_for_task_label.pack(side="left")
        self.time_for_task_entry = tb.Entry(self.mainFrame)
        self.time_for_task_entry.pack(side="left")

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
        task_frame.pack(padx=5, pady=5, fill="x")

        task_label = tb.Label(task_frame, text=task["title"])
        task_label.pack(side="top")

        task_description = tb.Label(
            task_frame, text="Description:   " + task["description"])
        task_description.pack(side="top")

        task_id = task["taskID"]
        self.task_timers[task_id] = {"label": tb.Label(task_frame, text=task["timer"]),
                                     "start_time": None,
                                     "elapsed_time": timedelta(),
                                     "timer_running": False}
        self.task_timers[task_id]["label"].pack()

        # success colored solid progressbar style
        progressbar = tb.Progressbar(task_frame, bootstyle="success-striped")
        progressbar.pack(fill="x", padx=5, pady=5)
        progressbar.start()
        # progressbar.stop()

        toggle_button = tb.Button(
            task_frame, text="Start Timer",
            command=lambda id=task_id: self.toggle_timer(id)
        )
        toggle_button.pack(side="left", padx=(5, 0), pady=(0, 5))

        # Store the button reference
        self.task_timers[task_id]["toggle_button"] = toggle_button

        # Create a checkbox for each task
        if task["completed"]:
            checkmark = tk.BooleanVar(value=True)
            print("task completed")
        else:
            checkmark = tk.BooleanVar(value=False)
            print("task not completed")
        checkbox = tk.Checkbutton(
            task_frame, text="Completed", variable=checkmark)
        checkbox.pack(side="right")

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

        # Create a frame to hold the task labels and pack it
        self.task_frame_area = ScrolledFrame(self)
        self.task_frame_area.pack(fill="both", expand=True)

        # Create and pack new tasks inside the task_frame_area with checkboxes inside there frame
        for task in jsontasks.read_tasks():
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
            timer["toggle_button"].config(text="Start Timer")

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
            timer["toggle_button"].config(text="Stop Timer")
            jsontasks.update_task_time(task_id, str(
                timer["elapsed_time"]).split('.')[0])

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

    def submit_new_task(self):
        """
        Submits a new task.

        This method retrieves the task, description, and time from the entry fields,
        adds the task to the tasks module, clears the entry fields, and displays the updated tasks.
        If the task field is empty, it shows an error message.
        """
        task = self.task_entry.get()
        description = self.description_entry.get()

        if task:
            jsontasks.add_task(task, description)
            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
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

    # def remove_popup(self, label):
    #     """
    #     Removes the error message popup.

    #     This method removes the error message label from the main window.
    #     """
    #     label.config(text="")
    #     self.popup_label_active = False


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
