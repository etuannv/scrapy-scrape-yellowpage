#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2018, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://webscrapingbox.com"
from pymysql.cursors import DictCursor
import pymysql
import sys
import os


def export_result(scraped_key, db_args, table_name):
    # delete previous file
    import glob
    for f in glob.glob("/var/lib/mysql/shoprite/*.csv"):
        print("Delete previous file: {}".format(f))
        os.remove(f)

    import socket
    host_name = socket.gethostname()
    result_file_name = scraped_key + '_' + host_name + '.csv'

    sqlconnect = pymysql.connect(**db_args)
    # Read from scrapper_urls
    try:
        with sqlconnect.cursor() as cursor:
            # The result file will be save at folder: /var/lib/mysql/shoprite/filename.csv
            sql = """SELECT * FROM {} 
                        WHERE scraped_key='{}' INTO OUTFILE '{}' 
                        FIELDS ENCLOSED BY '\"' TERMINATED BY ';' ESCAPED BY '\"' 
                        LINES TERMINATED BY '\r\n';""".format(table_name, scraped_key, result_file_name)
            result = cursor.execute(sql)
            # accept the change
            sqlconnect.commit()
            print("Finish {} records from table {}".format(result, table_name))
    finally:
        sqlconnect.close()
    
    full_path = os.path.join('/var/lib/mysql/shoprite', result_file_name)
    print("Result file path {}".format(full_path))
    return full_path



def main():
    db_args = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'yellowpage',
        'charset': 'utf8',
        'cursorclass': DictCursor
    }

    export_result('20190502', db_args, 'detail_item')
    
if __name__ == "__main__":
    main()