# Product Management System (Flask + MongoDB)

A full-stack web application for **product management**, built with **Python, Flask, and MongoDB**.
This project demonstrates backend development concepts such as **RESTful architecture, authentication, CRUD operations, modular code structure, and automated testing**.

The application allows authenticated users to manage a product inventory through a web interface.

---

# 🚀 Project Goals

This project was developed to practice and demonstrate:

* Backend development with Python and Flask
* Database integration with MongoDB
* Authentication using JWT
* CRUD operations (Create, Read, Update, Delete)
* Clean project architecture
* Automated testing with pytest
* Version control with Git and Conventional Commits

It serves as a **portfolio project showcasing practical backend engineering skills**.

---

# 🧠 Features

✔ User authentication system
✔ JWT token generation
✔ Product creation
✔ Product listing
✔ Product editing
✔ Product deletion
✔ Currency formatting utility
✔ Unit testing with pytest
✔ Modular Flask architecture

---

# 🛠 Tech Stack

## Backend

* Python
* Flask
* PyMongo
* JWT Authentication

## Database

* MongoDB

## Frontend

* HTML
* Bootstrap
* Jinja2 Templates

## Testing

* Pytest

## Tools

* Git
* GitHub
* Virtual Environments (venv)

---

# 📂 Project Structure

```
project/
│
├── app/
│   ├── routes/
│   │   └── main.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── products.html
│   │   ├── add_product.html
│   │   └── edit_product.html
│   │
│   ├── utils.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   └── test_utils.py
│
├── config.py
├── requirements.txt
└── run.py
```

This modular structure separates **application logic, templates, utilities, and tests**, improving maintainability and scalability.

---

# ⚙️ Installation

Clone the repository:

```
git clone https://github.com/your-username/your-repository.git
```

Enter the project directory:

```
cd your-repository
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment:

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶ Running the Application

Start the Flask server:

```
python run.py
```

The application will run at:

```
http://127.0.0.1:5000
```

---

# 🔐 Authentication

The system includes a login endpoint that returns a **JWT token** used to authenticate protected routes.

Example credentials for testing:

```
username: admin
password: supersecret
```

---

# 📦 Example Product (MongoDB)

```
{
  "name": "Gaming Mouse",
  "description": "High precision gaming mouse",
  "price": 249.90,
  "stock": 120
}
```

---

# 🧪 Automated Tests

This project includes unit tests using **pytest**.

Run tests with:

```
pytest
```

Example output:

```
3 passed
```

The tests validate the **currency formatting utility**, ensuring consistent output formatting.

---

# 🧩 Utility Functions

The project includes reusable helper functions such as:

```
format_currency()
```

This function standardizes currency formatting across the application.

Example:

```
format_currency(59.9)
```

Output:

```
59,90
```

---

# 📈 Skills Demonstrated

This project highlights practical experience with:

* Backend development with Flask
* RESTful design concepts
* MongoDB database operations
* Authentication with JWT
* CRUD system design
* Python project structure
* Automated testing with pytest
* Git version control and commit standards

---

# 📷 Application Preview

You can add screenshots or GIFs here to demonstrate:

* login page
* product dashboard
* product creation
* product editing

---

# 👨‍💻 Author

Eduardo Medeiros

Backend developer in training focused on **Python development and web applications**.

Currently building projects to strengthen knowledge in:

* Backend architecture
* API development
* Software engineering practices

-------------------------------------PORTUGUÊS-----------------------------------------

# Sistema de Gerenciamento de Produtos (Flask + MongoDB)

Uma aplicação web completa para **gerenciamento de produtos**, desenvolvida com **Python, Flask e MongoDB**.

Este projeto demonstra conceitos importantes de desenvolvimento backend como **arquitetura REST, autenticação, operações CRUD, organização modular do código e testes automatizados**.

A aplicação permite que usuários autenticados gerenciem um inventário de produtos através de uma interface web.

---

# 🚀 Objetivos do Projeto

Este projeto foi desenvolvido para praticar e demonstrar:

* Desenvolvimento backend com Python e Flask
* Integração com banco de dados MongoDB
* Autenticação utilizando JWT
* Operações CRUD (Criar, Ler, Atualizar, Deletar)
* Arquitetura organizada de projeto
* Testes automatizados com pytest
* Versionamento de código com Git e Conventional Commits

Ele funciona como um **projeto de portfólio para demonstrar habilidades reais de desenvolvimento backend**.

---

# 🧠 Funcionalidades

✔ Sistema de autenticação de usuário
✔ Geração de token JWT
✔ Criação de produtos
✔ Listagem de produtos
✔ Edição de produtos
✔ Exclusão de produtos
✔ Função utilitária para formatação de moeda
✔ Testes automatizados com pytest
✔ Arquitetura modular com Flask

---

# 🛠 Tecnologias Utilizadas

## Backend

* Python
* Flask
* PyMongo
* Autenticação com JWT

## Banco de Dados

* MongoDB

## Frontend

* HTML
* Bootstrap
* Templates Jinja2

## Testes

* Pytest

## Ferramentas

* Git
* GitHub
* Ambiente virtual Python (venv)

---

# 📂 Estrutura do Projeto

```id="ctz3jo"
project/
│
├── app/
│   ├── routes/
│   │   └── main.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── products.html
│   │   ├── add_product.html
│   │   └── edit_product.html
│   │
│   ├── utils.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   └── test_utils.py
│
├── config.py
├── requirements.txt
└── run.py
```

Essa estrutura modular separa **lógica da aplicação, templates, utilidades e testes**, facilitando manutenção e evolução do projeto.

---

# ⚙️ Instalação

Clone o repositório:

```id="qjn29r"
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Entre na pasta do projeto:

