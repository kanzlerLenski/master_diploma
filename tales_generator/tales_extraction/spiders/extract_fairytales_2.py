import scrapy

class FairytalesExtractor(scrapy.Spider):
    name = 'fairytales2'

    def start_requests(self):
        url = 'file:///C:/Users/Eugene/Desktop/%D0%9A%D0%BE%D1%80%D0%BE%D1%82%D0%BA%D0%B8%D0%B5%20%D1%81%D0%BA%D0%B0%D0%B7%D0%BA%D0%B8%20-%20%D1%87%D0%B8%D1%82%D0%B0%D1%82%D1%8C%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD.html'
        #url = 'https://nukadeti.ru/skazki/korotkie#'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for x in response.css('li.st-bl'):
            #link = 'https://nukadeti.ru{}'.format(x.css('div.main-box a::attr(href)').get())
            link = x.css('div.main-box a::attr(href)').get()
            yield scrapy.Request(link, callback=self.parse_link)

    def parse_link(self, link):
        name = link.css('h1::text').get()
        text = ' '.join(link.css('div.tale-text.si-text p::text').getall())

        with open('fairytales2.txt', 'a', encoding='utf-8') as outp:
                outp.write('<title>{}</title>'.format(name) + '\n' + text.strip() + '\n\n')