#to run
#scrapy crawl imdb_spider -o movies.csv

import scrapy 
class ImdbSpider(scrapy.Spider):
	name = 'imdb_spider'

	start_urls = ['https://www.imdb.com/title/tt1160419/']

	def parse(self,response):
		"""
		assumes you start on a movie page, navigate to Cast & Crew page
		once at <movie_url>fullcredits, call parse_full_Credits method in the callback argument 
		to a yielded scrapy.Request. returns nothing, around 5 lines of code
		"""
		#gets link to cast and crew from start page 
		cast_crew = response.css("a[href^= 'fullcredits']").attrib["href"] 
		if cast_crew:
			#joins link to existing link
			cast_crew = response.urljoin(cast_crew)

			#yields request: if this page exists, navigate to it and perform whatever function is described in the callback argument
			yield scrapy.Request(cast_crew, callback = self.parse_full_credits)

		
	def parse_full_credits(self,response):
		"""
		assumes you start on cast and crew page 
		yields a scraoy.Request for the page of each actor listed on parse_actor_page
		No crew, just actors 
		returns nothing, around 5 lines of code
		"""

		#below code gathers a list of urls for actors from cast page
		cast_list = [a.attrib["href"] for a in response.css("td.primary_photo a")] 
		for actor in cast_list:
			#for each actors url in the list, join it to the existing response url
			actor_page = response.urljoin(actor)
			#for each actor, yield a request: go to new response url, and perform parse_actor_page function
			yield scrapy.Request(actor_page, callback = self.parse_actor_page)


	def parse_actor_page(self,response):
		"""
		start on the page of an actor, yields a dictionary of form {"actor": actor_name, "movie_or_TV_name": movie_or_TV_name}
		should yield one such dict for each of the movies or tv shows on which the actor has worked.Name has to be determined of the actor 
		and each movie or tv show 
		no more than 15 lines of code 
		"""
		#retrieve actor name from header
		actor = response.css("h1.header span.itemprop::text").get()

		#get list of movies actor was involved with
		movies = response.css("div.filmo-row")
		for movie in movies:
			#see how the actor contributed to the movie, we are interested only in acting credits
			role = movie.css("::attr(id)").get()[0:3] 
			if(role == 'act'): #to account for 'ACT'or and 'ACT'ress 
				yield{
					"actor":actor, #specified above 
					"movie_or_TV_name": movie.css("a::text").get() #get movie title
				}
