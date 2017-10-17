# -*- coding: utf-8 -*-
from scrapy import Item
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import re

def remove_letters(value):
    return int(re.sub(r"[^0-9]", "", value))

class Recipe(Item):
    name = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )

    image_url = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )

    time_to_prepare = Field(
        input_processor=MapCompose(remove_tags, remove_letters),
        output_processor=TakeFirst()
    )

    recipe_yield = Field(
        input_processor=MapCompose(remove_tags, remove_letters),
        output_processor=TakeFirst()
    )

    ingredients = Field(
        input_processor=MapCompose(remove_tags)
    )

    instructions = Field(
        input_processor=MapCompose(remove_tags)
    )
