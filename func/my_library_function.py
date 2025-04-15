import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()



def origin_db(cursor_factory_param=None): # connecting to the database origin_db via the psycopg library
    conn = psycopg2.connect(f'host={os.getenv("SECRET_HOST")} port={os.getenv("SECRET_PORT")} user={os.getenv("SECRET_USER")} password={os.getenv("SECRET_PASS")} dbname={os.getenv("DBNAME")}')
    if cursor_factory_param == None:
        return conn.cursor()
    else:
        return conn.cursor(cursor_factory=cursor_factory_param)
    


def dest_db(cursor_factory_param=None): # connecting my database dest_db via the psycopg library
    con = psycopg2.connect(f'host={os.getenv("my_host")} port={os.getenv("my_port")} user={os.getenv("my_user")} password={os.getenv("my_password")} dbname={os.getenv("my_dbname")}')
    if cursor_factory_param == None:
        return con.cursor()
    else:
        return con.cursor(cursor_factory=cursor_factory_param)



def update_insert_into_dest_base(qu): # This function executes an update or insert query on the database and commits the changes
    con = psycopg2.connect(f'host={os.getenv("my_host")} port={os.getenv("my_port")} user={os.getenv("my_user")} password={os.getenv("my_password")} dbname={os.getenv("my_dbname")}')
    cur = con.cursor()
    cur.execute(qu)
    con.commit()
    con.close()





def get_latest_data_by_city (fromwhichbase,city_name): # The function retrieves the latest data from the specified database, filtering results based on the selected city.
    city_pattern = "%" + city_name + "%" # Prepares a pattern for SQL LIKE search (matches anywhere in the text)

    fromwhichbase.execute("select distinct njuskalo_id, author from njuskalo_home_crawled_data_attrributes where value_text like %s", (city_pattern,))
    rezultat = fromwhichbase.fetchall() # Retrieves all matching records
    list_of_rows=[]

    for key in rezultat:
        njuskalo_id = key['njuskalo_id']  
        author = key['author']
        author = author.replace("'", "''") # Escapes single quotes to prevent SQL errors
        fromwhichbase.execute("select * from get_latest_data_attributes_for_njuskalo_id(%s, %s)", (njuskalo_id, author))
        result = fromwhichbase.fetchone()

        if result != None: # Adds the result to the list if it's not empty
            list_of_rows.append(result) # Returns the list of retrieved data
    return list_of_rows




from datetime import datetime

def track_price_update(row, existrow):
    if row['Cijena'] != existrow ['Cijena']:
        old_price = existrow['Cijena']
        new_price = row['Cijena']
        today = datetime.now()

        insert_query = f'''
        INSERT INTO update_price (njuskalo_id, author, old_price, new_price, date_of_up)
        VALUES ({row['njuskalo_id']}, '{row["author"]}', {old_price}, {new_price}, '{today}')
        '''
        update_insert_into_dest_base(insert_query)

        print(f"Price change recorded for ID {row['njuskalo_id']} on {today}: Old Price = {old_price}, New Price = {new_price}")




def update_insert_table_with_latest_data(getlatestdatafunc,towhichbase,fromwhichbase):  # Loop through the latest data to insert or update

    for row in getlatestdatafunc: # Check if the record already exists in the target table
    
        towhichbase.execute("SELECT * FROM zagreb_app WHERE njuskalo_id=%s AND author=%s", (row['njuskalo_id'], row['author']))
        existrow = towhichbase.fetchone() # Check if the record already exists in the target table
        
        if existrow: # If record exists, compare values and update if necessary
            for key, value in row.items():
                if key != 'njuskalo_id':
                    if key != 'author':      # If value has changed, update it in the target table
                        
                        if existrow[key] != value:

                            print("UPDATE made by : ", row['njuskalo_id'], key, value, existrow[key])

                            fromwhichbase.execute(f"select value_type from njuskalo_attributes where name='{key}'") # Fetch value type for the column from the source database
                            value_type = fromwhichbase.fetchone()['value_type']
                            setvalues = []
                            # Format the value based on its type before creating the SQL query
                            if value_type == 'text':
                                if value == None:
                                    row[key] = 'NULL'
                                else:
                                    if "'" in value:
                                        value = value.replace("'", "''")
                                    setvalues = f"\"{key}\"='{value}'"
                            elif value_type == 'int':
                                if value == None:
                                    row[key] = 'NULL'
                                else:
                                    setvalues=f'"{key}"={value}'
                            elif value_type == 'double':
                                if value == None:
                                    row[key] = 'NULL'
                                else:
                                    setvalues=f'"{key}"={value}'
                            elif value_type == 'date':
                                if value == None:
                                    row[key] = 'NULL'
                                else:
                                    
                                    setvalues=f"\"{key}\"='{value}'"
                            else:
                                setvalues='Null'
                        
                            if setvalues: # Execute the update query if a value was set
                                query = f"UPDATE zagreb_app SET {setvalues} WHERE njuskalo_id = {row['njuskalo_id']} AND author = '{row['author']}'"
                                update_insert_into_dest_base(query)
        
            track_price_update(row, existrow)
                                
        else:   # If record doesn't exist, insert a new row into the target table
            for key, value in row.items():
                if key != 'njuskalo_id' and key != 'author':
                    
                    fromwhichbase.execute(f"select value_type from njuskalo_attributes where name='{key}'") # Fetch value type for the column from the source database
                    value_type = fromwhichbase.fetchone()['value_type']

                     # Format the value based on its type for insertion
                    if value_type == 'text':
                        if value == None:
                            row[key] = 'NULL'
                        else:
                            if "'" in value:
                                value = value.replace("'", "''")
                            row[key]=f"'{value}'"
                    elif value_type == 'int':
                        if value == None:
                            row[key] = 'NULL'      
                    elif value_type == 'double':
                        if value == None:
                            row[key] = 'NULL'
                    elif value_type == 'date':
                        if value == None:
                            row[key] = 'NULL'
                        else:
                            row[key]=f"'{value}'"

            # Construct the insert query for the new record
            insert =f'''INSERT INTO zagreb_app (
            njuskalo_id, 
            author, 
            "Naslov", 
            "Balkon/Loda/Terasa", 
            "Broj etaze", 
            "Broj parkirnih mjesta", 
            "Broj soba", 
            "Cijena", 
            "Energetski razred", 
            "Godina izgradnje", 
            "Kat", 
            "Lokacija", 
            "Netto povrsina", 
            "Oglas objavljen", 
            "Oglas prikazan", 
            "Stambena povrsina", 
            "Tip stana"
        ) 
        VALUES ({row['njuskalo_id']}, '{row["author"]}', {row["Naslov"]}, {row["Balkon/Loda/Terasa"]}, 
            {row["Broj etaze"]}, {row["Broj parkirnih mjesta"]}, {row["Broj soba"]}, {row["Cijena"]}, 
            {row["Energetski razred"]}, {row["Godina izgradnje"]}, {row["Kat"]}, {row["Lokacija"]}, 
            {row["Netto povrsina"]}, {row["Oglas objavljen"]}, {row["Oglas prikazan"]}, 
            {row["Stambena povrsina"]}, {row["Tip stana"]})'''
                
            print('INSERT made for ID: ', row['njuskalo_id'])
            update_insert_into_dest_base(insert) # Execute the insert query





