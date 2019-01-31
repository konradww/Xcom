#!/usr/bin/python
from bs4 import BeautifulSoup
import requests

page_link = 'https://www.x-kom.pl'

ProductDict = {}
page_response = requests.get(page_link, timeout=5)
# parse html
page_content = BeautifulSoup(page_response.content, "html.parser")

# name product
# productName = page_content.find(class_='product-name')
# oldPrice = page_content.find(class_='old-price')
# newPrice = page_content.find(class_='new-price')
# ProductDiscount = page_content.find(class_='discount-tip-value center-block')
# ProductBefore_count = page_content.find(class_='pull-left')
# ProductAfter_count = page_content.find(class_='pull-right')

ProductDict = {
    'productName': page_content.find(class_='product-name'),
    'oldPrice': page_content.find(class_='old-price'),
    'newPrice': page_content.find(class_='new-price'),
    'ProductDiscount': page_content.find(class_='discount-tip-value center-block'),
    'ProductBefore_count': page_content.find(class_='pull-left'),
    'ProductAfter_count': page_content.find(class_='pull-right')
}

for k, v in ProductDict.items():
    print(v)

# print(productName)
# print(oldPrice)
# print(newPrice)
# print (ProductDiscount)
# print(ProductBefore_count)
# print(ProductAfter_count)

