# -*- coding: utf-8 -*-
import re

import demjson
from scrapy_redis.spiders import RedisSpider

from tianqi.items import WeatherItem
from tianqi.spiders.tq_utills import get_date_list


class TqSpider(RedisSpider):
    name = 'tq'
    allowed_domains = ['tianqi.2345.com']
    start_url = ['http://tianqi.2345.com/js/citySelectData.js']

    def parse(self, response):
        '''
        城市对应城市编码解析
        '''
        city_select_data = re.findall(r'var prov=new Array.*?台湾-36\'.*?(.*?)var provqx',
                                      response.body.decode('gbk'), re.S)[0]
        city_select_data_list = re.findall("'(.*?)'", city_select_data, re.S)
        city_list = []
        code_list = []
        for city in city_select_data_list:
            result = city.split('|')

            city_data = []
            code_data = []
            for city_code in result:
                try:
                    city_code_data = city_code.split(' ')[1]
                    city_data.append(city_code_data.split('-')[0])
                    code_data.append(city_code_data.split('-')[1])
                    city_list += city_data
                    code_list += code_data
                except Exception:
                    continue
        # 得到city --> code 字典
        city_dict = dict(zip(city_list, code_list))
        # 开始构造请求
        # 2011-2016: http://tianqi.2345.com/t/wea_history/js/城市id_年月.js  其中年月格式为:年份+整数月份          比如 二零一零年一月份为：20111
        # 2017-未来：http://tianqi.2345.com/t/wea_history/js/年月/城市id_年月.js   其中 年月格式为 年份+带序号的月份 比如二零零七年一月份为：201701
        date = get_date_list()
        date_1 = date[:(2016 - 2011) * 12 + 12]
        date_2 = date[(2016 - 2011) * 12 + 12:]
        for city, code in city_dict.items():
            for date in date_1:
                api_data_1 = str(date.split('-')[0]) + str(int(date.split('-')[1]))
                api_1_url = 'http://tianqi.2345.com/t/wea_history/js/{}_{}.js'.format(code, api_data_1)
                request = response.follow(api_1_url, self.parse_weather)
                request.meta['city'] = city
                request.meta['code'] = code
                yield request
            for date in date_2:
                api_data_2 = str(date.split('-')[0]) + str(date.split('-')[1])
                api_2_url = 'http://tianqi.2345.com/t/wea_history/js/{}/{}_{}.js'.format(api_data_2, code, api_data_2)
                request = response.follow(api_2_url, self.parse_weather)
                request.meta['city'] = city
                request.meta['code'] = code
                yield request

    def parse_weather(self, response):
        '''
        解析每月份天气数据
        :param response:
        :return:
        '''
        data = WeatherItem()
        data['city'] = response.meta['city']
        data['city_code'] = response.meta['code']
        weather = response.body.decode('gbk')[16:-1]
        weather_dict = demjson.decode(weather)
        data['city'] = weather_dict.get('city')
        tqinfo_list = weather_dict.get('tqInfo')
        for tqinfo in tqinfo_list:
            if tqinfo:
                for key, value in tqinfo.items():
                    data[key] = value
                    if key == 'bWendu' or key == 'yWendu':
                        try:
                            data[key] = int(value[:-1])
                        except ValueError:
                            data[key] = ''
                yield data
