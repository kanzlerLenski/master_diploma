import scrapy

class FairytalesExtractor(scrapy.Spider):
    name = 'fairytales'

    def start_requests(self):
        url = 'https://deti-online.com/skazki/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for x in response.css('tr'):
            try:
                if int(x.css('td:nth-child(3)::attr(data-filter)').get()) == 0:
                    link = x.css('a.dt-a::attr(href)').get()
                    yield scrapy.Request(link, callback=self.parse_link)
            except TypeError:
                continue

    def parse_link(self, link):
        name = ' '.join(str((link.css('h1::text').get())).split()[1:])
        text = ' '.join(link.css('div.text p::text').getall())

        with open('fairytales.txt', 'a', encoding='utf-8') as outp:
                outp.write('<title>{}</title>'.format(name) + '\n' + text.strip() + '\n\n')




