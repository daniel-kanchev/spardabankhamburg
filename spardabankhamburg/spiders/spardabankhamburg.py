import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from spardabankhamburg.items import Article


class SpardabankhamburgSpider(scrapy.Spider):
    name = 'spardabankhamburg'
    start_urls = ['https://www.sparda-bank-hamburg.de/ueber-uns/presse/pressemitteilungen/aktuelle-nachrichten.html']

    def parse(self, response):
        articles = response.xpath('//div[@class="acc-wrapper"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            date = ''
            title = article.xpath('./a/text()[last()]').get()
            if title:
                if title[:2].isnumeric():
                    title = title.split()
                    date = title.pop(0)
                    title.pop(0)
                    title = " ".join(title)
                else:
                    title = title.split()
                    date = title[:3]
                    title = title[4:]
                    title = " ".join(title)

            content = article.xpath('.//div[@class="acc-inner"]//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
