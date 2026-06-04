import sqlite3

'''
Database manager for the bird_identifications table. Contains database lifecycle and CRUD operations
'''

class BirdIdentificationsManager:

    TABLE_STORAGE_PATH = "database/table/storage/bird_identifications.db"
    INSERT_QUERY_FORMAT = "INSERT INTO bird_identifications (bird_species, location, weather, temperature_fahrenheit) VALUES (?, ?, ?, ?)"

    def __init__(self):
        self.db_connection = sqlite3.connect(self.TABLE_STORAGE_PATH)
        self.db_cursor = self.db_connection.cursor()

    def create_identification(self, bird_species, location, weather, temperature_farenheit):
        entry_data = (bird_species, location, weather, temperature_farenheit)
        self.db_cursor.execute(self.INSERT_QUERY_FORMAT, entry_data)
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()
