#!/usr/bin/env python3

import tkinter as tk
import os
import configparser
import sqlite3
import logging
from db import Database
from datetime import date
import time


class Badge(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartPage,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def start(self):
        self.tk.mainloop()

    def do_quit(self):
        self.quit()

class StartPage(tk.Frame):

    def onValidate(self, d, s, S):
        self.text.delete("1.0", "end")
        self.text.insert("end","OnValidate:\n")
        self.text.insert("end","d='%s'\n" % d)
        self.text.insert("end","s='%s'\n" % s)
        self.text.insert("end","S='%s'\n" % S)

        # Allow only digit and ":"
        if d == "0":
            return True
        if (S == ":" and len(s) != 2) or (not S.isdigit() and S != ":") or (len(s) == 3 and int(S) > 5) or len(s) > 4:
            self.bell()
            return False
        
        return True

        if S == ":" and len(s) != 2:
            print("S", S, "len s != 2", len(s), "d != 0" , d)
            self.bell()
            return False            
        if not S.isdigit() and S != ":":
            print("2")
            self.bell()
            return False
        if len(s) == 3 and int(S) > 5:
            print("3")
            self.bell()
            return False
        if len(s) > 4:
            print("4")
            self.bell()
            return False

    def hour_24(self, event):
        """
        Check and build the correct format hour: hh:mm
        it keep in mind the 1x and 2x hours and the max minutes can be 59
        """

        # get the object that triggered the event
        s = event.widget

        # if delete a char do not nothing or delete 
        if len(s.get()) == 2 and event.char=='\x7f':
            s.delete(len(s.get())-1, tk.END)
        if event.char=='\x7f':
            return
        
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 2:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) < 24:
            s.insert(2, ":")
        elif len(s.get()) == 2:
            self.bell()
            s.delete(1)
        
    def is_validhour(self, char):
        for ch in char:
            if char.isdigit or char == ":":
                yield True
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.label = tk.Label(self, text="Start Page",)
        self.label.pack(pady=10,padx=10)

        tk.Label(self, text='Enter a hour in 24 format:').pack()

        vcmd = (self.register(self.onValidate),
                '%d', '%s', '%S')
        self.entry = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry.pack(side="top")
        self.entry.bind("<KeyRelease>", self.hour_24)

        self.entry1 = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry1.pack(side="top")
        self.entry1.bind("<KeyRelease>", self.hour_24)

        self.text = tk.Text(self, height=10, width=40)
        self.text.pack(side="bottom", fill="both", expand=True)

        
    def message(self):
        self.label.config(text="bottone cliccato")

def main():
    app = Badge()
    app.title(string="Badge")
    app.geometry("500x400")
    app.start()    

if __name__ == '__main__':
    main()
else:
    print('I would like to be the main module.')
