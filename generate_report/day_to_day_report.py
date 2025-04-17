import sys
import os
import pandas as pd
from psycopg2.extras import RealDictCursor 
from datetime import datetime

# Add parent folder to system path to allow importing local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from func.my_library_function import dest_db       # Connects to destination DB
from func.my_library_function import update_insert_into_dest_base  # Executes & commits query

cursor = dest_db(cursor_factory_param=RealDictCursor)  # Connect to destination DB with dict-style rows

# Dictionary to store daily metrics
data_storage = {}

# Define constants (keys for the data_storage dict)
COUNT_OF_APARTMENTS_BY_AGENCIES = "count_of_apartments_by_agencies"
COUNT_OF_APARTMENTS_BY_PRIVATE_SELLER = "count_of_apartments_by_private_seller"
MEDIAN_PRICE_OF_APARTMENTS_BY_AGENCIES = "median_price_of_apartment_by_agencies"
MEDIAN_PRICE_OF_APARTMENTS_BY_PRIVATE_SELLER = "median_price_of_apartment_by_private_seller"
MEDIAN_PRICE_FOR_APARTMENTS_0_TO_40_M2_ZG = "median_price_for_apartments_0_to_40_m2_zg"
MEDIAN_PRICE_FOR_APARTMENTS_40_TO_80_M2_ZG = "median_price_for_apartments_40_to_80_m2_zg"
MEDIAN_PRICE_FOR_APARTMENTS_80_TO_120_M2_ZG = "median_price_for_apartments_80_to_120_m2_zg"
MEDIAN_PRICE_FOR_APARTMENTS_120_TO_MORE_M2_ZG = "median_price_for_apartments_120_to_more_m2_zg"
COUNT_OF_ENERGY_CLASS_A_PLUS = "count_of_energy_class_a_plus"
COUNT_OF_ENERGY_CLASS_A = "count_of_energy_class_a"
COUNT_OF_ENERGY_CLASS_B = "count_of_energy_class_b"
COUNT_OF_ENERGY_CLASS_C = "count_of_energy_class_c"
COUNT_OF_ENERGY_CLASS_D = "count_of_energy_class_d"
COUNT_OF_ENERGY_CLASS_E = "count_of_energy_class_e"
COUNT_OF_ENERGY_CLASS_F = "count_of_energy_class_f"
COUNT_OF_ENERGY_CLASS_G = "count_of_energy_class_g"
COUNT_OF_UPDATE_PRICE_PER_DAY = "count_of_update_price_per_day"
COUNT_OF_UPDATE_PRICE_INCREASE_PER_DAY = "count_of_update_price_increase_per_day"
COUNT_OF_UPDATE_PRICE_DECREASE_PER_DAY = "count_of_update_price_decrease_per_day"



# Get apartments from agencies (filtering out names that look like private sellers)   AGENCIES POST 
query_for_agencies = """SELECT *
FROM zagreb_app z
WHERE NOT EXISTS (
    SELECT *
    FROM (
        SELECT * 
        FROM zagreb_app
        WHERE author not ilike '%nekretnine%' 
            and author not ilike '%nekretnina%'
            and author not ilike '%d.o.o%' 
            and author not ilike '%real%' 
            and author not ilike '%Immobilien%' 
            and author not ilike '%properties%'
            and author not ilike '%agencija%'
            and author not ilike '%projekt%'
            and author not ilike '%www%'
            and LEFT(author, 1) != UPPER(LEFT(author, 1))
    ) as consumeri
    WHERE consumeri.author = z.author
)
AND author !~ '\\d+$' 
AND author !~ '^[^A-Za-z0-9]'
ORDER BY author"""

cursor.execute(query_for_agencies)                        
result_agency_set = cursor.fetchall()                    

df_agency = pd.DataFrame(data=result_agency_set)          # Convert to pandas DataFrame

