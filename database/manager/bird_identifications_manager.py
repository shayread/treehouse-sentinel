from util import constants
import sqlite3

'''
Database manager for the bird_identifications table. Contains database lifecycle and CRUD operations
'''

class BirdIdentificationsManager:

    TABLE_SCHEMA_PATH = "database/table/bird_identifications.sql"
    INSERT_QUERY_FORMAT = """
        INSERT INTO bird_identifications (bird_species, country, region, city, weather, temperature_fahrenheit, year, month, day, hour)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    PRIMARY_KEY_QUERY_FORMAT = """
        SELECT * 
        FROM bird_identifications
        WHERE bird_species = ? AND year = ? AND month = ? AND day = ? AND hour = ?
    """

    def __init__(self):
        self.db_connection = sqlite3.connect(constants.TABLE_STORAGE_PATH)
        self.db_cursor = self.db_connection.cursor()
        with open(self.TABLE_SCHEMA_PATH, "r") as schema_file:
            self.db_cursor.executescript(schema_file.read())

    # Checks for existing table items with the same primary key, returns boolean
    def has_duplicate_identification(self, bird_species, year, month, day, hour):
        query_data = (bird_species, year, month, day, hour)
        self.db_cursor.execute(self.PRIMARY_KEY_QUERY_FORMAT, query_data)
        return len(self.db_cursor.fetchall()) > 0

    def create_identification(self, bird_species, country, region, city, weather, temperature_fahrenheit, year, month, day, hour):
        entry_data = (bird_species, country, region, city, weather, temperature_fahrenheit, year, month, day, hour)
        self.db_cursor.execute(self.INSERT_QUERY_FORMAT, entry_data)
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()
