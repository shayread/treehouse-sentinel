from util import constants
import sqlite3

'''
Database manager for the bird_identifications table. Contains database lifecycle and CRUD operations
'''

class BirdIdentificationsManager:

    TABLE_SCHEMA_PATH = "database/table/bird_identifications.sql"
    INSERT_QUERY_FORMAT = """
        INSERT INTO bird_identifications (bird_species, location, weather, temperature_fahrenheit, year, month, day, hour)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(self):
        self.db_connection = sqlite3.connect(constants.TABLE_STORAGE_PATH)
        self.db_cursor = self.db_connection.cursor()
        with open(self.TABLE_SCHEMA_PATH, "r") as schema_file:
            self.db_cursor.executescript(schema_file.read())

    def create_identification(self, bird_species, location, weather, temperature_farenheit, year, month, day, hour):
        entry_data = (bird_species, location, weather, temperature_farenheit, year, month, day, hour)
        self.db_cursor.execute(self.INSERT_QUERY_FORMAT, entry_data)
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()
