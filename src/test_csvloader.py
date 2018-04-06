'''
Created on Feb 13, 2018

Unit testing with pytest.

@author: Philip Deck
'''
import filesource
import datasource


def test_filesource_loadata():
    """Test load_data from file reader"""
    file = filesource.FileSource("C:\\Users\\Philtop\\Documents\\eclipse-workspace\\cst8333_CSVLoader\\src\\03290040-eng.csv")
    header, data = file.load_data()
    assert data[0] == ['Jan-81', 'Canada', 'Meat, fish and dairy products', 'v1574569', '1.1', '60.9']
    assert header == ['Ref_Date', 'GEO', 'COMMOD', 'Vector', 'Coordinate', 'Value']


def test_datasource_loaddata():
    """Test load_data from database"""
    db = datasource.DataSource(db_host="localhost",
                               db_user="phil",
                               db_pass="1473",
                               db_name="cst8333",
                               table_name="PythonDataset")

    data = db.get_all_records()
    assert data[0] == ['Jan-81', 'Canada', 'Meat, fish and dairy products', 'v1574569', '1.1', '60.9']


def test_datasource_getheader():
    """Test load headers from database"""
    db = datasource.DataSource(db_host="localhost",
                               db_user="phil",
                               db_pass="1473",
                               db_name="cst8333",
                               table_name="PythonDataset")
    headers = db.get_headers()
    assert headers == ['Ref_Date', 'GEO', 'COMMOD', 'Vector', 'Coordinate', 'Value']

#Philip Deck
def test_filesource_savefile():
    '''Test save from database into a file'''
    db = datasource.DataSource(db_host="localhost",
                               db_user="phil",
                               db_pass="1473",
                               db_name="cst8333",
                               table_name="PythonDataset")

    data = db.get_all_records()
    headers = db.get_headers()
    file = filesource.FileSource("C:\\Users\\Philtop\\Documents\\eclipse-workspace\\cst8333_CSVLoader\\src\\test.csv")
    file.save_file(data, headers)
    file.close_file()

    header, data = file.load_data()
    assert data[0] == ['Jan-81', 'Canada', 'Meat, fish and dairy products', 'v1574569', '1.1', '60.9']
    assert header == ['Ref_Date', 'GEO', 'COMMOD', 'Vector', 'Coordinate', 'Value']

    
def test_datasource_export():
    '''Test export to database'''
    file = filesource.FileSource("C:\\Users\\Philtop\\Documents\\eclipse-workspace\\cst8333_CSVLoader\\src\\test.csv")
    header, data = file.load_data()
    db = datasource.DataSource(db_host="localhost",
                               db_user="phil",
                               db_pass="1473",
                               db_name="cst8333",
                               table_name="TestPythonDataset")
    db.insert_records_into_table(data)
    data = db.get_all_records()
    assert data[0] == ['Jan-81', 'Canada', 'Meat, fish and dairy products', 'v1574569', 1.1, '60.9']
    assert header == ['Ref_Date', 'GEO', 'COMMOD', 'Vector', 'Coordinate', 'Value']