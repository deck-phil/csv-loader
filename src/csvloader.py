'''
Created on Feb 12, 2018

Class that holds data and 
delegates task to separate modules.

@author: Philip Deck
'''
import datasource
import filesource


# Handles file operations
class CSVLoader():
    '''Holds data and delegates task to separate modules.'''

    def __init__(self):
        '''Constructor'''
        self.data = list()
        self.header = list()
        self.db_helper = None
        self.file_helper = None

    def create_connection(self,
                         db_host: str,
                         db_user: str,
                         db_pass: str,
                         db_name: str,
                         table_name: str):
        print("Saving database parameters...")
        print("\tHost:", db_host)
        print("\tUser:", db_user)
        print("\tPass:", db_pass)
        print("\tDatabase:", db_name)
        self.db_helper = datasource.DataSource(db_host, db_user, db_pass, db_name, table_name)
        
    def test_connection(self):
        return self.db_helper.test_connection()

    def set_file(self, file_name: str):
        """Changes the file name."""
        self.file_helper = filesource.FileSource(file_name)  # just makes a new file source object.

    def set_table(self,
                 table_name):
        """Changes the table to be used in the database."""
        self.db_helper.set_table(table_name)

    def load_data_from_file(self):
        """Loads data and header from file."""
        try:
            print("Getting data from file...")
            self.header, self.data = self.file_helper.load_data()

        except AttributeError:
            print("Set file name before loading data.")

    def save_file(self, file_path=""):
        """Saves a csv format file with all data in the list to a file."""
        print("Saving data to", file_path)
        file_helper = filesource.FileSource(file_path)
        file_helper.save_file(self.data, self.header)
    
    def load_data_from_db(self):
        """Load data from the database."""
        print("Getting data from database...")
        self.data = self.db_helper.get_all_records()
        print("Getting headers from database...")
        self.header = self.db_helper.get_headers()
    
    def insert_row(self, n, line):
        """Inserts a row into the data."""
        self.data.insert(n, line)
        
    def delete_row(self, n):
        del self.data[n]
    
    def insert_records_into_table(self):
        print("Inserting records")
        self.db_helper.insert_records_into_table(self.data)
        
    def delete_all_records(self):
        print("Deleting all records")
        self.db_helper.delete_all_records()
        
    def create_table(self):
        print("Creating new table.")
        self.db_helper.create_table(self.header)
        
    def is_connected(self):
        return self.db_helper.test_connection()

    def clear_data(self):
        print("Clearing data...")
        self.data = list()