import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from func.my_library_function import origin_db
from func.my_library_function import dest_db
from func.my_library_function import get_latest_data_by_city
from func.my_library_function import update_insert_table_with_latest_data

from psycopg2.extras import RealDictCursor  



cursor = origin_db(cursor_factory_param=RealDictCursor)
cur  = dest_db(cursor_factory_param=RealDictCursor)

latest_data = get_latest_data_by_city(cursor, 'Grad Zagreb')
print('Latest data fetched:', len(latest_data))

update_insert_table_with_latest_data(latest_data, cur, cursor)


