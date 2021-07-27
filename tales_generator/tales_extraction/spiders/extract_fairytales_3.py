import scrapy

class FairytalesExtractor(scrapy.Spider):
    name = 'fairytales3'

    def start_requests(self):
        urls = ['https://dobrye-skazki.ru/korotkie-skazki/',
               'https://dobrye-skazki.ru/korotkie-skazki/page/2/',
               'https://dobrye-skazki.ru/korotkie-skazki/page/3/',
        'https://dobrye-skazki.ru/korotkie-skazki/page/4/',
        'https://dobrye-skazki.ru/korotkie-skazki/page/5/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for x in response.css('article'):
            link = x.css('a::attr(href)').get()
            yield scrapy.Request(link, callback=self.parse_link)

    def parse_link(self, link):
        name = link.css('h1::text').get()
        text = ' '.join(link.css('div.entry p').getall())

        with open('fairytales3.txt', 'a', encoding='utf-8') as outp:
                outp.write('<title>{}</title>'.format(name) + '\n' + text.strip() + '\n\n')