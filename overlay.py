import tkinter as tk
from PIL import Image, ImageTk

def settings():
    print('open settings')

def settask(day, row):
    print(day, row)

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

for i in range(1, 25):
    root.rowconfigure(i, weight=1)
root.columnconfigure([1, 2, 3, 4, 5, 6, 7], weight=4)
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
        frame.rowconfigure(i, weight=1)
    frame.columnconfigure(0, weight=1)

for i in range(24):
    if i > 9:
        timefuni = tk.Label(text=f'{i}:00', master=root)
        timefuni.grid(row=i + 1, column=0)
    else:
        timefuni = tk.Label(text=f'0{i}:00', master=root)
        timefuni.grid(row=i + 1, column=0, sticky='news')

cogimg = Image.open("cog.png").resize((24, 24), Image.LANCZOS)
cogimg = ImageTk.PhotoImage(cogimg)

# Settings button with icon
settings_button = tk.Button(master=root, image=cogimg, command=settings, relief="flat")
settings_button.grid(row=0, column=0, sticky='nw')

for day in days:
    for i in range(24):
        if day =='monday':
            maths = tk.Button(text='Maths', bg='darkblue', fg='white', master=frames['monday'], command=lambda day=day, i=i: settask(day, i))
            maths.grid(row=i, sticky='news')
        else:
            empty = tk.Button(text='Click To Set', bg='lightgrey', fg='black', master=frames[day], command=lambda day=day, i=i: settask(day, i))
            empty.grid(row=i, sticky='news')


root.mainloop()