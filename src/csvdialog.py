'''
Created on Feb 18, 2018

Contains 2 dialog class.
Alert dialog displays one line.
Input dialog prompts users
to enter information.

@author: Philip Deck
'''
from tkinter import Label, Entry, Frame, Button, LEFT, ACTIVE, END, Toplevel

class CSVInputDialog(Toplevel):
    """Helper class that handles inputs from the user"""
    def __init__(self, title, *inputs):
        super().__init__()

        self.inputs = inputs
        self.entries = list()
        self.results = list()
        
        self.grab_set()
        self.title(title)
        self.resizable(False, False)
        self.focus_force()

        self.contentframe = Frame(self)

        msg = Label(self.contentframe, text=title)
        msg.grid(row=0, column=0, columnspan=2)

        i = 0
        while i < len(inputs):
            lbl = Label(self.contentframe, text=inputs[i])
            lbl.grid(row=i + 1, column=0)
            entry = Entry(self.contentframe)
            entry.grid(row=i + 1, column=1, padx=5)
            self.entries.insert(i,entry)
            i += 1
        
        # Nice buttons at the bottom
        buttonframe = Frame(self)
        btn_ok = Button(buttonframe, text="Ok", width=10, command=self.get_string, default=ACTIVE)
        btn_ok.pack(side=LEFT, padx=5, pady=5)
        btn_cancel = Button(buttonframe, text="Cancel", width=10, command=self.end)
        btn_cancel.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.get_string)
        self.bind("<Escape>", self.end)
        
        self.contentframe.pack( padx=20, pady=5)
        buttonframe.pack()
        
    def add_input(self, line):
        rownum = len(self.entries) +1 
        lbl = Label(self.contentframe, text=line)
        lbl.grid(row=rownum, column=0)
        entry = Entry(self.contentframe)
        entry.grid(row=rownum, column=1, padx=5)
        self.entries.insert(rownum,entry)
        
    def default_values(self, values):
        """Used to set default values within the dialog window."""
        for entry, line in zip(self.entries, values):
            entry.insert(END, line)

    def get_string(self, event=None):
        """Compiles the results then terminates the app."""
        for entry in self.entries:
            self.results.append(entry.get())
            
        self.end()

    def get_inputs(self):
        """Returns the info gathered."""
        self.mainloop()
        return self.results
        
    def end(self, event=None):
        """Ends the dialog."""
        self.grab_release()
        self.quit()
        self.destroy()
        
class CSVAlertDialog(Toplevel):
    def __init__(self, title, info):
        super().__init__()
        
        self.grab_set()
        self.title(title)
        self.resizable(False, False)
        self.focus_force()

        self.contentframe = Frame(self)

        msg = Label(self.contentframe, text=info)
        msg.pack()
        
                # Nice buttons at the bottom
        buttonframe = Frame(self)
        btn_ok = Button(buttonframe, text="Ok", width=10, command=self.end, default=ACTIVE)
        btn_ok.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.end)
        
        self.contentframe.pack( padx=20, pady=5)
        buttonframe.pack()
        
        
    def show_alert(self):
        self.mainloop()
        
    def end(self, event=None):
        """Ends the dialog."""
        self.grab_release()
        self.quit()
        self.destroy()