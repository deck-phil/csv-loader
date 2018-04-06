'''
Created on Feb 26, 2018

GUI portion of the application.
Holds a variable of type CSVLoader
and uses it to perform functions.

@author: Philip Deck
'''

from tkinter import Tk, Toplevel, Label, Listbox, Entry, Menu, END, BOTTOM, BOTH, NORMAL, DISABLED

import time
import threading
import csvloader
import csvdialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
import queue


class Window(Tk):
    '''
    The graphical interface for the CSV Loader.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()  # Call the parent's constructor.
        
        self.startime = time.time()  # Record the start time. (Used for uptime)
        
        self.app = csvloader.CSVLoader()  # Start a session of the csvloader.
        self.build()  # Build the scene.

    def build(self):
        """Builds the main scene for the window."""
        self.title("CSV Loader - Philip Deck")
        
        self.build_menu()  # Build the menu bar.
        
        self.listbox = Listbox(self, width=120, height=20)  # The container for the data.
        self.listbox.pack(padx=5, pady=5, fill=BOTH, expand=1)  # Place it in the middle.
        
        self.infobox = Entry(self)  # Displays useful information to the user.
        self.infobox.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH)  # Place it underneath the listbox.
        
        self.set_infobox_msg("CSV Loader - Philip Deck")
        
    def set_infobox_msg(self, info):
        """Set the text in the bottom right corner entry box."""
        self.infobox.configure(state=NORMAL)
        self.infobox.delete(0, END)
        self.infobox.insert(END, info)
        self.infobox.configure(state=DISABLED)

    def build_menu(self):
        """Builds the menu bar."""
        menubar = Menu(self)
        
        # File Menu with Commands
        filemenu = Menu(menubar, tearoff=0)
        
        filemenu.add_command(label="New List", command=self.new_list)
        filemenu.add_command(label="Import MySQL Database", command=self.import_db)
        filemenu.add_command(label="Import CSV File", command=self.import_csv)
        
        filemenu.add_separator()
        
        filemenu.add_command(label="Export MySQLDatabase", command=self.export_db)
        filemenu.add_command(label="Export CSV", command=self.export_csv)
        
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.destroy)
        
        # Edit Menu with Commands
        editmenu = Menu(menubar, tearoff=0)
        
        editmenu.add_command(label="Insert Row Above", command=self.insert_row)
        editmenu.add_command(label="Delete Current Row", command=self.delete_row)
        editmenu.add_command(label="Update Current Row", command=self.edit_row)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.open_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)
        
    def new_list(self):
        """Creates a new list. Empties the listbox."""
        self.app.clear_data()
        self.populate_listbox(self.app.data)
        self.set_infobox_msg("New list created.")
        
    def import_csv(self):
        """Loads a CSV file to the listbox."""
        path = askopenfilename(title="Philip Deck - Open", filetypes=[('CSV files', '*.csv')])
        # #ADD ERROR CHECKING
        if path is not None and path != "":
            self.app.set_file(path)
            self.app.load_data_from_file()
            self.populate_listbox(self.app.data)
            self.set_infobox_msg("Imported " + str(self.listbox.size()) + " rows from " + path)

    def import_db(self):
        """Loads data from a database to the listbox."""
        inputs = csvdialog.CSVInputDialog("Philip Deck - Db Import", "Host:", "User:", "Pass:", "Schema:", "Table:")  # Ask the user for credentials
        inputs.default_values(["localhost", "phil", "1473", "cst8333", "PythonDataset"])  # My defaults
        results = inputs.get_inputs()  # Wait for the results
        
        # Philip Deck
        if len(results) == 5:
            self.app.create_connection(results[0], results[1], results[2],
                                       results[3], results[4])  # Connect to a database with all parameters the user specified
            
            if self.app.test_connection():
                self.set_infobox_msg("Loading data.")
                
                qu = queue.Queue()  # Queue to signal the end of the database loading

                def db_proccess(q):
                    self.app.load_data_from_db()  # Load data from database
                    q.put(True)  # Signal end of db load
                    
                def update_listbox():
                    try:
                        qu.get(block=False)  # Try to see if the database is done loading
                        self.populate_listbox(self.app.data)  # Update the listbox
                        self.set_infobox_msg("Imported " + str(self.listbox.size()) + " rows from " 
                                             + self.app.db_helper.db_name + "." + self.app.db_helper.table_name)  # Give the user some info
                        
                        csvdialog.CSVAlertDialog("Philip Deck - Alert", "Editing rows in this file does not modify the database!" 
                                             + "\nExport to database to commit changes.").show_alert()  # Some info about the program
                    except queue.Empty:
                        self.set_infobox_msg(self.infobox.get() + ".")  # Add an extra dot
                        self.after(100, update_listbox)  # Recall the method until it updates
                    
                db_thread = threading.Thread(target=lambda: db_proccess(qu))  # Creating a thread object
                db_thread.start()  # Start the database loading thread
                update_listbox()  # Start the GUI update polling
                
            else:  # If the connection failed
                csvdialog.CSVAlertDialog("Philip Deck - Error", "Table not found.").show_alert()
            
    def export_csv(self):
        """Saves the data to a new CSV file."""
        path = asksaveasfilename(defaultextension=".csv", filetypes=[('CSV files', '*.csv')])
        
        # #ADD ERROR CHECKING
        if path is not None and path != "":
            self.app.save_file(path)
            self.set_infobox_msg("Saved to " + path)
    
    def export_db(self):
        """Exports data to a MySQL database."""
        inputs = csvdialog.CSVInputDialog("Philip Deck - Db Export", "Host:", "User:", "Pass:", "Schema:", "Table:")
        inputs.default_values(["localhost", "phil", "1473", "cst8333", "PythonDataset"])
        results = inputs.get_inputs()
        
        # #ADD ERROR CHECKING
        if len(results) == 5:
            self.app.create_connection(results[0], results[1], results[2], results[3], results[4])
            
            delete_table = askyesno("New Table?", "Create new table?")
            if delete_table:
                self.app.create_table()
            
            self.app.insert_records_into_table()
            self.set_infobox_msg("Inserted " + str(self.listbox.size()) + " rows into " + results[3] + "." + results[4])
            
    def populate_listbox(self, data):
        """Populates the listbox with data from the loader."""
        self.listbox.delete(0, END)
        for line in data:
            self.listbox.insert(END, line)
            
    def insert_row(self):
        """Inserts a row in the listbox and CSV data list at index n."""
        if not self.listbox.curselection():  # If no row is selected
            alert = csvdialog.CSVAlertDialog("Philip Deck - Alert", "You must select a row!")  # Display alert dialog
            alert.show_alert()
            return
        n = self.listbox.curselection()[0]  # Select the current row
        inputs = csvdialog.CSVInputDialog("Philip Deck - New row")  # Open a dialog
        for line in self.app.header:
            inputs.add_input(line)
        results = inputs.get_inputs()
        if results:
            self.listbox.insert(n, results)
            self.app.insert_row(n, results)
            self.set_infobox_msg("Inserted " + str(results))  # Set the infobox message
            
    def delete_row(self):
        """Deletes a row in the listbox and CSV data list at index n."""
        if not self.listbox.curselection():  # If no row is selected
            alert = csvdialog.CSVAlertDialog("Philip Deck - Alert", "You must select a row!")  # Display alert dialog
            alert.show_alert()
            return
        n = self.listbox.curselection()[0]  # Select the current row
        del_row = self.app.data[n]
        self.listbox.delete(n)  # Delete the row from the gui
        self.app.delete_row(n)  # Delete the row from the data
        self.set_infobox_msg("Deleted " + str(del_row))  # Set the infobox message
        
    def edit_row(self):
        if not self.listbox.curselection():  # If no row is selected
            alert = csvdialog.CSVAlertDialog("Alert", "You must select a row!")  # Display alert dialog
            alert.show_alert()
            return
        n = self.listbox.curselection()[0]  # Select the current row
        inputs = csvdialog.CSVInputDialog("Philip Deck - Edit row")  # Open a dialog
        for line in self.app.header:
            inputs.add_input(line)  # Add rows to the dialog window
        inputs.default_values(self.app.data[n])  # Adds default values to the dialog
        results = inputs.get_inputs()  # Get inputs from the user
        if results:
            self.listbox.delete(n)  # Delete the old row from the gui
            self.app.delete_row(n)  # Delete the old row from the data
            self.listbox.insert(n, results)  # Insert the updated row to the gui
            self.app.insert_row(n, results)  # Insert the row to the data
            self.set_infobox_msg("Updated " + str(inputs))  # Set the infobox message
        
    def open_about(self):
        """Opens a new window with information about the application."""
        root = Toplevel()
        
        lbl_info = Label(root, text="Created by Philip Deck\nFebruary 28, 2018.")
        lbl_info.pack(padx=12, pady=12)

        root.resizable(False, False)        
        root.grab_set()
        root.mainloop()

    def get_uptime(self):
        """Returns the up time of the window."""
        endtime = time.time()  # Get the uptime
        return endtime - self.startime
