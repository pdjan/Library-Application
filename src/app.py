'''
Application Library
author: Predrag Nikolic github/pdjan
date: nov 2019
version 0.1.2
python: 3.7.4
'''

from tkinter import *
from tkinter import ttk
import sqlite3
import os.path
import csv

class Library:
    def __init__(self, master):

        # create empty database if it does not exist in the directory
        
        if not os.path.exists('data.db'):
            print('create database ...')
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE t (Author,Title,Pages,Date);")
            con.commit()
            con.close()
            if os.path.exists('data.db'):
                print('done.')
            else:
                print('error creating database.')

        # UI setup

        self.addbtn = ttk.Button(text="New book", width=15, command=self.add_book_dialog)
        self.addbtn.grid(row=0, column=0, sticky=W+N)

        self.modbtn = ttk.Button(text="Edit book", width=15, command=self.edit_book_dialog)
        self.modbtn.grid(row=1, column=0, sticky=W+N)

        self.tree = ttk.Treeview(show="headings", height=20, column=4, selectmode="browse")
        self.tree.grid(row=0, column=1, rowspan=20, sticky=N)
        self.tree["columns"]=("one","two","tree","four")
        self.tree.column("one", width=140)
        self.tree.column("two", width=240)
        self.tree.column("tree", width=100)
        self.tree.column("four", width=100)
        self.tree.heading("one", text='Author', anchor=N)
        self.tree.heading("two", text='Title', anchor=N)
        self.tree.heading("tree", text='Pages', anchor=N)
        self.tree.heading("four", text='Date', anchor=N)        

    def add_book_dialog(self):
        pass

    def edit_book_dialog(self):
        pass
    
root = Tk()
root.title("Library")
application = Library(root)
root.mainloop()
