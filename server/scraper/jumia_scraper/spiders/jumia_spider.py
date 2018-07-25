import scrapy

from ..items import ProductCategories, Products


class JumiaSpider(scrapy.Spider):
    name = "jumia"

    def start_requests(self):
        urls = [
            'https://www.jumia.co.ke/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for main_categories in response.css('#menuFixed ul.menu-items li.menu-item'):
            main = {
                'Main Category': main_categories.css('a.main-category span.nav-subTxt::text').extract_first(),
                'Main Category Link': main_categories.css('a.main-category::attr("href")').extract_first(),
                'categories': []
            }

            if main['Main Category'] is not None and main['Main Category Link'] is not None:
                yield scrapy.Request(main['Main Category Link'], callback=self.parse_product_list, meta={ 'category': main['Main Category'] })
        
            for categories in main_categories.css('div.navLayerWrapper div.submenu .column'):

                for sub_categories in categories.css('div.categories'):
                    category = {
                        'Category': sub_categories.css('.category::text').extract_first(),
                        'Category Link': sub_categories.css('a.category::attr("href")').extract_first(),
                        'Sub Categories': sub_categories.css('a.subcategory::text').extract(),
                        'Sub Category Links': sub_categories.css('a.subcategory::attr("href")').extract()
                    }

                    

                    if category['Category'] is not None and category['Category Link'] is not None:
                        yield scrapy.Request(category['Category Link'], callback=self.parse_product_list, meta={ 'category': category['Category'] })

                    for idx, sub in enumerate(category['Sub Categories']):
                        yield scrapy.Request(category['Sub Category Links'][idx], callback=self.parse_product_list, meta={ 'category': sub })

                    main['categories'].append(category)
            
            yield ProductCategories(main=main['Main Category'], main_link=main['Main Category Link'], categories=main['categories'])
    
    def parse_product_list(self, response):
        for product in response.css('section.products.-mabaya div.sku.-gallery'):
            data = {
                'sku': product.css('div.image-wrapper.default-state img::attr("data-sku")').extract_first(),
                'image_url': response.urljoin(product.css('div.image-wrapper.default-state img::attr("data-src")').extract_first()),
                'brand': product.css('a.link h2.title span.brand::text').extract_first(),
                'name': product.css('a.link h2.title span.name::text').extract_first(),
                'currency': product.css('a.link div.price-container.clearfix span.price-box.ri span.price span::attr("data-currency-iso")').extract_first(),
                'amount': product.css('a.link div.price-container.clearfix span.price-box.ri span.price span::attr("data-price")').extract_first()
            }

            product = Products(
                category=response.meta['category'],
                sku=data['sku'],
                image_url=response.urljoin(data['image_url']),
                brand=data['brand'],
                title=data['name'],
                currency=data['currency'],
                price=data['amount'],
            )

            # yield { 'image_urls': data['image_url'] }

            yield product

        for pages in response.css('section.pagination ul.osh-pagination li.item'):
            title = pages.css('a::attr("title")').extract_first()
            link = pages.css('a::attr("href")').extract_first()

            if title is not None and title.strip().lower() == 'next' and link is not None:
                yield response.follow(link, callback=self.parse_product_list, meta={ 'category': response.meta['category'] })
                # pass

    def parse_product(self, response):
        pass