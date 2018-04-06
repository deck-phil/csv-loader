'''
Created on Feb 12, 2018

Handles file I/O of csv files.

@author: Philip Deck
'''
import csv


class FileSource():
    '''Handles file I/O of csv files.'''

    def __init__(self, file_name):
        '''Constructor'''
        self.file_name = file_name
        self.file = None
        
    def load_data(self):
        """Iterates through csv file with csv.reader and adds entries to a list."""
        
        try:
            print("Loading data...")
            self.open_file()
            reader = csv.reader(self.file)
            
            data = list()
            for i, line in enumerate(reader):
                data.insert(i, line)

            header = data[0]
            del data[0] #Delete the first header line
            
            
        except FileNotFoundError:
            print("File", self.file_name, "not found.")    
        finally:
            self.close_file()

        return header, data
            
    def save_file(self, data, header):
        """Saves a file to csv format with headers as the first line."""
        try:
            print("Loading data...")
            self.open_file('w')
            writer = csv.writer(self.file,lineterminator="\n", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            writer.writerow(header)
            writer.writerows(data)
            
        finally:
            self.close_file()
    
    def open_file(self, open_type ="rt"):
        """Opens a file with the file name provided."""
        try:
            self.file = open(self.file_name, open_type, encoding='utf-8')
        except FileNotFoundError:
            print("File", self.file_name, "not found.")
    
    def close_file(self):
        """Close the current file."""        
        try:
            self.file.close()
        except AttributeError:
            print("File reader is already closed or None.")