# Store agency apartment count and median price
data_storage[COUNT_OF_APARTMENTS_BY_AGENCIES] = int(df_agency['njuskalo_id'].count())
data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_AGENCIES] = float(df_agency['Cijena'].median())






# Query for private sellers (opposite filters)  PRIVATE POST
query_for_private_per = '''SELECT * 
FROM zagreb_app
WHERE author not ilike '%nekretnine%' 
    and author not ilike '%nekretnina%'
    and author not ilike '%d.o.o%' 
    and author not ilike '%real%' 
    and author not ilike '%Immobilien%' 
    and author not ilike '%properties%'
    and author not ilike '%agencija%'
    and author not ilike '%projekt%'
    and author not ilike '%www%'
    and LEFT(author, 1) != UPPER(LEFT(author, 1))'''

cursor.execute(query_for_private_per)
result_private_per_set = cursor.fetchall()

df_private = pd.DataFrame(data=result_private_per_set)

# Store private seller apartment count and median price
data_storage[COUNT_OF_APARTMENTS_BY_PRIVATE_SELLER] = int(df_private['njuskalo_id'].count())
data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_PRIVATE_SELLER] = float(df_private['Cijena'].median())




# Get all Zagreb apartments          ZAGREB BY SQUARE METER
cursor.execute('SELECT * FROM zagreb_app')
result_zagreb_set = cursor.fetchall()
df_zagreb = pd.DataFrame(data=result_zagreb_set)

# Filter apartments by size ranges and calculate median prices
filtered_data_0_40 = df_zagreb[(df_zagreb['Stambena povrsina'] > 0) & (df_zagreb['Stambena povrsina'] < 40)]
filtered_data_40_80 = df_zagreb[(df_zagreb['Stambena povrsina'] > 40) & (df_zagreb['Stambena povrsina'] < 80)]
filtered_data_80_120 = df_zagreb[(df_zagreb['Stambena povrsina'] > 80) & (df_zagreb['Stambena povrsina'] < 120)]
filtered_data_120_more = df_zagreb[(df_zagreb['Stambena povrsina'] > 120)]

