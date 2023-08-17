BASE_URL = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=260&sid1=101&date={}&page={}'

from pathlib import Path

import scrapy

from datetime import datetime, timedelta


class NaverNewsSpider(scrapy.Spider):
    name = "naver_news"

    def start_requests(self):
        urls = []
        date_today = datetime.now()
        for day in range(10):
            target_day = date_today - timedelta(days=day)
            #for page in range(1, 4):
            url=BASE_URL.format(target_day.strftime('%Y%m%d'),1)
            urls.append(url)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={
                'target_day' : target_day,
                'page': 1
            })
        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse, )

    def parse(self, response, target_day, page):
        description = response.css('.lede::text').get()
        print(target_day.strftime('%Y-%m-%d'), page, end='\t')
        print(description)
        if page == 10:
            return

        yield scrapy.Request(url=BASE_URL.format(target_day.strftime('%Y%m%d'),page+1), callback=self.parse, cb_kwargs={
                'target_day' : target_day,
                'page': page+1
            })