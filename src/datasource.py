'''
Created on Feb 12, 2018

Handles database connection and SQL queries

@author: Philip Deck
'''
import time
from MySQLdb import connect  # https://github.com/PyMySQL/mysqlclient-python
from _mysql_exceptions import OperationalError


# Class that handles the database methods and connections
class DataSource():
    '''Handles database connection and SQL queries'''

    def __init__(self,
                 db_host,
                 db_user,
                 db_pass,
                 db_name,
                 table_name):
        '''Constructor'''
        self.db_host = db_host  # Database Host( Most likely 'localhost')
        self.db_user = db_user  # Database username
        self.db_pass = db_pass  # Database password
        self.db_name = db_name  # Databse schema name
        self.table_name = table_name  # Database table name
        self.db = None

    # Insert records from csv file
    def insert_records_into_table(self,
                   data_list: list):
        """Inserts a list of records into the database."""

        try:
            insert_statement = self.get_insert_statement(self.get_headers())
            
            self.open_database()
            
            with self.db.cursor() as cursor:

                print("Starting database insert.")
                pre = time.time()
                cursor.executemany(insert_statement, data_list)
                self.db.commit()
                post = time.time()
                
                print("Finished database insert. Took {0:.2f} seconds.".format(post - pre))
                print("Inserted", len(data_list), "rows into", self.table_name, "in schema", self.db_name + ".")
        finally:
            cursor.close()
            self.close_database()
    
    def get_insert_statement(self, header):
        """Builds an insert statement based on the header."""
            # Statement Builder
            # Builds a create table statement based on the names and number of headers
        insert_statement = "INSERT INTO " + self.table_name + "("
        values = ") VALUES ("
        for header in self.get_headers():
            insert_statement += header + ","
            values += "%s,"
        values = values[0:-1] + ")"
        insert_statement = insert_statement[0:-1]
        insert_statement += values
            
        # Prints out something like this.
        # """INSERT INTO tablename (%s,%s,%s) VALUES (value1,value2,value3);"""
        return insert_statement
            
    def get_all_records(self):
        """Gets all records of the database as a list."""
        try:
            self.open_database()  # Open the database.
            with self.db.cursor() as cursor:  # Create a cursor.
                cursor.execute('select * from ' + self.table_name + ';')  # Select all from the table.
                data = list(cursor.fetchall())  # Execute the query.
                print("Got all", len(data), "records.")
                for i, line in enumerate(data):
                    data[i] = list(line)  # Converting every line from a tuple to a list.
                return data
        finally:
            cursor.close()  # Close the cursor.
            self.close_database()  # Close the database.
            
    def get_headers(self):
        """Returns a list of headers from the database."""
        try:
            self.open_database()
            with self.db.cursor() as cursor:
                cursor.execute('select distinct column_name from information_schema.columns where table_name = "' + self.table_name + '" and table_schema = "' + self.db_name + '" order by ordinal_position;')
                headers = list()
                for header in cursor.fetchall():
                    headers.append(header[0])
                return headers
        finally:
            cursor.close()
            self.close_database()
                    
    def delete_all_records(self):
        """Deletes all records from the table."""
        try:
            self.open_database()
            with self.db.cursor() as cursor:
                print("\tClearing rows from", self.table_name, "in", self.db_name + ".")
                cursor.execute("TRUNCATE TABLE " + self.table_name)
        except AttributeError:
            print("Cursor is None. Database must not have been initialized")
        finally:
            self.close_database()
    
    def set_table(self,
                 table_name: str):
        """Changes the working table"""
        if table_name:
            self.table_name = table_name
            
    def create_table(self,
                    header):
        if not header:
            return
        try:
            self.open_database()
            with self.db.cursor() as cursor:
                create_table_statement = "CREATE TABLE " + self.table_name + "("
                for column in header:
                    create_table_statement += column + " VARCHAR(255),"
                create_table_statement = create_table_statement[0:-1] + ");"
                print("Dropping " + self.table_name)
                cursor.execute("DROP TABLE IF EXISTS " + self.table_name)
                print("Creating " + self.table_name)
                cursor.execute(create_table_statement)
                cursor.close()
        finally:
            self.close_database()

    def open_database(self):  # Opens a connection.
        """Opens a database with the parameters passed."""
        try:
            print("\t>>Opening a database session...")
            self.db = connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, db=self.db_name)  # Connect to the database.
        except OperationalError:
            print("Wrong database credentials. Closing connection.")
    
    def close_database(self):  # Closes a connection.
        """Close the current database."""
        if self.db is not None and self.db.open:
            print("\t>>Closing database session.")
            self.db.close()  # Close the database.
        else:
            print("Database was not initialized.")
    
    def test_connection(self):
        """A simple test connection method."""
        connected = False
        try:
            self.open_database()
            with self.db.cursor() as cursor:
                cursor.execute('select * from ' + self.table_name + ' limit 1;')
                cursor.close()
            print("Connection successful.")
            connected = True
        except Exception as err:
            print(err)
        finally:
            self.close_database()
            return connected
