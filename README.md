Tech Stack 🛠️
Framework: Flask

Database ORM: SQLAlchemy with Flask-SQLAlchemy

Authentication: Flask-JWT-Extended

Data Validation: Pydantic

Migrations: Flask-Migrate

Rate Limiting: Flask-Limiter

CORS: Flask-Cors


im-backend/
  .env
  .env.example
  manage.py
  requirements.txt
  run.py
  venv/                       # virtual environment included in the zip (contents omitted)
  app/
    __init__.py
    config.py
    extensions.py
    seed.py
    models/
      __init__.py
      user.py
      category.py
      product.py
      refresh_token.py
    blueprints/
      v1/
        auth.py
        categories.py
        health.py
        products.py
    schemas/
      auth_schemas.py
      category_schemas.py
      product_schemas.py
    services/
      auth_service.py
      category_service.py
      product_service.py
    utils/
      decorators.py
      error_handlers.py
  migrations/
    README
    alembic.ini
    env.py
    script.py.mako
    versions/
      072dfc0650ad_initial_migration_with_corrected_models.py
0



Repository Link
You can find the source code at the following GitHub repository:

backend:https://github.com/itechnotionivansh/Inventory-Management.git




Getting Started 🚀
Prerequisites
Python 3.8+

A running MySQL server

(Optional) A running Redis server for rate limiting

Setup Instructions
Clone the repository:

Bash

git clone <your-repository-url>
cd im-backend
Create and activate a virtual environment:

Bash

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
Install the dependencies:

Bash

pip install -r requirements.txt
Configure environment variables:

Copy the example .env.example file to a new .env file:

Bash

cp .env.example .env
Open the .env file and update the variables, especially DATABASE_URI, SECRET_KEY, and JWT_SECRET_KEY.

Set up the database:

Ensure you have created a database in MySQL that matches the one in your DATABASE_URI.

Run the database migrations to create all the tables:

Bash

flask db upgrade
Run the application:

Bash

python run.py
The API will be available at http://127.0.0.1:5000.