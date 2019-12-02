#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is spider which get license infomation from https://www2.cslb.ca.gov

"""

import scrapy
import sys, os

from scrapy.http import Request, FormRequest
from datascraper.items import DetailItem
import time
import datetime
import logging
import json
from pymysql.cursors import DictCursor
import pymysql
from urllib.parse import urljoin, quote_plus
import re
from hashlib import md5
from scrapy.loader import ItemLoader
from datascraper.common import readCsvToListDict

logger = logging.getLogger(__name__)


# === Start spider class ===
class YComSpider(scrapy.Spider):
    name = "y_com_spd"
    
    
    # Config table name
    detail_item = 'detail_item'
    

    # Config custom setting
    custom_settings = {
        'IS_STOP_REPORT'   : False,
        'MYSQL_TABLE'   : detail_item,
        # 'DOWNLOAD_TIMEOUT'   : 180,
        'ROTATING_PROXY_PAGE_RETRY_TIMES'   : 5,
        'RETRY_TIMES'   : 5,
        'HTTPERROR_ALLOWED_CODES': [],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 543,
            'datascraper.middlewares.RandomUserAgentMiddleware': 400,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':543,
        },
        'ROTATING_PROXY_BAN_POLICY':'datascraper.middlewares.MyDetectionPolicy',
        'ITEM_PIPELINES': {
            'datascraper.pipelines.MySQLPipeline': 100,
            # 'datascraper.pipelines.PrintPipeline': 200,
        },
    }

    # === Init function ===
    def __init__(self, scraped_key=None, *args, **kwargs):
        
        super(YComSpider, self).__init__(*args, **kwargs)
        if scraped_key is not None:
            self.scraped_key = scraped_key
        else:
            # Random key
            self.scraped_key = datetime.datetime.now().strftime("%Y%m%d")
    
    # === start request to scrape data ===

    def start_requests(self):
        """Start request data. 
        """
        # read csv file
        searchlist, header = readCsvToListDict('input.csv')
        
        for item in searchlist:
            logger.info("Get page: {} for city: {} with search key: {}".format(1, item['city'], item['search_key']))
            yield Request(
                item['url'],
                callback=self.parse_search,
                meta={
                    'city': item['city'],
                    'search_key': item['search_key'],
                    'page': 1,
                },
            )
    
    def parse_search(self, response):
        city = response.meta['city']
        search_key = response.meta['search_key']
        page = response.meta['page']
        
        jstring = re.findall(r'''json\"\>(\[.*])</script>''', response.text, re.MULTILINE)
        if not jstring:
            logger.info('Not found json data')
            return
        else:
            jstring = jstring[0]
        
        
        jdata = json.loads(jstring)
        search_items = response.xpath("//div[@class='search-results organic']/div[@class='result']//div[@class='info']")
        counter = 0
        for item, jitem in zip(search_items, jdata):
            counter +=1
            # import pdb; pdb.set_trace()
            link = item.xpath(".//h2/a/@href").extract_first()
            if link:
                link = urljoin('https://www.yellowpages.com', link)
            else:
                continue
            
            item_loader = ItemLoader(item=DetailItem(), response=response)
            id = md5((link).encode('utf-8')).hexdigest()
            item_loader.add_value('id', id)
            item_loader.add_value('search_key', search_key)
            item_loader.add_value('name', jitem['name'])
            try:
                item_loader.add_value('address_country', jitem['address']['addressCountry'])
            except:
                pass
            
            try:
                item_loader.add_value('address_street', jitem['address']['streetAddress'])
            except:
                pass
            
            try:
                item_loader.add_value('address_locality', jitem['address']['addressLocality'])
            except:
                pass
            
            try:
                item_loader.add_value('address_region', jitem['address']['addressRegion'])
            except:
                pass
            
            try:
                item_loader.add_value('postal_code', jitem['address']['postalCode'])
            except:
                pass
            
            try:
                item_loader.add_value('latitude', jitem['geo']['latitude'])
                item_loader.add_value('longitude', jitem['geo']['longitude'])
            except:
                pass
            
            try:
                item_loader.add_value('phone', jitem['telephone'])
                item_loader.add_value('website', jitem['url'])
                item_loader.add_value('image', jitem['image'])
            except:
                pass

            try:
                item_loader.add_value('rating', jitem['aggregateRating']['ratingValue'])
                item_loader.add_value('no_of_reviews', jitem['aggregateRating']['reviewCount'])
            except:
                pass
            
            
            item_loader.add_value('url', link)
            item_loader.add_xpath('category', ".//div[@class='categories']/a/text()")
            item_loader.add_value('rank', counter + (page-1)*30)
            
            # Other data
            item_loader.add_value('ref_url', response.url)
            item_loader.add_value('scraped_key', self.scraped_key)
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            item_loader.add_value('created_at', timestamp)
            item_loader.add_value('created_by', self.name)
            item_loader.add_value('modified_at', timestamp)
            item_loader.add_value('modified_by', self.name)
            item_loader.add_value('table_name', self.detail_item)
            
            # yield the result
            yield item_loader.load_item()

            # Request to get detail info
            yield Request(
                link,
                callback=self.parse_detail,
                meta={
                    'id': id
                }
            )

        # Check for next page
        next_page = response.xpath("//div[@class='pagination']/ul/li/a[contains(text(),'Next')]/@href").extract_first()
        if next_page:
            logger.info("Get page: {} for city: {} with search key: {}".format(page+1, city, search_key))
            yield Request(
                urljoin('https://www.yellowpages.com', next_page),
                callback=self.parse_search,
                meta={
                    'city': city,
                    'search_key': search_key,
                    'page': page+1,
                },
            )
    
    def parse_detail(self, response):
        id = response.meta['id']
        item_loader = ItemLoader(item=DetailItem(), response=response)
        item_loader.add_value('id', id)
        
        # category
        item_loader.add_xpath("category", "//dd[@class='categories']//a/text()")
        
        # opening_hours
        item_loader.add_xpath("opening_hours", "//time/@datetime")

        # email
        item_loader.add_xpath("email", "//a[@class='email-business']/@href")
        
        # year in bussines
        item_loader.add_xpath("year_in_business", "//div[@class='years-in-business']/div/div[@class='number']/text()")
        
        # Payment method
        item_loader.add_xpath("payment_method", ".//dd[@class='payment']/text()")
        
        # general_info
        item_loader.add_xpath("general_info", ".//dd[@class='general-info']/text()")
        
        # services_products
        item_loader.add_xpath("services_products", "//dt[contains(text(),'Services/Products')]//following-sibling::dd[1]/ul/li/text()")
            

        # Other data
        item_loader.add_value('ref_url', response.url)
        item_loader.add_value('scraped_key', self.scraped_key)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        item_loader.add_value('created_at', timestamp)
        item_loader.add_value('created_by', self.name)
        item_loader.add_value('modified_at', timestamp)
        item_loader.add_value('modified_by', self.name)
        item_loader.add_value('table_name', self.detail_item)
        
        yield item_loader.load_item()