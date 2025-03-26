# OVERVIEW

This is my project where I aim to demonstrate what I have learned so far and continue to refine my knowledge. Through this project, I learned how to transfer records from one database to another while also understanding how to establish a connection to a different database. After that, I created my own tables to store specific data relevant to my further analysis.

# SOURCE DB

In this project, I extracted data from a structured database where records were stored in tables with the format described below. 

![examplepic](https://github.com/ValeNovak/zagreb_house_market/blob/main/img/ex1.png)


The database also includes an additional table that is linked via a foreign key to the attribute_type column. This table stores the names of the attributes and their respective types, which help to identify what each attribute represents. The reason for implementing this structure is that the previous table cannot store different data types in the same columns, and this separation ensures that the data is correctly categorized and structured.

The database includes a procedure that pivots the table, ensuring that for each attribute, we retrieve the most recent value based on the latest entry date. This transformation structures the data into columns, making it more organized and easier to interpret.

Here is an example of pivot table:

| njuskalo_id | author          | Naslov           | Balkon/Loda/Terasa | Broj etaze | Broj parkirnih mjesta | Broj soba | Cijena  | Energetski razred | Godina izgradnje | Kat | Lokacija    | Netto povrsina | Oglas objavljen | Oglas prikazan | Stambena povrsina | Tip stana            |
|-------------|-----------------|------------------|--------------------|------------|-----------------------|-----------|---------|-------------------|------------------|-----|-------------|-----------------|-----------------|----------------|-------------------|----------------------|
| 12345678    | ABC Nekretnine  | Stan na prodaju  | Balkon, Terasa     | 3          | 2                     | 3         | 250000  | A                 | 2015             | 2   | Centar grada | 65              | 2025-03-10      | 1               | 60                | u stambenoj zgradi   |
| 87654321    | XYZ Nekretnine  | Kuća s vrtom     | Balkon             | 2          | 1                     | 4         | 248000  | B                 | 2010             | 1   | Trsat        | 85              | 2025-03-09      | 0               | 80                | u stambenoj zgradi   |
| 13579246    | LMN Nekretnine  | Luksuzni penthouse | Terasa            | 1          | 2                     | 5         | 500000  | A+                | 2022             | 5   | Riva         | 120             | 2025-03-11      | 1               | 115               | u stambenoj zgradi   |


# MY DATABASE PROCESS


First, I created two functions to establish connections with the databases:

1. origin_db: This function connects to the source database from which I pull the data.

2. dest_db: This function connects to my destination database where I store the processed data.

Both functions return a cursor that can be used to execute SQL queries.

Additionally, there’s a function in the file that executes an update or insert query on the destination database and commits the changes.

## Main Goals and Approach:
The primary goal was to create a function that retrieves a list of rows from the source database. This list is filtered based on the city I want by using a predefined procedure in the source database. To make the city filtering flexible, I generalized it by using the city_pattern parameter. Below, you can see my code:


```python
def get_latest_data_by_city(fromwhichbase, city_name):
    # The function retrieves the latest data from the specified database, filtering results based on the selected city.
    city_pattern = "%" + city_name + "%"  # Prepares a pattern for SQL LIKE search (matches anywhere in the text)

    fromwhichbase.execute("select distinct njuskalo_id, author from njuskalo_home_crawled_data_attrributes where value_text like %s", (city_pattern,))
    rezultat = fromwhichbase.fetchall()  # Retrieves all matching records
    list_of_rows = []

    for key in rezultat:
        njuskalo_id = key['njuskalo_id']
        author = key['author']
        author = author.replace("'", "''")  # Escapes single quotes to prevent SQL errors
        fromwhichbase.execute("select * from get_latest_data_attributes_for_njuskalo_id(%s, %s)", (njuskalo_id, author))
        result = fromwhichbase.fetchone()

        if result is not None:  # Adds the result to the list if it's not empty
            list_of_rows.append(result)  # Returns the list of retrieved data
    return list_of_rows
```


Lastly, the main goal was to transfer the selected data to my zagreb_app table in the destination database for future analysis. If the data already exists in the zagreb_app table (identified by the unique ID), I update only the values that have changed.

In addition, I created a function to track the price changes of properties. This function stores the previous and new prices in a separate columns to allow for analysis of price fluctuations over time. This feature provides valuable insights into how property owners adjust prices, whether they increase or decrease them, enabling better future analysis of property price trends.

This approach allows for efficient data transfer and ensures that the destination table is always up-to-date with the latest property listings.

All the functions that I have done you can see in my script: [Link to my script](C:\Users\Valentina\Desktop\Škola\baza_njuskalo\func\my_library_function.py)

## MY REPORTS

In the new folder called [generate_report](generate_report) I started generating daily reports based on apartment data in Zagreb. The goal is to create a table with data that interests me, which would be generated daily so I can track changes in the data, such as the median apartment prices per square meter, the number of ads posted by agencies, the number of ads posted by private users, and so on. I am currently testing it in Jupyter Notebook using the pandas library. The goal with this data is to later perform analyses and eventually include it in Power BI for more advanced insights.


# CONCLUSION

In the past, I learned Python through the book "Learn Python" by Allen B. Downey. Now, with this project, I am expanding my knowledge and skills by learning on my own and following tutorials. This project marks the beginning of my journey into the data world, where I'm developing the skills needed to work with data effectively. Through this project, I’ve learned how to connect to databases using Python and SQL, how to transfer data from one database to another, and how to logically approach which data is necessary to display meaningful insights.

Though the project is still in development, it has helped me build a solid foundation in handling data, and I am excited to continue learning and improving these skills.


