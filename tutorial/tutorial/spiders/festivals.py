# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scrapy


class FestivalSpider(scrapy.Spider):

    name = 'music_festivals'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.musicfestivalwizard.com/festival-guide/us-festivals/',
        'https://www.musicfestivalwizard.com/festival-guide/canada-festivals/'
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        festival_links = response.xpath('//span[@class="festivaltitle"]/a/@href').extract()
        festival_names = response.xpath('//span[@class="festivaltitle"]/a/text()').extract()
        
        for i in range(len(festival_links)):
            yield scrapy.Request(
                url=festival_links[i],
                callback=self.parse_festival,
                meta={'url': festival_links[i], 'name': festival_names[i]}
            )


        # Follow pagination links and repeat
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()


        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_festival(self, response):
        
        name = response.request.meta['name']
        
        url = response.request.meta['url']

        location = (
            response.xpath('//div[@id="festival-basics"]/text()').extract()[3])

        dates = (
            response.xpath('//div[@id="festival-basics"]/text()').extract()[5])


        website = (
            response.xpath(
                '//div[@id="festival-basics"]/a/@href').extract_first()
        )

        logo = (
            response.xpath(
                '//div[@id="festival-basics"]/img/@src').extract()[0]
        )

        lineup = (
            response.xpath(
                '//div[@class="lineupguide"]/ul/li/text()').extract() +
            response.xpath(
                '//div[@class="lineupguide"]/ul/li/a/text()').extract()
        )

        yield {
            'url': url,
            'name': name,
            'location': location,
            'dates': dates,
            'website': website,
            'logo': logo,
            'lineup': lineup
        }

