import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from func.my_library_function import leno_baza
from func.my_library_function import vale_baza
from func.my_library_function import update_insert_vale_base
from func.my_library_function import get_lates_data_by_city
from func.my_library_function import update_insert_table_with_lates_data

from psycopg2.extras import RealDictCursor  



cursor = leno_baza(cursor_factory_param=RealDictCursor)
cur  = vale_baza(cursor_factory_param=RealDictCursor)

lates = get_lates_data_by_city(leno_baza(cursor_factory_param=RealDictCursor), 'Grad Zagreb')

update_insert_table_with_lates_data(lates, cur, cursor)


