'''
Application Library
author: Predrag Nikolic github/pdjan
date: nov 2019
version 0.1.3
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
        '''
        Add new book dialog box
        '''
        try:
            self.tl = Tk()
            # window position
            x=root.winfo_rootx()+150
            y=root.winfo_rooty()+50
            self.tl.geometry('+%d+%d' % (x,y))

            Label(self.tl,text='Author:').grid(row=0, column=0, sticky=W)
            ne1var = StringVar()
            ne1 = Entry(self.tl, textvariable=ne1var)
            ne1.grid(row=0, column=1, sticky=W)
            ne1.insert(0,"")

            Label(self.tl,text='Title:').grid(row=1, column=0, sticky=W)
            ne2var = StringVar()
            ne2 = Entry(self.tl, textvariable=ne2var)
            ne2.grid(row=1, column=1, sticky=W)
            ne2.insert(0,"")

            Label(self.tl,text='Pages:').grid(row=2, column=0, sticky=W)
            ne3var = StringVar()
            ne3 = Entry(self.tl, textvariable=ne3var)            
            ne3.grid(row=2, column=1, sticky=W)
            ne3.insert(0,"")

            Label(self.tl,text='Date:').grid(row=3, column=0, sticky=W)
            ne4var = StringVar()
            ne4 = Entry(self.tl, textvariable=ne4var)
            ne4.grid(row=3, column=1, sticky=W)
            ne4.insert(0,"")            

            # Button calls function for executing sql command      
            upbtn = Button(self.tl, text= 'Add new book', command=lambda:self.add_book(ne1,ne2,ne3,ne4))
            upbtn.grid(row=5, column=0, sticky=W)            
                                    
            self.tl.mainloop()

        except IndexError as e:
            pass


    def edit_book_dialog(self):
        pass
    
    def add_book(self,a,b,c,d):
        print("book added.")
        pass
    
root = Tk()
root.title("Library")
application = Library(root)
root.mainloop()
