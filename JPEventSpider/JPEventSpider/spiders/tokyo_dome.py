import scrapy

class TokyoDome(scrapy.Spider):
    name = 'TokyoDome'
    allowed_domains = ['tokyo-dome.co.jp']
    start_urls =[
        'https://www.tokyo-dome.co.jp/dome/event/schedule.html'
    ]

    def parse(self,response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
