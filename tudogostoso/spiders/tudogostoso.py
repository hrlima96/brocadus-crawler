# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Spider
from scrapy.loader import ItemLoader
from ..items import Recipe
import re

class TudogostosoSpider(Spider):
    name = "tudogostoso"
    allowed_domains = ["tudogostoso.com.br"]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}

    def start_requests(self):
        yield Request("http://www.tudogostoso.com.br/", callback=self.initial_url, headers=self.headers)

    def initial_url(self, response):
        for href in response.xpath("//div[contains(@class, 'menu')]/nav/ul/li/a/@href"):
            href_text = href.extract()
            if href_text not in ["/videos.php", "/especiais/15-chefs-tudo-gostoso", "/categorias/sopas.php"]:
                yield Request(response.urljoin(href.extract()), callback=self.categories_urls, headers=self.headers)

    def categories_urls(self, response):
        all_recipes_link = response.xpath("//div[contains(@class, 'submenu')]/ul/li/a/@href")[0].extract()
        yield Request(response.urljoin(all_recipes_link), callback=self.all_recipes_urls, headers=self.headers)

    def all_recipes_urls(self, response):
        href_list = response.xpath("//div/a[contains(@class, 'next')]/@href")
        if href_list:
            yield Request(response.urljoin(href_list[0].extract()), callback=self.all_recipes_urls, headers=self.headers)

        for href in response.xpath("//ul[contains(@class, 'clearfix')]/li/a/@href"):
            yield Request(response.urljoin(href.extract()), callback=self.recipe_parse, headers=self.headers)


    def recipe_parse(self, response):
      l = ItemLoader(item=Recipe(), response = response)
      l.add_xpath('name', '//h1[@itemprop="name"]')
      l.add_xpath('image_url', '//img[@itemprop="image"]/@src')
      l.add_xpath('time_to_prepare', '//time[@itemprop="totalTime"]')
      l.add_xpath('recipe_yield', '//data[@itemprop="recipeYield"]')
      l.add_xpath('ingredients', '//span[@itemprop="recipeIngredient"]')
      l.add_xpath('instructions', '//div[@itemprop="recipeInstructions"]/ol/li/span')

      return l.load_item()
