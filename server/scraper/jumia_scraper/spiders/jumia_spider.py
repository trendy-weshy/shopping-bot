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

            main_category = main_categories.css('a.main-category span.nav-subTxt::text').extract_first()
            main_category_link = main_categories.css('a.main-category::attr("href")').extract_first()

            if main_category is not None or main_category_link is not None:
                yield ProductCategories(title=main_category.strip().lower(), link=main_category_link)

            if main_category is not None or main_category_link is not None:
                yield scrapy.Request(main_category_link, callback=self.parse_product_list, meta={'category': main_category.strip().lower()})
        
            for categories in main_categories.css('div.navLayerWrapper div.submenu .column'):

                for sub_categories in categories.css('div.categories'):
                    category = sub_categories.css('.category::text').extract_first()
                    category_link = sub_categories.css('a.category::attr("href")').extract_first()

                    if category is not None:
                        yield ProductCategories(
                            title=category.strip().lower(),
                            link=category_link,
                            parent=dict(
                                title=main_category.strip().lower(),
                                link=main_category_link
                            ) if main_category is not None or main_category_link is not None else None
                        )

                    sub_category_titles = sub_categories.css('a.subcategory::text').extract()
                    sub_category_links = sub_categories.css('a.subcategory::attr("href")').extract()

                    for idx, sub in enumerate(sub_category_titles):
                        yield ProductCategories(
                            title=sub.strip().lower(),
                            link=sub_category_links[idx],
                            parent=dict(
                                title=category,
                                link=category_link
                            ) if category is not None or category_link is not None else None
                        )

                    for idx, sub in enumerate(sub_category_titles):
                        yield scrapy.Request(sub_category_links[idx], callback=self.parse_product_list, meta={'category': sub.strip().lower()})

                    if category is not None or category_link is not None:
                        yield scrapy.Request(category_link, callback=self.parse_product_list, meta={'category': category.strip().lower()})
    
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