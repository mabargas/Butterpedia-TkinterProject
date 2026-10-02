-- (1)creating the table
--AUTOINCREMENT was added because I read that it allows for easier ID handling for deleted rows and added rows
-- check is used to ensure that the metric is either inches or centimeters
-- image is a BLOB since the images are going to be referred by a path
-- CREATE TABLE butterflies (
--     butterfly_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     rarity TEXT NOT NULL,
--     est_population TEXT NOT NULL,
--     main_family TEXT NOT NULL,
--     sub_family TEXT NOT NULL,
--     color TEXT NOT NULL,
--     wing_patterns TEXT NOT NULL,
--     wingspan_size INTEGER NOT NULL,
--     metric TEXT CHECK(metric IN ('in', 'cm')) NOT NULL,
--     image BLOB);
-- -- (2) Second Table for Butterfly Habitat
CREATE TABLE butterflies_habitat (
    habitat_id INTEGER PRIMARY KEY,
    butterfly_id INTEGER,             
    location TEXT NOT NULL,   
    region TEXT NOT NULL,      
    FOREIGN KEY (butterfly_id) REFERENCES butterflies(butterfly_id)
);
