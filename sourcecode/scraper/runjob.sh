#!/bin/bash
echo "Run the price tracking scraper" 
cd /home/adtuan/scrapingbox/pricetracking/sourcecode/scraper/
nohup /home/adtuan/scrapingbox/pricetracking/sourcecode/scraper/scraper_env/bin/python3 runme.py &> /home/adtuan/scrapingbox/pricetracking/sourcecode/scraper/log.out &
 