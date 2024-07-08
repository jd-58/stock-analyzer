# Author: Jacob Deaton
# GitHub username: jd-58
# Date:
# Description:


from tkinter import *

root = Tk()

e = Entry(root, width=20, borderwidth=5)
e.pack()
e.insert(0, "Enter your name: ")



# Function for the button to do something
def click():
    hello = "Hello " + e.get()
    myLabel = Label(root, text=hello)
    myLabel.pack()


# Creating a label widget
# myLabel1 = Label(root, text="Hello world")
# myLabel2 = Label(root, text="Test")

# Creating a button
myButton = Button(root, text="Enter Your Name", command=click)

# Putting it on the screen
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=0)
myButton.pack()

root.mainloop()
