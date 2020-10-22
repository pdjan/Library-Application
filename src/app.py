'''
Application Library
author: Predrag Nikolic github/pdjan
date: June 2020
version 1.1
python: 3.7.4
'''
# theme applied

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
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
            # Setting Theme
            style = ThemedStyle(self.tl)
            style.set_theme("plastik")
            
            self.tl.title("Add book")
            self.tl.resizable(False, False)
            
            # window position
            x=root.winfo_rootx()+150
            y=root.winfo_rooty()+50
            self.tl.geometry('+%d+%d' % (x,y))

            Label(self.tl,text='Author').grid(row=0, column=0, sticky=W+E)
            ne1var = StringVar()
            ne1 = ttk.Entry(self.tl, textvariable=ne1var)
            ne1.grid(row=0, column=1, sticky=W)
            ne1.insert(0,"")

            Label(self.tl,text='Title').grid(row=1, column=0, sticky=W+E)
            ne2var = StringVar()
            ne2 = ttk.Entry(self.tl, textvariable=ne2var)
            ne2.grid(row=1, column=1, sticky=W)
            ne2.insert(0,"")

            Label(self.tl,text='Pages').grid(row=2, column=0, sticky=W+E)
            ne3var = StringVar()
            ne3 = ttk.Entry(self.tl, textvariable=ne3var)            
            ne3.grid(row=2, column=1, sticky=W)
            ne3.insert(0,"")

            Label(self.tl,text='Date').grid(row=3, column=0, sticky=W+E)
            ne4var = StringVar()
            ne4 = ttk.Entry(self.tl, textvariable=ne4var)
            ne4.grid(row=3, column=1, sticky=W)
            ne4.insert(0,"")            

            # Button calls function for executing sql command      
            # upbtn = Button(self.tl, bg="grey", fg="white", text= 'Add new book', command=lambda:self.add_book(ne1,ne2,ne3,ne4))
            upbtn = ttk.Button(self.tl, text= 'Add new book', command=lambda:self.add_book(ne1,ne2,ne3,ne4))
            upbtn.grid(row=5, column=0, sticky=W, pady=10, padx=10)

            self.config()
            self.tl.protocol("WM_DELETE_WINDOW", self.config)
                                    
            self.tl.mainloop()

        except IndexError as e:
            self.msg["text"] = "Error while adding a book"


    def edit_book_dialog(self):
        try:
            self.msg["text"] = " "
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            name = self.tree.item(self.tree.selection()[0])['values'][1]
            
            query = "SELECT * FROM t WHERE Title = '%s';" %name
            db_data = c.execute(query)

            for item in db_data:
                _author = item[0]
                _title = item[1]
                _pages = item[2]
                _date = item[3]
                
            self.tl = Tk()
            self.tl.title("Edit details")
            
            # Setting Theme
            style = ThemedStyle(self.tl)
            style.set_theme("plastik")
            
            x = root.winfo_rootx()+120
            y = root.winfo_rooty()+50
            self.tl.geometry('%dx%d+%d+%d' % (380, 155, x, y))
            self.tl.resizable(False, False)

            Label(self.tl,text='Author ').grid(row=0, column=0, sticky=E+W)
            new_author = ttk.Entry(self.tl, width=30)
            new_author.grid(row=0, column=1, sticky=W, padx=10)
            new_author.insert(0,_author)

            Label(self.tl, text='Title ').grid(row=1, column=0,sticky=E+W)
            new_title = ttk.Entry(self.tl, width=30)
            new_title.grid(row=1, column=1, sticky=W, padx=10)
            new_title.insert(0,_title)

            Label(self.tl, text='Pages').grid(row=2, column=0,sticky=E+W)
            new_pages = ttk.Entry(self.tl, width=30)
            new_pages.grid(row=2, column=1, sticky=W, padx=10)
            new_pages.insert(0,_pages)

            Label(self.tl, text='Date').grid(row=3, column=0,sticky=E+W)
            new_date = ttk.Entry(self.tl, width=30)
            new_date.grid(row=3, column=1, sticky=W, padx=10)
            new_date.insert(0,_date)
                                        
            #upbtn = Button(self.tl, bg="grey", fg="white", text='Enter details',
            #               command=lambda:self.enter_changes(new_author,new_title,new_pages,new_date,name))
            upbtn = ttk.Button(self.tl, text='Enter details', command=lambda:self.enter_changes(new_author,new_title,new_pages,new_date,name))
            upbtn.grid(row=4, column=0, sticky=W, padx=10, pady=10)

            # dbtn = Button(self.tl, bg="grey", fg="white", text="Delete book", command=lambda:self.delete_book(name))
            dbtn = ttk.Button(self.tl, text="Delete book", command=lambda:self.delete_book(name))
            dbtn.grid(row=4, column=1, sticky=W, padx=10, pady=10)

            conn.commit()
            c.close()
            
            self.config()
            self.tl.protocol("WM_DELETE_WINDOW", self.config)

            self.tl.mainloop()
            
        except IndexError as e:
            self.msg["text"] = "Select book to edit"
            
    
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

        self.msg["text"] = "Book added."
        
        self.config()
        self.update_list()
        
    def enter_changes(self,new_author,new_title,new_pages,new_date,name):
        '''
        Enter changes to database function
        '''
        inAuthor = new_author.get()
        inTitle = new_title.get()
        inPages = new_pages.get()
        inDate = new_date.get()
        inName = name

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('UPDATE t SET Author=(?), Title=(?), Pages=(?), Date=(?) WHERE Title=(?) AND Author=(?)',
                  (inAuthor,inTitle,inPages,inDate,inName,inAuthor))
        conn.commit()
        c.close()
        self.msg['text'] = "Data for '%s' is changed" %name
        self.config()
        self.update_list()

    def delete_book(self, name):
        '''
        Deletes chosen book from database and list
        '''
        dName = name
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        sql_query = """DELETE from t WHERE Title=(?)"""
        # note: if there are 2 books with same title, both will be deleted
        # solution is to check by title and another parameter
        c.execute(sql_query, (dName,))
        conn.commit()
        c.close()
        self.msg["text"] = "Book is deleted"
        self.config()
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

# Setting Theme
style = ThemedStyle(root)
style.set_theme("plastik")

root.title("Library")
application = Library(root)
root.mainloop()
