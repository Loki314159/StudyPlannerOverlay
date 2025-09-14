import tkinter as tk
from PIL import Image, ImageTk
from tkinter import colorchooser
from datetime import datetime, timedelta
from pynput import keyboard
import threading
import numpy as np

def opensettings():
    def savetimetable():
        shape = (7, 24)
        savearray = np.zeros(shape, dtype=object)
        for dindex, day in enumerate(taskmatrix):
            for tindex, task in enumerate(day):
                savearray[dindex][tindex] = (task.cget('fg'), task.cget('bg'), task.cget('text'))
        np.save('timetable.npy', savearray)
    def loadtimetable():
        savedarray = np.load('timetable.npy', allow_pickle=True)
        for dindex, day in enumerate(savedarray):
            for tindex, task in enumerate(day):
                updatetask(days[dindex], tindex, task[0], task[1], task[2])
        
    settings = tk.Toplevel()
    settings.title('Settings')
    savebutton = tk.Button(settings, text='Save', command=savetimetable, bg='darkgrey', fg='white') 
    savebutton.pack(expand=True)
    loadbutton = tk.Button(settings, text='Load', command=loadtimetable, bg='darkgrey', fg='white') 
    loadbutton.pack(expand=True)
    settings.mainloop()


def openoverlay():
    overlay = tk.Toplevel()
    overlay.title('Overlay')
    overlay.attributes('-topmost', True)
    global wordcount, currentword
    wordcount = 0
    currentword = ''
    
    def updatewords():
        wordcounter.config(text=f"Total Words: {wordcount}")
    def updatetimer(minutes, seconds):
        tthvar.set(f'Time to next task: {minutes}m {seconds}s')
    def startlistener():
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()
    def on_press(key):
        global wordcount, currentword
        try:
            if key.char.isalnum():
                currentword += key.char
            elif key.char == ' ':
                if currentword:
                    wordcount += 1
                    currentword = ''
                    updatewords()
        except AttributeError:
            if key == keyboard.Key.space or key == keyboard.Key.enter:
                if currentword:
                    wordcount += 1
                    currentword = ''
                    updatewords()
            elif key == keyboard.Key.esc:
                return False
    def currenttaskcoords():
        now = datetime.now()
        dindex = now.weekday()
        hour = now.strftime('%H')
        return dindex, hour
    
    def tthour():
        now = datetime.now()
        next_hour_start = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        time_difference = next_hour_start - now
        total_seconds = int(time_difference.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        updatetimer(minutes, seconds)
        overlay.after(1000, tthour)
    tthvar = tk.StringVar(overlay, 'Time to next task:')
    timetohour = tk.Entry(overlay, state='readonly', textvariable=tthvar)
    tthour()
    timetohour.pack(expand=True)
    threading.Thread(target=startlistener, daemon=True).start()
    wordcounter = tk.Label(overlay, text=f'Word Count: 0')
    wordcounter.pack(expand=True)
    overlay.mainloop()

def setcolour(var, button, option):
    hex = colorchooser.askcolor()[1]
    if hex:
        var.set(hex)
        if option == 'bg':
            button.config(bg = hex)
        elif option == 'fg':
            button.config(fg = hex)

def updatetask(day, row, fg, bg, text):
    task = taskmatrix[days.index(day)][row]
    task.configure(fg = fg, bg = bg, text = text)

def copytoggle():
    global copied
    global copymode
    global copybutton
    if copymode:
        copymode = False
        copied = ''
        copybutton.configure(background='lightgrey', fg='black')
    else:
        copymode = True
        copybutton.configure(background='green', fg='black')


def settask(day, hour, fg, bg, text):
    global copied
    global copymode    
    if copymode:
        if copied:
            updatetask(day, int(hour), copied['fg'], copied['bg'], copied['text'])
            pass
        else:
            copy = taskmatrix[days.index(day)][int(hour)]
            copied = {
                'text': copy.cget('text'),
                'fg': copy.cget('fg'),
                'bg': copy.cget('bg')
            }
    else:
        taskmenu(day, hour, fg, bg, text)

def taskmenu(day, hour, fg, bg, text):
    taskmenu = tk.Toplevel()
    taskmenu.title('Set Task')
    taskmenu.geometry('400x300')

    dayvar = tk.StringVar(value=str(day))
    daycoord = tk.Entry(taskmenu, state='readonly', textvariable=dayvar)

    hourvar = tk.StringVar(value=f'From: {hour} to {hour+1}')
    hourcoord = tk.Entry(taskmenu, state='readonly', textvariable=hourvar)

    fglabel = tk.Label(taskmenu, text='Text Colour:')
    fgvar = tk.StringVar(taskmenu, fg)
    fgentry = tk.Entry(taskmenu, state='readonly', textvariable=fgvar)
    fgbutton = tk.Button(taskmenu, text='Set new text colour', command=lambda: setcolour(fgvar, visbutton, 'fg'))

    bglabel = tk.Label(taskmenu, text='Background Colour:')
    bgvar = tk.StringVar(taskmenu, bg)
    bgentry = tk.Entry(taskmenu, state='readonly', textvariable=bgvar)
    bgbutton = tk.Button(taskmenu, text='Set new background colour', command=lambda: setcolour(bgvar, visbutton, 'bg'))

    tasklabel = tk.Label(taskmenu, text='Task:')
    taskvar = tk.StringVar(taskmenu, text)
    taskentry = tk.Entry(taskmenu, textvariable=taskvar)

    vislabel = tk.Label(taskmenu, text='Task Visualisation:')
    visbutton = tk.Button(taskmenu, textvariable=taskvar, fg=fgvar.get(), bg=bgvar.get())
    applybutton = tk.Button(taskmenu,
                            text='Apply',
                            command=lambda: updatetask(
                                dayvar.get(),
                                int(hour),
                                fgvar.get(),
                                bgvar.get(),
                                taskvar.get()))

    daycoord.grid(row=0, column=0)
    hourcoord.grid(row=0, column=1)
    fglabel.grid(row=1, column=0, sticky='e')
    fgentry.grid(row=1, column=1)
    fgbutton.grid(row=1, column=2)
    bglabel.grid(row=2, column=0, sticky='e')
    bgentry.grid(row=2, column=1)
    bgbutton.grid(row=2, column=2)
    tasklabel.grid(row=3, column=0)
    taskentry.grid(row=3, column=1)
    vislabel.grid(row=4, column=0)
    visbutton.grid(row=4, column=1, sticky='news')
    applybutton.grid(row=4, column=2)
    print(day, hour, fg, bg, text)
    taskmenu.mainloop()

global copied, copymode
copied = ''
copymode = False

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
root.columnconfigure([0], weight=2)
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
    daylabel = tk.Label(root, text=day.capitalize())
    daylabel.grid(column=index + 1, row=0)
    for i in range(24):
        frame.rowconfigure(i, weight=1)
    frame.columnconfigure(0, weight=1)

for i in range(24):
    if i > 9:
        timefuni = tk.Label(root, text=f'{i}:00')
        timefuni.grid(row=i + 1, column=0)
    else:
        timefuni = tk.Label(root, text=f'0{i}:00')
        timefuni.grid(row=i + 1, column=0, sticky='news')

taskmatrix = []

for dindex, day in enumerate(days):
    taskmatrix.append([])
    for hour in range(24):
        blank = tk.Button(text='Blank',
                        bg='lightgrey',
                        fg='black',
                        master=frames[day],)
        blank.config(command=lambda b=blank, d=day, h=hour: settask(d, h, b.cget('fg'), b.cget('bg'), b.cget('text')))
        blank.grid(row=hour, sticky='news')
        taskmatrix[dindex].append(blank)

menuframe = tk.Frame(root)

cogimg = Image.open("cog.png").resize((24, 24), Image.LANCZOS)
cogimg = ImageTk.PhotoImage(cogimg)
settings_button = tk.Button(menuframe, image=cogimg, command=opensettings, relief="flat")
settings_button.grid(row=0, column=0, sticky='news')

copybutton = tk.Button(menuframe, text='Cpy', command=copytoggle, bg='lightgrey') 
copybutton.grid(row=0, column=1, sticky='news')

ovlybutton = tk.Button(menuframe, text='Ovly', command=openoverlay, bg='grey') 
ovlybutton.grid(row=0, column=2, sticky='news')

menuframe.grid(row=0, column=0)
root.mainloop()