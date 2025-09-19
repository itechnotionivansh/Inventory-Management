from app import create_app
from app.extensions import db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

# Only needed so Flask CLI can discover `app`
if __name__ == "__main__":
    app.run()
