'''
Application Library
author: Predrag Nikolic github/pdjan
date: nov 2019
version 0.1.6
python: 3.7.4
'''

# windows management function

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

        leftFrame = Frame(width=150, height=600)
        leftFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N)       

        self.addbtn = ttk.Button(leftFrame, text="New book", width=15, command=self.add_book_dialog)
        self.addbtn.grid(row=0, column=0, sticky=W+N)

        self.modbtn = ttk.Button(leftFrame, text="Edit book", width=15, command=self.edit_book_dialog)
        self.modbtn.grid(row=1, column=0, sticky=W+N)

        rightFrame = Frame(width=150, height=600)
        rightFrame.grid(row=0, column=1, padx=0, pady=5)                

        self.tree = ttk.Treeview(rightFrame, show="headings", height=20, column=4, selectmode="browse")
        self.tree.grid(row=0, column=1, rowspan=20, sticky=N)

        self.vsb = ttk.Scrollbar(rightFrame, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=0, column=2, sticky=N+S+E+W, rowspan=20)
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        self.tree["columns"]=("one","two","tree","four")
        self.tree.column("one", width=140)
        self.tree.column("two", width=240)
        self.tree.column("tree", width=100)
        self.tree.column("four", width=100)
        self.tree.heading("one", text='Author', anchor=N)
        self.tree.heading("two", text='Title', anchor=N)
        self.tree.heading("tree", text='Pages', anchor=N)
        self.tree.heading("four", text='Date', anchor=N)

        self.msg=Label(text='*', fg='red')
        self.msg.grid(row=21, column=1)

        self.context_open = False

        self.update_list()

    def add_book_dialog(self):
        '''
        Add new book dialog box
        '''
        try:
            self.msg["text"] = ""
            self.tl = Tk()
            self.tl.title("Add book")
            self.tl.resizable(False, False)
            
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
            upbtn = Button(self.tl, bg="grey", fg="white", text= 'Add new book', command=lambda:self.add_book(ne1,ne2,ne3,ne4))
            upbtn.grid(row=5, column=0, sticky=W, pady=10, padx=10)

            self.config()
            self.tl.protocol("WM_DELETE_WINDOW", self.config)
                                    
            self.tl.mainloop()

        except IndexError as e:
            self.msg["text"] = "Error while adding a book"


    def edit_book_dialog(self):
        pass
    
    def add_book(self,a,b,c,d):
        '''
        Function adds book to database
        '''
        a1 = a.get()
        b1 = b.get()
        c1 = c.get()
        d1 = d.get()

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO t(Author,Title,Pages,Date) VALUES (?,?,?,?)", (a1,b1,c1,d1))

        conn.commit()                  
        c.close()
        self.tl.destroy()

        self.msg["text"] = "Book added."
        
        self.update_list()

    def update_list(self):
        '''
        Updates book list from database into treeview 
        '''
        
        # delete current items
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

        # read new data
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        lst = c.execute("SELECT * FROM t ORDER BY Date(Date) desc")

        for row in lst:
            self.tree.insert("", END, text="", values=(row[0], row[1], row[2], row[3]))
        conn.commit()    
        c.close()

    def config(self):
        '''
        Windows management function
        '''
        if self.context_open:
            self.addbtn.config(state=NORMAL)
            self.modbtn.config(state=NORMAL)
            self.tree.config(selectmode="browse")
            self.tl.destroy()
            # restore root close button function
            root.protocol('WM_DELETE_WINDOW', root.destroy)
        else:
            # ignore root close button
            root.protocol('WM_DELETE_WINDOW', lambda:0)
            self.addbtn.config(state=DISABLED)
            self.modbtn.config(state=DISABLED)
            self.tree.config(selectmode="none")
        self.context_open = not self.context_open        

    
root = Tk()
root.title("Library")
application = Library(root)
root.mainloop()
