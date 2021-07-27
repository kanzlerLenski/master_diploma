import scrapy

class FairytalesExtractor(scrapy.Spider):
    name = 'fairytales4'

    def start_requests(self):
        urls = ['https://mishka-knizhka.ru/skazki-dlay-detey/']

        for i in range (2,41):
            s = 'https://mishka-knizhka.ru/skazki-dlay-detey/page/{}/'.format(str(i))
            urls.append(s)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for x in response.css('article'):
            try:
                temp = str(x.css('div.duration span').get()).split()
                if int(temp[0][6:]) <= 10 and 'ч' not in temp[1]:
                    link = x.css('a::attr(href)').get()
                    yield scrapy.Request(link, callback=self.parse_link)
            except ValueError:
                continue

    def parse_link(self, link):
        name = str(link.css('h1::text').get()).split(' — ')[0]
        text = ' '.join(link.css('div.entry-content p::text').getall()[1:]).replace('<p>', '').replace('</p>', '')

        with open('fairytales4.txt', 'a', encoding='utf-8') as outp:
                outp.write('<title>{}</title>'.format(name) + '\n' + text.strip() + '\n\n')