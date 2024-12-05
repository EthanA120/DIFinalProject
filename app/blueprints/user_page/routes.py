from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, session


user_page = Blueprint('user_page', __name__)


@user_page.route("/user_page", methods=["GET", "POST"])
@login_required
def profile():
    
    return render_template('userPage/user_page.html')
