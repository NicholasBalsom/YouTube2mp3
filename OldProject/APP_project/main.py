# pip install pytube
import youtube2mp3 as yt
from tkinter import *
import tkinter.messagebox
import os


# Testing link: https://youtu.be/gV1V8aZ5B2U 


# Button Functions
def download():
    if len(urlist) == 0 and linkbox.get() != "" and linkbox.get() != linkbox_placeholder:
        urlist.append(linkbox.get())
    elif len(urlist) == 0:
        return
    
    # If outdir_box is empty use default directroy
    if outdir_box.get() == "" or outdir_box.get() == outdir_placeholder:
        outdir = os.getcwd()
    else:
        outdir = outdir_box.get()

    message = get_message()
    message += " was successfuly downloaded!"

    try:
        yt.convert(urlist, outdir)
        tkinter.messagebox.showinfo("Success", message)
    except:
        print("Video could not be downloaded")
        tkinter.messagebox.showinfo("Failed", "Download Failed")


def add():
    url = linkbox.get()
    urlist.append(url)
    title = yt.get_title(url)
    listbox.insert(len(urlist)+1, title)


def get_message():
    message = ""
    for url in urlist:
        if url != urlist[-1]:
            message += yt.get_title(url) + ", "
        else:
            message += yt.get_title(url)
    return message


# def load_pb(event):
#     button_add.grid_forget()
#     button_download.grid_forget()
#     pb.grid(column=0, row=3, columnspan=2, sticky=N, padx=5, pady=5)
#     download()


# Entry box placeholders
def erase_linkbox(event=None):
    if linkbox.get() == linkbox_placeholder:
        linkbox.config(fg="black")
        linkbox.delete(0, 'end')


def erase_outdir(event=None):
    if outdir_box.get() == outdir_placeholder:
        outdir_box.config(fg="black")
        outdir_box.delete(0, 'end')


def add_linkbox(event=None):
    if linkbox.get() == '':
        linkbox.config(fg="grey")
        linkbox.insert(0, linkbox_placeholder)


def add_outdir(event=None):    
    if outdir_box.get() == '':
        outdir_box.config(fg="grey")
        outdir_box.insert(0, outdir_placeholder)
    

# setup
urlist = []
window = Tk()
window.title("yt2mp3")
window.minsize(320, 350)
window.maxsize(600, 400)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=0)
window.rowconfigure(2, weight=0)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)

# Title
title = StringVar()
title.set("YouTube to mp3") 
label_title = Label(window, textvariable=title )
label_title.grid(column=0, row=0, columnspan=2, sticky=N, padx=5, pady=5)

# pb = Progressbar(window, orient='horizontal', mode='indeterminate', length=200)

# Linkbox Labels
# label_link = Label(window, text="Link: ")
# label_outdir = Label(window, text="OutDir: ") 
# label_link.grid(row = 1, column = 0, sticky = "W", pady = 2)
# label_outdir.grid(row = 2, column = 0, sticky = "W", pady = 2)

# Textbox for link and outdir input
linkbox = Entry(window)
outdir_box = Entry(window)
linkbox.grid(column=0, row=1, columnspan=2, sticky=EW, padx=5, pady=5)
outdir_box.grid(column=0, row=2, columnspan=2, sticky=EW, padx=5, pady=5)
linkbox_placeholder = "Paste Youtube Link (ex. https://youtu.be/dQw4w9WgXcQ)"
outdir_placeholder = "Paste Download Directory (Leave empty for default)"
linkbox.bind('<FocusIn>',erase_linkbox)
linkbox.bind('<FocusOut>',add_linkbox)
outdir_box.bind('<FocusIn>',erase_outdir)
outdir_box.bind('<FocusOut>',add_outdir)
add_linkbox()
add_outdir()

# Buttons
button_download = Button(window, width=10, bg="red", fg="white", text="Download", command=download)
button_add = Button(window, width=10, bg="blue", fg="white", text="Add", command=add)
button_download.grid(column=0, row=3, sticky=E, padx=10, pady=5)
button_add.grid(column=1, row=3, sticky=W, padx=10, pady=5)
# button_download.bind('<Button-1>', load_pb)

listbox = Listbox(window)
listbox.grid(column=0, row=4, columnspan=2, sticky=NSEW, padx=10, pady=10)

window.mainloop()
