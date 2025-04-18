from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.product import create_product_repo, get_product_detail_repo, get_products_list_repo, process_sustainability_repo, process_tags_repo
from schemas.product import ProductCreateRequest, ProductCreatedResponse, ProductDetailResponse, ProductListFilters, ProductListResponse

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
    

def list_products_view(request_args):
    try: 
        filtered_products_data_validated = ProductListFilters.model_validate(request_args.to_dict(flat=False))

        paginated_product = get_products_list_repo(filtered_products_data_validated, request_args)

        # serialize data
        products_response = [
            ProductListResponse.model_validate(product).model_dump() for product in paginated_product.items
        ]

        return jsonify({
            "success": True,
            "products": products_response,
            "pagination": {
                "total": paginated_product.total,
                "pages": paginated_product.pages,
                "current_page": paginated_product.page,
                "per_page": paginated_product.per_page
            }
        })
    
    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "view list products request validation"}), 400
    
    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "view list products repo"}), 500
    

def get_product_detail_view(product_id):
    try:
        product = get_product_detail_repo(product_id)

        serialized_product = ProductDetailResponse.model_validate(product).model_dump()
        
        return jsonify({"success": True, "product": serialized_product}), 200
    
    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "view get product detail data validation"}), 500

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "view get product detail repo"}), 500