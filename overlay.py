import tkinter as tk
from tkcalendar import Calendar, DateEntry

class TimetableApp:
    def __init__(self, master):
        self.master = master
        master.title("Timetable Application")

        # Calendar Widget
        self.cal = Calendar(master, selectmode='day', year=2025, month=9, day=1)
        self.cal.pack(pady=20)

        # Event Input
        self.event_label = tk.Label(master, text="Event Description:")
        self.event_label.pack()
        self.event_entry = tk.Entry(master, width=50)
        self.event_entry.pack()

        # Add Event Button
        self.add_button = tk.Button(master, text="Add Event", command=self.add_event)
        self.add_button.pack(pady=10)

        # Event List Display
        self.event_list_label = tk.Label(master, text="Events for Selected Date:")
        self.event_list_label.pack()
        self.event_list = tk.Listbox(master, height=10, width=50)
        self.event_list.pack()

        # Bind calendar selection to update event list
        self.cal.bind("<<CalendarSelected>>", self.update_event_list)

        self.events = {} # Dictionary to store events: {date_str: [event1, event2]}

    def add_event(self):
        selected_date = self.cal.get_date()
        event_description = self.event_entry.get()
        if event_description:
            if selected_date not in self.events:
                self.events[selected_date] = []
            self.events[selected_date].append(event_description)
            self.update_event_list(None) # Update the listbox
            self.event_entry.delete(0, tk.END) # Clear input field

    def update_event_list(self, event):
        self.event_list.delete(0, tk.END)
        selected_date = self.cal.get_date()
        if selected_date in self.events:
            for item in self.events[selected_date]:
                self.event_list.insert(tk.END, item)

root = tk.Tk()
app = TimetableApp(root)
root.mainloop()