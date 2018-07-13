# coding: utf-8
import scrapy
from JPEventSpider.items import JpeventspiderItem


class TokyoDome(scrapy.Spider):
    name = 'TokyoDome'
    allowed_domains = ['tokyo-dome.co.jp']
    start_urls =[
        'https://www.tokyo-dome.co.jp/dome/event/schedule.html'
    ]

    def parse(self,response):
        item = JpeventspiderItem()

        event_date = []
        event_type = []
        event_name = []
        event_start = []

        # lambda function
        convertDateFunc  =lambda text:''.join(['-' if '\u4e00' <= char <= '\u9fff' else char for char in text ])

        month_body_sel = response.xpath('//div[contains(@class,"c-mod-tab__body")]')
        for body in month_body_sel:
            # get this month
            month_str = body.xpath('.//p[contains(@class,"c-ttl-set-calender")]/text()').extract()[0]
            month_str = convertDateFunc(month_str)

            # get each collection of event row
            this_month_event_row = body.xpath('.//tr[contains(@class,"c-mod-calender__item")]')
            for i, tab_body in enumerate(this_month_event_row):
                # judge whether event exist
                if tab_body.xpath('.//div[contains(@class,"c-mod-calender__detail-in")]/text()'):
                    # date
                    day_string = '%02d' % (i+1)
                    event_date.append(month_str+day_string)
                    print (day_string)
                    # type
                    event_type.append( tab_body.xpath('.//span[contains(@class,"c-txt-tag__item")]/text()').extract()[0] )
                    # name
                    name_sel = tab_body.xpath('.//p[contains(@class,"c-mod-calender__links")]')
                    name = ''
                    if len(name_sel.xpath('.//a')):
        #                 print ('have sub link')
                        name = name_sel.xpath('.//a/text()').extract()[0]
                        print (name)

                    else:
                        name = name_sel.xpath('./text()').extract()[0]
                        print (name)
                    event_name.append(name)
                    # start time
                    start_time_sel = tab_body.xpath('.//p[contains(@class,"c-txt-caption-01")]/text()').re(r'\d+:\d+')
                    if start_time_sel:
                        start_time = start_time_sel[1]
                    else:
                        start_time = ''
                    print (start_time)
                    event_start.append(start_time)

        item['name'] = event_name
        item['type'] = event_type
        item['start'] = event_start
        item['date'] = event_date
        yield item
