'''
Application Library
author: Predrag Nikolic github/pdjan
date: nov 2019
version 0.1.1
python: 3.7.4
'''

from tkinter import *
from tkinter import ttk
import sqlite3
import os.path
import csv

class Library:
    def __init__(self, master):

        # Create empty database if it does not exist in the directory
        
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

    def add_book_dialog(self):
        pass
    
root = Tk()
root.title("Library")
application = Library(root)
root.mainloop()
