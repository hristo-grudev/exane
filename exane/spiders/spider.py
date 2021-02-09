import scrapy

from scrapy.loader import ItemLoader
from ..items import ExaneItem
from itemloaders.processors import TakeFirst


class ExaneSpider(scrapy.Spider):
	name = 'exane'
	start_urls = ['https://www.exane.com/corporate/news']

	def parse(self, response):
		articles = response.xpath('//div[@id="groupe_contenu"]/div[@style]/div[@id]')
		for article in articles:
			yield self.parse_post(response, article)

	def parse_post(self, response, article):
		data = article.xpath('./b/text()').get().replace('–', '-')
		date, title = data.split('-', 1)

		description = article.xpath('./p//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ExaneItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
