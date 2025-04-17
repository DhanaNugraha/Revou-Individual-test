from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.product import create_product_repo, process_sustainability_repo, process_tags_repo
from schemas.product import ProductCreateRequest, ProductCreatedResponse

def create_product_view(user, product_request):
    if not user.is_vendor:
        return jsonify({"message": "User is not a vendor", "success": False, "location": "view create product vendor validation"}), 403
    
    try:
        product_data_validated = ProductCreateRequest.model_validate(product_request)

        # flush product and get product id
        product = create_product_repo(product_data_validated, user.id)

        # add new tags to tags table and append relationship of product to tags
        process_tags_repo(product_data_validated.tags, product)

        # add new sustainability attributes to sustainability_attributes table and append relationship of product to sustainability attributes
        process_sustainability_repo(product_data_validated.sustainability_attributes, product)

        db.session.commit()

        return jsonify({"message": "Product created successfully", "product": ProductCreatedResponse.model_validate(product).model_dump(), "success": True}), 201

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "view create product request validation"}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "success": False, "location": "view create product repo"}), 500