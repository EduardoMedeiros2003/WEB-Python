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
from flask import render_template, redirect, url_for, session, flash

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que o usuário se autentique para obter um token
@main_bp.route('/login', methods=['GET', 'POST'])
def login():

    # 🔹 Se for GET → apenas renderiza a página
    if request.method == 'GET':
        return render_template("login.html")

    # 🔹 Se for POST → processa login
    try:
        # Se vier do formulário HTML
        if request.form:
            raw_data = request.form.to_dict()
        else:
            raw_data = request.get_json()

        user_data = LoginPayload(**raw_data)

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except Exception:
        return jsonify({"error": "Erro durante a requisição do dado"}), 500


    if user_data.username == 'admin' and user_data.password == 'supersecret':

        token = jwt.encode({
            "user_id": user_data.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256")

        # 🔹 Se for API → retorna JSON
        if request.is_json:
            return jsonify({'access_token': token}), 200

        # 🔹 Se for formulário HTML → cria sessão e redireciona
        session["user"] = user_data.username
        return redirect(url_for("main_bp.dashboard"))

    return jsonify({"message": "Credenciais invalidas"}), 401

@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():

    products = list(db.products.find())

    return render_template(
        "products.html",
        products=products,
        title="Produtos"
    )

#RF: O sistema deve mostar um formulario para criação de um novo dado 
@main_bp.route('/products/new', methods=['GET'])
def new_product():
    return render_template("add_product.html")

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products/new', methods=['POST'])
def create_product():

    try:
        data = request.form.to_dict()

        data["price"] = float(data["price"])
        data["stock"] = int(data["stock"])

        product = Product(**data)

        db.products.insert_one(product.model_dump())

        flash("Produto criado com sucesso!", "success")

        return redirect(url_for("main_bp.get_products"))

    except Exception as e:
        print(e)
        flash("Erro ao criar produto", "danger")
        return redirect(url_for("main_bp.new_product"))
    
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

#RF: o sistema vai abrir a aba de edição 
@main_bp.route('/products/edit/<string:product_id>', methods=['GET'])
def edit_product(product_id):

    product = db.products.find_one({"_id": ObjectId(product_id)})

    if not product:
        flash("Produto não encontrado", "danger")
        return redirect(url_for("main_bp.get_products"))

    return render_template("edit_product.html", product=product)

# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/products/edit/<string:product_id>', methods=['POST'])
def update_product(product_id):

    try:
        data = request.form.to_dict()

        data["price"] = float(data["price"])
        data["stock"] = int(data["stock"])

        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": data}
        )

        flash("Produto atualizado com sucesso!", "success")

        return redirect(url_for("main_bp.get_products"))

    except Exception as e:
        print(e)
        flash("Erro ao atualizar produto", "danger")
        return redirect(url_for("main_bp.get_products"))

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

