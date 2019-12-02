from pymysql.cursors import DictCursor
import pymysql
import sys

def clear_data(table_name):
    db_args = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'db': 'california_contractors',
            'charset': 'utf8',
            'cursorclass': DictCursor
        }
    sqlconnect = pymysql.connect(**db_args)
    # Read from scrapper_urls
    try:
        with sqlconnect.cursor() as cursor:
            # Read a single record
            sql = "DELETE FROM `{}` WHERE 1".format(table_name)
            result = cursor.execute(sql)
            # accept the change
            sqlconnect.commit()
            print("Delete {} records from table {}".format(result, table_name))
    finally:
        sqlconnect.close()




clear_data('backend_licenseclassification')
clear_data('backend_licensesale')
clear_data('backend_personnel')
clear_data('backend_saleperson')
clear_data('backend_bondcompany')
clear_data('backend_wccinfo')
clear_data('backend_classification')
clear_data('backend_license')