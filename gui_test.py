# Author: Jacob Deaton
# GitHub username: jd-58
# Date:
# Description:


from tkinter import *

root = Tk()


# Function for the button to do something
def click():
    number = 5
    print(number + 5)


# Creating a label widget
# myLabel1 = Label(root, text="Hello world")
# myLabel2 = Label(root, text="Test")

# Creating a button
myButton = Button(root, text="Click Me!", command=click)

# Putting it on the screen
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=0)
myButton.pack()

root.mainloop()
