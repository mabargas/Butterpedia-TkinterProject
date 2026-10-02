
#Name: Mei Lan Bargas
#Course: ITEC 352

import sqlite3


class ButterflyLibraryMain():
    def __init__(self):
        #Connecting to the Databse
        self.conn = sqlite3.connect('Butterpedia_Database.db')
        #Communicating with the database to do whatever function I am coding
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    #Add Butterflies backend code, call this in main with my .get() method
    def add_butterflymain(self,name,rarity,species_amt, mainfamily,subfamily,color,wingpatterns, wingspan,metric,img_bin, location, region):
        #Query to insert data into the database
        data_insert_query = '''INSERT INTO butterflies (name, rarity, species_amt, 
                    main_family, sub_family, color, wing_patterns, wingspan_size, 
                    metric, image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        #Assigning variables to the columns in my query
        data_insert_tuple = (name,rarity,species_amt,mainfamily, subfamily,color,wingpatterns,wingspan,metric,img_bin)
        
        #Execute Query to insert entry data into the database
        self.cursor.execute(data_insert_query, data_insert_tuple)

        #Get the id of the last row inserted to use for my next query
        butterfly_id = self.cursor.lastrowid

        habitat_insert_query = '''INSERT INTO butterflies_habitat (butterfly_id, location, region) VALUES(?, ?, ?) '''
        habitat_insert_tuple = (butterfly_id, location, region)
        self.cursor.execute(habitat_insert_query, habitat_insert_tuple)
        
        #Saving it to the database
        self.conn.commit()

    #Backend code to retrieve butterflies from the database
    def get_butterflies_main(self):
        self.cursor.execute('''SELECT butterfly_id, name, main_family, sub_family, color, wing_patterns, wingspan_size, metric, image from butterflies''')
        #Retrieving items from the database
        butterflies = self.cursor.fetchall()
        return butterflies
        
    def get_butterflies_hab(self):
        hab_data_insert_query = '''SELECT butterflies.butterfly_id, butterflies.name, butterflies.rarity, 
        butterflies.species_amt, butterflies.image, butterflies_habitat.location, butterflies_habitat.region FROM butterflies 
        JOIN butterflies_habitat ON butterflies.butterfly_id = butterflies_habitat.butterfly_id'''
        self.cursor.execute(hab_data_insert_query)
        butterflies_hab = self.cursor.fetchall()
        return butterflies_hab
       
    def delete_butterfly(self, butterfly_id):
        #Delete Query
        delete_main = "DELETE FROM butterflies WHERE butterfly_id = ?"
        #Run the execution, similar to adding, but we are removing
        self.cursor.execute(delete_main, (butterfly_id,))

        delete_habitat = "DELETE FROM butterflies_habitat WHERE butterfly_id = ?"
        self.cursor.execute(delete_habitat, (butterfly_id,))
        self.conn.commit()
    