from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from colorich import printr
import argon2

class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.rank == 'admin'

    def inaccessible_callback(self, *args, **kwargs):
        return redirect(url_for('login_register.login')) # Redirect to login page

# Create a custom view that inherits from ModelView and implements login_required
class UserAdmin(ModelView):
    column_list = ('username', 'email', 'password', 'rank')  # Columns to display in the list view
    form_columns = ('username', 'email', 'password', 'rank')  # Editable columns in the form
    column_searchable_list = ('username', 'email')  # Allow searching by these columns
    column_filters = ('username', 'email', 'rank') # Allow filtering by these columns
    column_editable_list = ('username', 'email')  # Allow quick editing of these

    ph = argon2.PasswordHasher()  # Initialize Argon2 hasher ONCE

    def on_model_change(self, form, model, is_created):
        if 'password' in form.data and form.data['password']:
            hashed_password = self.ph.hash(form.data['password']) # Use the pre-initialized hasher
            model.password = hashed_password

    def on_form_prefill(self, form, id):
        # Prevent the password from being displayed when editing
        form.password.data  = ""
        
    def is_accessible(self):
        return current_user.is_authenticated and current_user.rank == 'admin'

    def inaccessible_callback(self, *args, **kwargs):
        return redirect(url_for('login_register.login')) # Redirect to login page