# Store size-based median prices
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_0_TO_40_M2_ZG] = float(filtered_data_0_40['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_40_TO_80_M2_ZG] = float(filtered_data_40_80['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_80_TO_120_M2_ZG] = float(filtered_data_80_120['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_120_TO_MORE_M2_ZG] = float(filtered_data_120_more['Cijena'].median())


# Count apartments by energy class          ZAGREB BY ENERGY CLASS
count_a_plus = df_zagreb['Energetski razred'].value_counts().get('A+', 0)
count_a = df_zagreb['Energetski razred'].value_counts().get('A', 0)
count_b = df_zagreb['Energetski razred'].value_counts().get('B', 0)
count_c = df_zagreb['Energetski razred'].value_counts().get('C', 0)
count_d = df_zagreb['Energetski razred'].value_counts().get('D', 0)
count_e = df_zagreb['Energetski razred'].value_counts().get('E', 0)
count_f = df_zagreb['Energetski razred'].value_counts().get('F', 0)
count_g = df_zagreb['Energetski razred'].value_counts().get('G', 0)

# Store counts by energy class
data_storage[COUNT_OF_ENERGY_CLASS_A_PLUS] = int(count_a_plus)
data_storage[COUNT_OF_ENERGY_CLASS_A] = int(count_a)
data_storage[COUNT_OF_ENERGY_CLASS_B] = int(count_b)
data_storage[COUNT_OF_ENERGY_CLASS_C] = int(count_c)
data_storage[COUNT_OF_ENERGY_CLASS_D] = int(count_d)
data_storage[COUNT_OF_ENERGY_CLASS_E] = int(count_e)
data_storage[COUNT_OF_ENERGY_CLASS_F] = int(count_f)
data_storage[COUNT_OF_ENERGY_CLASS_G] = int(count_g)



# ZAGREB BY UPDATE PRICE 
cursor.execute('SELECT * FROM update_price')
result_update_price_set = cursor.fetchall()
df_update_price_zg = pd.DataFrame(data=result_update_price_set)

if not df_update_price_zg.empty:
    data_storage[COUNT_OF_UPDATE_PRICE_PER_DAY] = len(df_update_price_zg)

    filtered_data_price_increase = df_update_price_zg[df_update_price_zg['old_price'] < df_update_price_zg['new_price']]
    filtered_data_price_decrease = df_update_price_zg[df_update_price_zg['old_price'] > df_update_price_zg['new_price']]

    data_storage[COUNT_OF_UPDATE_PRICE_INCREASE_PER_DAY] = int(filtered_data_price_increase['id'].count())
    data_storage[COUNT_OF_UPDATE_PRICE_DECREASE_PER_DAY] = int(filtered_data_price_decrease['id'].count())
else:
    # If DataFrame is empty, set all counts to 0
    data_storage[COUNT_OF_UPDATE_PRICE_PER_DAY] = 0
    data_storage[COUNT_OF_UPDATE_PRICE_INCREASE_PER_DAY] = 0
    data_storage[COUNT_OF_UPDATE_PRICE_DECREASE_PER_DAY] = 0


data_storage['date_of_reporting'] = datetime.today().strftime('%Y-%m-%d')



# INSERT ALL VALUES
# Define SQL insert query for all report values
insert_que = '''INSERT INTO day_to_day_report (
    date_of_reporting,
    count_of_apartments_by_agencies,
    count_of_apartments_by_private_seller,
    median_price_of_apartment_by_agencies,
    median_price_of_apartment_by_private_seller,
    median_price_for_apartments_0_to_40_m2_zg,
    median_price_for_apartments_40_to_80_m2_zg,
    median_price_for_apartments_120_to_more_m2_zg,
    count_of_energy_class_a_plus,
    count_of_energy_class_a,
    count_of_energy_class_b,
    count_of_energy_class_c,
    count_of_energy_class_d,
    count_of_energy_class_e,
    count_of_energy_class_f,
    count_of_energy_class_g,
    count_of_update_price_per_day,
    count_of_update_price_increase_per_day,
    count_of_update_price_decrease_per_day
) VALUES ('{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'''

# Prepare tuple of values to fill in the query
data = (
    data_storage['date_of_reporting'],
    data_storage[COUNT_OF_APARTMENTS_BY_AGENCIES],
    data_storage[COUNT_OF_APARTMENTS_BY_PRIVATE_SELLER],
    data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_AGENCIES],
    data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_PRIVATE_SELLER],
    data_storage[MEDIAN_PRICE_FOR_APARTMENTS_0_TO_40_M2_ZG],
    data_storage[MEDIAN_PRICE_FOR_APARTMENTS_40_TO_80_M2_ZG],
    data_storage[MEDIAN_PRICE_FOR_APARTMENTS_120_TO_MORE_M2_ZG],
    data_storage[COUNT_OF_ENERGY_CLASS_A_PLUS],
    data_storage[COUNT_OF_ENERGY_CLASS_A],
    data_storage[COUNT_OF_ENERGY_CLASS_B],
    data_storage[COUNT_OF_ENERGY_CLASS_C],
    data_storage[COUNT_OF_ENERGY_CLASS_D],
    data_storage[COUNT_OF_ENERGY_CLASS_E],
    data_storage[COUNT_OF_ENERGY_CLASS_F],
    data_storage[COUNT_OF_ENERGY_CLASS_G],
    data_storage[COUNT_OF_UPDATE_PRICE_PER_DAY],
    data_storage[COUNT_OF_UPDATE_PRICE_INCREASE_PER_DAY],
    data_storage[COUNT_OF_UPDATE_PRICE_DECREASE_PER_DAY]
)

# Format the query with values and execute it
formatted_que = insert_que.format(*data)
update_insert_into_dest_base(formatted_que)
