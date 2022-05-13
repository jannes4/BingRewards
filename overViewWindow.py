from tkinter import *
from tkinter.font import Font
import keyboard

def create_overview_window(username, amount_points, value_in_microsoft_products, real_value):
    primary = '#1E1E1E'
    secondary = '#6e7bd9'

    def headline(text):
        font = Font(family='roboto', size=20, weight='normal')
        label = Label(app, text=text, fg=secondary, bg=primary, font=font, pady=10, padx=0)
        label.pack()

    def paragraph(text):
        font = Font(family='roboto', size=40, weight='bold')
        label = Label(app, text=text, fg='white', bg=primary, font=font)
        label.pack()

    app = Tk()  # the application itself
    app.title("Übersicht (Dieses Fenster ist vertrauenswürdig)")  # title of window
    app.configure(background=primary)
    app.overrideredirect(1)
    app.attributes('-topmost', True)

    w = 500 # width for the Tk root
    h = 430 # height for the Tk root

    # get screen width and height
    ws = app.winfo_screenwidth() # width of the screen
    hs = app.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws) - (w)
    y = 0

    # set the dimensions of the screen 
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))

    label = Label(app, text= f"Stats von {username}", bg=secondary, fg='white', width=500, height=2)  # creates label
    label.pack()  # adds the label to the window

    dailySearchPoints = 150

    headline('Bing Punkte')
    paragraph(amount_points)
    headline('Microsoft Wert')
    paragraph(f"{value_in_microsoft_products} €")
    headline('Wert')
    paragraph(f"{real_value} €")

    keyboard.add_hotkey('ctrl+q', app.destroy)

    app.mainloop()  # this must go at the end of your window code