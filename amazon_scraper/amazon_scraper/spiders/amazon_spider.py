import scrapy

class SSDSpider(scrapy.Spider):
    name = "ssd"
    start_urls = [
        "https://www.amazon.com/s?k=ssd"
    ]

    def parse(self, response):
        for product in response.css("div.s-result-item"):
            yield {
                "title": product.css("h2.a-size-mini a::text").get(),
                "price": product.css("span.a-price span.a-offscreen::text").get(),
                "brand": product.css("div.a-section.a-text-left span.a-text-bold:contains('Brand') + span::text").get(),
                "read_speed": product.css("div.a-section.a-text-left span.a-text-bold:contains('Read Speed') + span::text").get(),
                "write_speed": product.css("div.a-section.a-text-left span.a-text-bold:contains('Write Speed') + span::text").get(),
                "form_factor": product.css("div.a-section.a-text-left span.a-text-bold:contains('Form Factor') + span::text").get(),
                "interface": product.css("div.a-section.a-text-left span.a-text-bold:contains('Interface') + span::text").get(),
                "cache": product.css("div.a-section.a-text-left span.a-text-bold:contains('Cache') + span::text").get(),
                "url": product.css("h2.a-size-mini a::attr(href)").get()
            }

        next_page = response.css("div.s-pagination-container a.s-pagination-next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
