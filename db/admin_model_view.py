from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from config.config import USER_ADMIN

class AdminModelView(ModelView):

    def is_accessible(self):
        if current_user.is_admin == True:
            return True
        else:
            return False


    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.login_page'))
