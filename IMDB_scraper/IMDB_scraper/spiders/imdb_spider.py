#to run
#scrapy crawl imdb_spider -o movies.csv

import scrapy 
class ImdbSPIDEr(scrapy.Spider):
	name = 'imdb_spider'

	start_urls = ['https://www.imdb.com/title/tt1160419/']

	def parse(self,response):
		"""
		assumes you start on a movie page, navigate to Cast & Crew page
		once at <movie_url>fullcredits, call parse_full_Credits method in the callback argument 
		to a yielded scrapy.Request. returns nothing, around 5 lines of code
		"""
		
	def parse_full_credits(self,response):
		"""
		assumes you start on cast and crew page 
		yields a scraoy.Request for the page of each actor listed on parse_actor_page
		No crew, just actors 
		returns nothing, around 5 lines of code
		"""

	def parse_actor_page(self,response):
		return null 