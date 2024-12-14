from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for
from app.models import db, Player
from app import admin
from colorich import printr
from app.blueprints.admin.models import UserAdmin


admin_page = Blueprint('admin_page', __name__)

printr(current_user, "red")
admin.add_view(UserAdmin(Player, db.session))
# if current_user.is_authenticated and current_user.rank == 'admin':
#     admin.add_view(UserAdmin(Player, db.session))
# else:
#     redirect(url_for('login_register.login'))