#Definir as rotas 
from flask import Blueprint, jsonify, request
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId

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

    if user_data.username == 'admin' and user_data.password == '123':
        return jsonify({"message":"Login bem-sucediso!"}),200
    else:
        return jsonify({"message":"Credenciais invalidas"}),401


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = []
    for product in products_cursor:
        product['_id'] = str(product['_id'])
        products_list.append(product)

    return jsonify(products_list)

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message":"Esta é a rota de criação de produto"})

# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try: 
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"}),400
    
    product = db.products.find_one({"_id": oid})

    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product),200
    else:
        return jsonify({"erro": f"Produto com o id: {product_id} - Não encontrado"}),404

# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message":f"Esta é a rota de atualizacao do produto com o id {product_id}"})

# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message":f"Esta é a rota de deleção do produto com o id {product_id}"})

# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message":"Esta é a rota de upload do arquivo de vendas"})

@main_bp.route('/')
def index():
    return jsonify({'message':'Bem vindo ao Stylesync!'})

