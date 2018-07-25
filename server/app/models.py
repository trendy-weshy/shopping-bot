import datetime
from . import db
from mongoengine import *
from mongoengine import signals


class ProductCategory(db.DynamicDocument):
    title = StringField(required=True, unique=True)
    link = URLField(required=False)
    sub_categories = ListField(ReferenceField('self'), unique=True, default=[])
    added_on = DateTimeField(default=datetime.datetime.now)
    modified_on = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'ProductCategories',
        'ordering': ['-modified_on']
    }


ProductCategory.register_delete_rule(ProductCategory, 'sub_categories', PULL)


class ProductBrand(db.Document):
    title = StringField(required=True, unique=True)


class Product(db.DynamicDocument):
    title = StringField(required=True)
    sku = StringField(required=True, unique=True)
    category = ReferenceField(ProductCategory, required=True)
    price = IntField(required=True)
    currency = StringField(max_length=3, required=True)
    added_on = DateTimeField(default=datetime.datetime.now)
    modified_on = DateTimeField(default=datetime.datetime.now)
    product_image = URLField(required=False)
    brand = ReferenceField(ProductBrand, required=False)

    meta = {
        'collection': 'ProductCategories',
        'indexes': [
            {
                'fields': ['$title'],
                'default_language': 'english',
                'weights': { 'title': 6 }
            },
            ('currency', '-price')
        ],
        'ordering': ['-price', '-modified_on'],

    }


    @staticmethod
    def create_or_update(title, sku, category, price, currency, product_image=None, brand=None):
        product_brand = None

        if brand is not None:
            try:
                product_brand = ProductBrand.objects.get(title=brand)
            except product_brand.DoesNotExist:
                product_brand = ProductBrand(title=brand)
                product_brand.save()

        try:
            product = Product.objects.get(sku=sku)
            product.update(
                title=title,
                sku=sku,
                category=category,
                price=price,
                currency=currency,
                product_image=product_image,
                brand=product_brand
            )
            return product
        except DoesNotExist:
            product = Product(
                title=title,
                sku=sku,
                category=category,
                price=price,
                currency=currency,
                product_image=product_image,
                brand=product_brand
            )
            product.save()

            return product


def update_modified(sender, document):
    document.modified_on = datetime.datetime.utcnow()


signals.pre_save.connect(update_modified)
