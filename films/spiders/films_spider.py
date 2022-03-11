import scrapy
import re

class FilmsSpiderSpider(scrapy.Spider):
    name = 'films_spider'
    allowed_domains = ['88-films.myshopify.com']
    start_urls = ['http://88-films.myshopify.com/']


    def start_requests(self):
        for page in range(1,8):
            yield scrapy.Request(
                "https://88-films.myshopify.com/collections/blu-ray-version?page=" + str(page),callback=self.extract_link_first
                                )
    
    def extract_link_first(self,response):
        results = response.css('.product-image>a::attr(href)').getall()
        yield from response.follow_all(results,callback = self.parse)

    def delete_join(self,arr):
        de = map(lambda x:re.sub("[\r\n\t(\xa0)]","",x),arr)
        fi = filter(lambda y:y != '',de)
        delimiter = " "
        return delimiter.join(fi)

    def parse(self, response):
        title = response.css('.title>h1::text').get()
        price = re.sub("[\r\n\t\s(\xa0)]","",response.css('#productPrice::text').get())
        content = self.delete_join(response.css('.li2 *::text').getall())
        if(content == ''):
            content = self.delete_join(response.css('.column>ul *::text').getall())
            if(content == ''):
                content = self.delete_join(response.css('.rte>div')[8].css('li *::text').getall())
        
        yield {
                'url':response.url,
                'title':title,
                'price':price,
                'content': content
                }