```id="cb86x8"
cd seu-repositorio
```

Crie um ambiente virtual:

```id="h19w3n"
python -m venv venv
```

Ative o ambiente virtual:

Windows

```id="cv5gb3"
venv\Scripts\activate
```

Instale as dependências:

```id="ntiu3r"
pip install -r requirements.txt
```

---

# ▶ Executando a Aplicação

Inicie o servidor Flask:

```id="qnjc7q"
python run.py
```

A aplicação estará disponível em:

```id="m6m8l8"
http://127.0.0.1:5000
```

---

# 🔐 Autenticação

O sistema possui uma rota de login que retorna um **token JWT**, utilizado para autenticar rotas protegidas.

Credenciais de teste:

```id="f1uk2a"
username: admin
password: supersecret
```

---

# 📦 Exemplo de Produto no MongoDB

```id="mmszua"
{
  "name": "Mouse Gamer",
  "description": "Mouse gamer de alta precisão",
  "price": 249.90,
  "stock": 120
}
```

---

# 🧪 Testes Automatizados

O projeto possui testes automatizados utilizando **pytest**.

Execute os testes com:

```id="03hryr"
pytest
```

Saída esperada:

```id="1c8vj5"
3 passed
```

Os testes validam a função de **formatação de moeda**, garantindo consistência na saída.

---

# 🧩 Funções Utilitárias

O projeto inclui funções reutilizáveis como:

```id="t7x4x6"
format_currency()
```

Essa função padroniza a formatação de valores monetários na aplicação.

Exemplo:

```id="ohh9x3"
format_currency(59.9)
```

Saída:

```id="j6tnqj"
59,90
```

---

# 📈 Competências Demonstradas

Este projeto demonstra experiência prática com:

* Desenvolvimento backend com Flask
* Conceitos de arquitetura REST
* Operações com banco de dados MongoDB
* Autenticação com JWT
* Design de sistemas CRUD
* Estruturação de projetos em Python
* Testes automatizados com pytest
* Versionamento de código com Git

---

# 📷 Demonstração da Aplicação

Aqui podem ser adicionadas imagens ou GIFs mostrando:

* tela de login
* painel de produtos
* criação de produto
* edição de produto

---

# 👨‍💻 Autor

Eduardo Medeiros

Desenvolvedor em formação focado em **desenvolvimento backend com Python**.

Atualmente desenvolvendo projetos para fortalecer conhecimentos em:

* arquitetura backend
* desenvolvimento de APIs
* boas práticas de engenharia de software

---

# 📄 Licença

portfólio profissional**.
