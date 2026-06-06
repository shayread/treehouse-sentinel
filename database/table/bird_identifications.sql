/*
 * Schema for the bird_identifications table. Stores unique identifications based on species + timestamp combos
 */

CREATE TABLE bird_identifications (
    bird_species TEXT NOT NULL,
    location TEXT NOT NULL,
    weather TEXT NOT NULL,
    temperature_fahrenheit INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    PRIMARY KEY(bird_species, year, month, day, hour)
)