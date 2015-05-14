from tkinter import*
import base64
import urllib
import sys



#buttons opens a gif image  on toplevel canvas


root = Tk()

var = StringVar()
def fit():
   novi = Toplevel()
   canvas = Canvas(novi, width = 700, height = 400)
   canvas.pack(expand = YES, fill = BOTH)
   gif1 = PhotoImage(file ='C:/Users/lance/Desktop/pic/drama.gif')
   canvas.create_image(50, 10, image = gif1, anchor = NW)
    #assigned the gif1 to the canvas object
   canvas.gif1 = gif1
   

def callback():
   novi = Toplevel()
   canvas = Canvas(novi, width = 700, height = 600)
   canvas.pack(expand = YES, fill = BOTH)
   gif1 = PhotoImage(file ='C:/Users/lance/Desktop/pic/dog.gif')
   canvas.create_image(50, 10, image = gif1, anchor = NW)
    #assigned the gif1 to the canvas object
   canvas.gif1 = gif1

def answer():
   novi = Toplevel()
   canvas = Canvas(novi, width =300, height = 300)
   canvas.pack(expand = YES, fill = BOTH)
   gif1 = PhotoImage(file ='C:/Users/lance/Desktop/pic/FUCKIT.gif')
   canvas.create_image(50, 10, image = gif1, anchor = NW)
    #assigned the gif1 to the canvas object
   canvas.gif1 = gif1


w = Label(root, text="How are you today?")
w.pack()


Button(text='Great', command=callback).pack(fill=X)
Button(text='No so Great', command=answer).pack(fill=X)
Button(text='Im going to explode',command=fit).pack(fill=X)

mainloop()
