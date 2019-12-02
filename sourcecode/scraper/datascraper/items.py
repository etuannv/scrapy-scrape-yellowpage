# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from w3lib.html import replace_escape_chars
import re

def removeMoneySymbol(value):
    """remove money symbol
    
    Arguments:
        value {string} -- input value
    
    Returns:
        string -- output value
    """
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",",".")
    return value

def getQuantity(value):
    """Get quantity in a string
    
    Arguments:
        value {string} -- input string
    
    Returns:
        string -- quantity
    """
    if value:
        value = str(value)
        value = re.findall(r'(\d+)', value, re.MULTILINE)
        if value:
            value = value[0]
            value = convertToInt(value)
        else:
            value = 0
    
    return value

def getMoney(value):
    """get money from a string
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- money
    """
    if value is not None:
        trim = re.compile(r'[^\d.,]+')
        value = trim.sub('', value)
        value = value.replace(",","")
        return convertToFloat(value)
    else:
        return value

def convertToInt(value):
    """convert to int
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- result
    """
    if value is None:
        return value
    try:
        return int(value)
    except ValueError:
        return None
        
def convertToFloat(value):
    """convert to float
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- result
    """
    if value is None:
        return value
    try:
        return float(value)
    except ValueError:
        return None

def processText(value):
    """process to get text, clean specifix character
    
    Arguments:
        value {string} -- input value
    
    Returns:
        string -- out put value
    """
    if value:
        value = replace_escape_chars(value)
        value = remove_tags(value)
        return value
    else:
        return ''

def processFloat(value):
    """process to get float value
    
    Arguments:
        value {string} -- input string
    
    Returns:
        float -- output value
    """
    if value:
        value = getMoney(value)
        return value
    else:
        return ''

def processInt(value):
    if value:
        value = getQuantity(value)
        return value
    else:
        return ''


def processMoney(value):
    """input_processor to extract money to float
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- return money in float
    """
    if value:
        value = getMoney(value)
        return value
    else:
        return ''

def processQuantity(value):
    """input_processor to get quantity from a string
    
    Arguments:
        value {string} -- Input value
    
    Returns:
        int -- quantity
    """
    if value:
        value = getQuantity(value)
        return value
    else:
        return ''

def processEmail(value):
    emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', value)
    if emails:
        for email in emails:
            if email not in emails:
                emails.append(email)
    return emails

class DetailItem(scrapy.Item):
    id = scrapy.Field()
    search_key = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    address_country = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    address_street = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    address_locality = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    address_region = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    postal_code = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    latitude = scrapy.Field(
        input_processor=MapCompose(processFloat),
        output_processor=TakeFirst()
    )
    longitude = scrapy.Field(
        input_processor=MapCompose(processFloat),
        output_processor=TakeFirst()
    )
    phone = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    website = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    image = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(processFloat),
        output_processor=TakeFirst()
    )
    no_of_reviews = scrapy.Field(
        input_processor=MapCompose(processFloat),
        output_processor=TakeFirst()
    )
    rank = scrapy.Field(
        input_processor=MapCompose(processInt),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=Join(', ')
    )
    email = scrapy.Field(
        input_processor=MapCompose(processText, processEmail),
        output_processor=TakeFirst()
    )
    opening_hours = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=Join(', ')
    )
    year_in_business = scrapy.Field(
        input_processor=MapCompose(processInt),
        output_processor=TakeFirst()
    )
    payment_method = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    general_info = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )
    services_products = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=Join(', ')
    )
    image = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )

    ref_url = scrapy.Field()
    created_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    created_by = scrapy.Field(
        output_processor=TakeFirst()
    )
    modified_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    modified_by = scrapy.Field(
        output_processor=TakeFirst()
    )
    scraped_key = scrapy.Field(
        output_processor=TakeFirst()
    )
    table_name = scrapy.Field(
        output_processor=TakeFirst()
    )