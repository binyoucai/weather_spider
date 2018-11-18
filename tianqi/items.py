# -*- coding: utf-8 -*-

import scrapy


class WeatherItem(scrapy.Item):
    table_name = 'weather'
    city = scrapy.Field()
    city_code = scrapy.Field()
    ymd = scrapy.Field()
    bWendu = scrapy.Field()
    yWendu = scrapy.Field()
    tianqi = scrapy.Field()
    fengxiang = scrapy.Field()
    fengli = scrapy.Field()
    aqi = scrapy.Field()
    aqiInfo = scrapy.Field()
    aqiLevel = scrapy.Field()
