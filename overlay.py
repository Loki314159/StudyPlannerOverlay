import tkinter as tk

class event:
    pass

days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

root = tk.Tk()
root.title('Week View')

for i in range(24):
    root.rowconfigure(i, weight=1)
root.columnconfigure([1, 2, 3, 4, 5, 6, 7], weight=3)
root.columnconfigure([0], weight=1)
frames = {}

for index, day in enumerate(days):
    frame = tk.Frame(root,
                          relief="raised",
                          borderwidth=2,
                          highlightcolor='lightblue'
                          )
    frame.grid(row=1,
               column=index + 1,
               padx=2, pady=2,
               sticky='news',
               rowspan=24)
    frames[day] = frame
    daylabel = tk.Label(text=day.capitalize(), master=root)
    daylabel.grid(column=index + 1, row=0)

for i in range(24):
    if i > 9:
        timefuni = tk.Label(text=f'{i}:00', master=root)
        timefuni.grid(row=i + 1, column=0)
    else:
        timefuni = tk.Label(text=f'0{i}:00', master=root)
        timefuni.grid(row=i + 1, column=0)

root.mainloop()