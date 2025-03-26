import sys
import os
import pandas as pd

from psycopg2.extras import RealDictCursor  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from func.my_library_function import dest_db

cursor=dest_db(cursor_factory_param=RealDictCursor)


data_storage = {}
COUNT_OF_APARTMENTS_BY_AGENCIES="count_of_apartaments_by_agencies"
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

query_for_agencies="""SELECT *
FROM zagreb_app z
WHERE NOT EXISTS
(SELECT *
FROM
(SELECT * 
FROM zagreb_app
where author not ilike '%nekretnine%' 
and author not ilike '%nekretnina%'
and author not ilike '%d.o.o%' 
and author not ilike '%real%' 
and author not ilike '%Immobilien%' 
and author not ilike '%properties%'
and author not ilike '%agencija%'
and author not ilike '%projekt%'
and author not ilike '%www%'
and LEFT(author, 1) != UPPER(LEFT(author, 1))) as consumeri
where consumeri.author = z.author) 
and author !~ '\d+$' 
and author !~ '^[^A-Za-z0-9]'
ORDER BY author"""

cursor.execute(query_for_agencies)
result_agency_set=cursor.fetchall()

df_agency=pd.DataFrame(data=result_agency_set)

data_storage[COUNT_OF_APARTMENTS_BY_AGENCIES] = int(df_agency['njuskalo_id'].count())
data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_AGENCIES] = float(df_agency['Cijena'].median())


query_for_private_per= ''' SELECT * 
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
result_private_per_set=cursor.fetchall()

df_private=pd.DataFrame(data=result_private_per_set)

data_storage[COUNT_OF_APARTMENTS_BY_PRIVATE_SELLER] = int(df_private['njuskalo_id'].count())
data_storage[MEDIAN_PRICE_OF_APARTMENTS_BY_PRIVATE_SELLER] = float(df_private['Cijena'].median())



query_for_zagreb_apartmets = '''SELECT * FROM zagreb_app'''

cursor.execute(query_for_zagreb_apartmets)
result_zagreb_set = cursor.fetchall()

df_zagreb = pd.DataFrame(data=result_zagreb_set)

df_zagreb

filtered_data_0_40 = df_zagreb[(df_zagreb['Stambena povrsina'] > 0) & (df_zagreb['Stambena povrsina'] < 40)]
filtered_data_40_80 = df_zagreb[(df_zagreb['Stambena povrsina'] > 40) & (df_zagreb['Stambena povrsina'] < 80)]
filtered_data_80_120 = df_zagreb[(df_zagreb['Stambena povrsina'] > 80) & (df_zagreb['Stambena povrsina'] < 120)]
filtered_data_120_more = df_zagreb[(df_zagreb['Stambena povrsina'] > 120)]

data_storage[MEDIAN_PRICE_FOR_APARTMENTS_0_TO_40_M2_ZG] = float(filtered_data_0_40['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_40_TO_80_M2_ZG] = float(filtered_data_40_80['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_80_TO_120_M2_ZG] = float(filtered_data_80_120['Cijena'].median())
data_storage[MEDIAN_PRICE_FOR_APARTMENTS_120_TO_MORE_M2_ZG] = float(filtered_data_120_more['Cijena'].median())



count_a_plus = df_zagreb['Energetski razred'].value_counts().get('A+', 0)
count_a = df_zagreb['Energetski razred'].value_counts().get('A', 0)
count_b = df_zagreb['Energetski razred'].value_counts().get('B', 0)
count_c = df_zagreb['Energetski razred'].value_counts().get('C', 0)
count_d = df_zagreb['Energetski razred'].value_counts().get('D', 0)
count_e = df_zagreb['Energetski razred'].value_counts().get('E', 0)
count_f = df_zagreb['Energetski razred'].value_counts().get('F', 0)
count_g = df_zagreb['Energetski razred'].value_counts().get('G', 0)

data_storage[COUNT_OF_ENERGY_CLASS_A_PLUS] = int(count_a_plus)
data_storage[COUNT_OF_ENERGY_CLASS_A] = int(count_a)
data_storage[COUNT_OF_ENERGY_CLASS_B] = int(count_b)
data_storage[COUNT_OF_ENERGY_CLASS_C] = int(count_c)
data_storage[COUNT_OF_ENERGY_CLASS_D] = int(count_d)
data_storage[COUNT_OF_ENERGY_CLASS_E] = int(count_e)
data_storage[COUNT_OF_ENERGY_CLASS_F] = int(count_f)
data_storage[COUNT_OF_ENERGY_CLASS_G] = int(count_g)



print(data_storage)