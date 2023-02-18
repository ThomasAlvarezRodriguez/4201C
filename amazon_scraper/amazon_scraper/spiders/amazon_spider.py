import scrapy

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    
    def start_requests(self):
        url = "https://https://www.amazon.com/s?k=flashlights+high+lumens&crid=227OY683AP3IM&sprefix=flashlights%2Caps%2C163&ref=nb_sb_ss_ts-doa-p_2_11"
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        for product in response.css("div.s-result-item"):
            yield {
                "title": product.css("h2.a-size-mini a::text").get(),
                "price": product.css("span.a-price span.a-offscreen::text").get(),
                "rating": product.css("span.a-icon-alt::text").get(),
                "url": product.css("h2.a-size-mini a::attr(href)").get()
            }
