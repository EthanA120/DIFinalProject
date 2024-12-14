from flask import Flask
from app.config import Config, metadata
from flask_migrate import Migrate
from flask_admin import Admin
from app.blueprints.admin.models import AdminIndex
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# from flask_ngrok import run_with_ngrok


app = Flask(__name__, template_folder='templates', static_folder='static')
# run_with_ngrok(app, '296WTGEAyc728DZUXkdEpIQ4S2x_7Q7q7KVMNfKkaqAJyvb5f')

app.config.from_object(Config)
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, name="Admin", index_view=AdminIndex())

login_mngr = LoginManager(app)
login_mngr.login_view = 'login_register.login'

mail = Mail(app)

from app import routes
from app.blueprints.admin.routes import admin_page
from app.blueprints.login_register.routes import login_register
from app.blueprints.user_page.routes import user_page
from app.blueprints.tic_tac_toe.routes import tic_tac_toe
from app.blueprints.blackjack.routes import blackjack

app.register_blueprint(admin_page)
app.register_blueprint(login_register)
app.register_blueprint(user_page)
app.register_blueprint(tic_tac_toe)
app.register_blueprint(blackjack)

# Final
