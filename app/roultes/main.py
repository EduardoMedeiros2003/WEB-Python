#Definir as rotas 
from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
from bson.errors import InvalidId
import csv
import os 
import io

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que o usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
       raw_data = request.get_json()
       user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error":e.errors()}), 400
    except Exception as e:
        return jsonify({"error":"Erro durante a requisição do dado"}), 500

    if user_data.username == 'admin' and user_data.password == 'supersecret':
        token = jwt.encode({
            "user_id": user_data.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)# tempo de expriração 
        }, 
        current_app.config['SECRET_KEY'], 
        algorithm="HS256")

        return jsonify({'access_token': token}),200
    
    return jsonify({"message":"Credenciais invalidas"}),401


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
  
    return jsonify(products_list)

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    try:
        product= Product(**request.get_json())
    except ValidationError as e:
        return jsonify({'erro':e.errors()}),400
    
    result = db.products.insert_one(product.model_dump())
    
    return jsonify({
        "message": "Produto pode ser criado",
        "usuario_autenticado": current_user["user_id"],
        "id": str(result.inserted_id)
    }),201

# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try: 
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"}),400
    
    product = db.products.find_one({"_id": oid})

    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model),200
    else:
        return jsonify({"erro": f"Produto com o id: {product_id} - Não encontrado"}),404

# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
        update_result = db.products.update_one(
            {"_id": oid},
            {"$set": update_data.model_dump(exclude_unset=True)}
        )
        if update_result.matched_count == 0:
            return jsonify({"error": "Produto não encontrado"}), 404
        updated_product = db.products.find_one({"_id": oid})
        return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()})
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400

def update_product(product_id):
    return jsonify({"message":f"Esta é a rota de atualizacao do produto com o id {product_id}"})

# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        delete_product = db.products.delete_one({"_id":oid})
        if delete_product.deleted_count == 0:
            return jsonify({"erro": "Produto não foi encontrado"}),404
        return "",204
    except Exception:
        return jsonify({"erro":f"id do produto inválido"}),400

# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token):
    if 'file' not in request.files:
        return jsonify({"erro":"Nenhum arquivo foi enviado"}),400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo foi selecionado"}),400
    
    if file and file.filename.endswith('.csv'):
        csv_stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.DictReader(csv_stream)

        sales_to_insert = []
        error =[]
        for row_num, row in enumerate(csv_reader, 1):
            try:
                from app.models.sale import Sale
                sale_data = Sale(**row)
                sales_to_insert.append(sale_data.model_dump())

            except ValidationError as e:
                error.append(f'Linha{row_num}: com dados inválidos - {e.errors()}')
            except Exception as e:
                error.append(f"Linha {row_num}: Erro inesperado ao processar a linha - {str(e)}")

        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return jsonify({"error":f"Erro ao inserir dados no banco:{str(e)}"}),500
            
            return jsonify({"message":"Upload realizado com sucesso.",
                            "vendas_importadas": len(sales_to_insert),
                            "erros_encontrados": error}),200

    return jsonify({"message":"Esta é a rota de upload do arquivo de vendas"})

@main_bp.route('/')
def index():
    return jsonify({'message':'Bem vindo ao Stylesync!'})

