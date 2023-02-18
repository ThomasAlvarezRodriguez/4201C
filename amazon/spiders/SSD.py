import json
import scrapy
from urllib.parse import urljoin
import re

class SSD(scrapy.Spider):
    name = "SDD"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def start_requests(self):
        keyword_list = ['SSD'] # Add your keywords here
        for keyword in keyword_list: 
            amazon_search_url = f'https://www.amazon.fr/s?k={keyword}&page=1' 
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page})
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            for page_num in available_pages:
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})


    def parse_product_data(self, response):
        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        if not price:
            price = response.css('.a-price .a-offscreen ::text').get("")
        yield {
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
            "rating_count": response.css("div[data-hook=total-review-count] ::text").get("").strip(),
            "asin": response.css("input#ASIN::attr(value)").get(""),
            "url": response.url,
        }