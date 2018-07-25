from . import api
import datetime
from flask import jsonify, request, abort
from flask_cors import cross_origin
from ..models import ProductCategory, Product
from mongoengine import NotUniqueError


@api.after_request
def apply_caching(response):
    response.headers["Content-type"] = "application/json"
    return response


@api.route("/ping")
@cross_origin()
def ping_api():
    return jsonify(time=datetime.datetime.now())


@api.route("/categories")
def product_categories():
    if request.method == 'GET':
        categories = ProductCategory.objects()
        return jsonify(categories)

    if request.method == 'POST':
        req_data = request.get_json()

        parent_category = req_data['parent'] if 'parent' in req_data else None
        category = req_data['category'] if 'category' in req_data else None

        try:

            if parent_category is not None:
                get_parent_category = ProductCategory.objects.get(title=parent_category.title)

                new_category = ProductCategory(title=category.title, link=category.link)
                new_category.save()

                get_parent_category.update(push__sub_categories=new_category)
            else:
                new_category = ProductCategory(title=category.title, link=category.link)
                new_category.save()

            return jsonify(new_category)
        except get_parent_category.DoesNotExist:
            new_parent_category = ProductCategory(title=parent_category.title, link=parent_category.link)
            new_parent_category.save()

            new_category = ProductCategory(title=category.title, link=category.link)
            new_category.save()

            new_parent_category.update(push__sub_categories=new_category)

            return jsonify({
                'parent': new_parent_category,
                'category': new_category
            })
        except NotUniqueError:
            abort(406, 'Category seems to already been.', name='DuplicateRecord')
        except:
            abort(500, 'Could not finish processing request', name='CorruptRequest')


@api.route('/products')
def save_product():
    if request.method == 'GET':
        products = Product.objects()
        return jsonify(products)

    if request.method == 'POST':
        req_data = request.get_json()

        try:
            category = ProductCategory.objects.get(title=req_data["category"])
        except category.DoesNotExist:
            abort(404, "Category not found", name="MissingCategory")

        try:
            product = Product.create_or_update(
                req_data["title"],
                req_data["sku"],
                category,
                req_data["price"],
                req_data["currency"],
                product_image=req_data["image_url"] if "image_url" in req_data else None,
                brand=req_data["brand"] if "brand" in req_data else None,
            )

            return jsonify(product)
        except:
            abort(500, 'Could not finish processing request', name='CorruptRequest')
