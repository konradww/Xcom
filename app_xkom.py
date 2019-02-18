#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import json
import os.path
import pyodbc
import re
import datetime

date = datetime.datetime.now()

def open_json(name_file):
    if os.path.isfile(name_file):
        with open(name_file) as data_file:
            data_loaded = json.load(data_file)
        return data_loaded
    else:
        print("File doesn't exist")
        return 0

link = open_json('data.json')
page_response = requests.get(link['page_link'], timeout=5)
# parse html
page_content = BeautifulSoup(page_response.content, "html.parser")

def convert_price(price):
    if price != None or price != '':
        price = price.strip().replace(',', '.').replace(' ', '')
        return float((re.match(r'\d*.\d*', price)).group())
    else:
        return 0

ProductDict = {
    'productName': (page_content.find(class_='product-name')).text,
    'oldPrice': convert_price((page_content.find(class_='old-price')).text),
    'newPrice': convert_price((page_content.find(class_='new-price')).text),
    'ProductDiscount': (page_content.find(class_='discount-tip-value center-block')).text,
    'ProductBefore_count': (page_content.find(class_='pull-left')).text,
    'ProductAfter_count': (page_content.find(class_='pull-right')).text
}
for k, v in ProductDict.items():
    print(k, v)


try:
    db = open_json('data_DB.json')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
                          'SERVER=' + db['server']
                          + ';PORT=1443;DATABASE='
                          + db['database']
                          + ';UID=' + db['username']
                          + ';PWD=' + db['password'])
    print('Opened connection to Database ')
    try:
        cursor = cnxn.cursor()
        # question = ("BEGIN TRAN "
        #             "IF NOT EXISTS "
        #             "(SELECT * FROM dbo.Product)"
        #             " COMMIT")
        question = ("BEGIN TRAN "
                    "IF NOT EXISTS (SELECT * FROM [XCOM].[dbo].[Product]  "
                    "WHERE ([ProductName] like '%s' and YEAR(Data) = %i and MONTH(Data) = %i and DAY(Data) = %i))"
                    "   INSERT INTO Product"
                    "       (ProductName,  ProductDiscount, ProductOld_price, ProductNew_price, "
                    "       ProductBefore_count, ProductAfter_count)"
                    "   VALUES ('%s',%f, %f, %f, %i, %i ) "
                    "COMMIT") % (ProductDict['productName'], date.year, date.month, date.day,
                                 ProductDict['productName'], ProductDict['oldPrice'] - ProductDict['newPrice'],
                                 ProductDict['oldPrice'], ProductDict['newPrice'], 0, 0)
        cursor.execute(question)
        cursor.commit()

        # question = ("BEGIN TRAN "
        #             "(SELECT * FROM dbo.Product with (updlock, rowlock, holdlock) where ProductName= '%s') "
        #             "COMMIT") % (ProductDict['productName'])
        # cursor.execute(question)
        # cursor.commit()
    except:
        print('query filed')
        raise
    finally:
        cnxn.close()
        print('Closed connection to Database.')
except Exception as e:
    print('Something went wrong:', e)





