# Author: Jacob Deaton
# GitHub username: jd-58
# Date:
# Description:


from tkinter import *

root = Tk()

# Creating a label widget
myLabel1 = Label(root, text="Hello world")
myLabel2 = Label(root, text="Test")

# Putting it on the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)

root.mainloop()
