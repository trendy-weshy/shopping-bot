from . import api
import datetime
from flask import jsonify, request
from flask_cors import cross_origin
from ..models import ProductCategory, Product
from mongoengine import errors


@api.after_request
def apply_caching(response):
    response.headers["Content-type"] = "application/json"
    return response


@api.route("/ping")
@cross_origin()
def ping_api():
    return jsonify(time=datetime.datetime.now())


@api.route("/categories/", methods=['POST', 'GET'])
def product_categories():
    if request.method == 'GET':
        categories = ProductCategory.objects()
        return jsonify(categories)

    if request.method == 'POST':
        req_data = request.get_json()

        parent_category = req_data['parent_category'] if 'parent_category' in req_data and req_data['parent_category'] is not None else None
        category = req_data['category'] if 'category' in req_data else None

        try:

            if parent_category is not None:
                get_parent_category = ProductCategory.objects.get(title=parent_category['title'].strip().lower())

                new_category = ProductCategory(title=category['title'].strip().lower(), link=category['link'])
                new_category.save()

                get_parent_category.update(add_to_set__sub_categories=new_category)

                return jsonify(new_category)
            else:
                new_category = ProductCategory(title=category['title'].strip().lower(), link=category['link'])
                new_category.save()

                return jsonify(new_category)
        except errors.DoesNotExist:
            new_parent_category = ProductCategory(title=parent_category['title'].strip().lower(), link=parent_category['link'])
            new_parent_category.save()

            new_category = ProductCategory(title=category['title'].strip().lower(), link=category['link'])
            new_category.save()

            ProductCategory.objects.get(title=parent_category['title'].strip().lower()).update(add_to_set__sub_categories=new_category)

            return jsonify({
                'parent': new_parent_category,
                'category': new_category
            })
        except errors.NotUniqueError:
            return jsonify(msg='Category seems to already been added', name='DuplicateRecord'), 406
        except:
            return jsonify(msg='Could not finish processing request', name='CorruptRequest'), 500


@api.route('/products/', methods=['POST', 'GET'])
def save_product():
    if request.method == 'GET':
        products = Product.objects()
        return jsonify(products)

    if request.method == 'POST':
        req_data = request.get_json()

        try:
            category = ProductCategory.objects.get(title=req_data["category"].strip().lower())
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
        except errors.DoesNotExist:
            return jsonify(msg="Product Category not found", name="MissingCategory"), 404
        except Exception as e:
            print(e)
            return jsonify(msg='Could not finish processing request', name='CorruptRequest'), 500
