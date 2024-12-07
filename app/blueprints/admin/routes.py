from flask_login import login_required, current_user
from flask import Blueprint, render_template
from app.models import db, Player, Game, Score
from app import admin
from flask_admin.contrib.sqla import ModelView


admin_page = Blueprint('admin_page', __name__)

admin.add_view(ModelView(Player, db.session))

# @admin_page.route("/admin", methods=["GET", "POST"])
# @login_required
# def admin_view():
    
#     return render_template("admin.html")
