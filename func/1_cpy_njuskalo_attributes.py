import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adds the parent folder to system path so custom modules can be imported

from func.my_library_function import origin_db       
from func.my_library_function import dest_db         
from func.my_library_function import update_insert_into_dest_base  

from psycopg2.extras import RealDictCursor            # Allows rows from SQL query to be returned as dictionaries instead of tuples

cursor = origin_db(cursor_factory_param=RealDictCursor)   # Connect to the source database using RealDictCursor

cursor.execute('select * from njuskalo_attributes')       # Execute a query to fetch all records from 'njuskalo_attributes' table

for desc in cursor.description:                           # Loop through column descriptions
    print(desc.name)                                     

result = cursor.fetchall()                                # Fetch all the data rows and store them as a list of dictionaries

# print(result)  

cur = dest_db(cursor_factory_param=RealDictCursor)        # Connect to the destination database

create = "create table if not exists njuskalo_attributes(id serial primary key, name_atr text, value text)"  # SQL statement to create the table if it doesn't already exist
update_insert_into_dest_base(create)                      # Execute the CREATE TABLE statement

insert = "insert into njuskalo_attributes (id, name_atr, value) values ({},'{}','{}')"  # SQL template for inserting each row

for row in result:                                        # Loop through each row (dictionary) from the source table
    com = insert.format(row['id'], row['name'], row['value_type'])  # Fill the insert statement with actual values
    update_insert_into_dest_base(com)                     # Execute the insert statement

cur.execute('select * from njuskalo_attributes')          
res = cur.fetchall()                                      
print(res)                                              



    

