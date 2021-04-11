from flask import Flask, redirect, request, abort, jsonify, make_response
from alhimik_work_class.data import db_session
from alhimik_work_class.data.Users import User
from alhimik_work_class.data.News import News
from alhimik_work_class.data.Jobs import Jobs
from flask import render_template
from alhimik_work_class.data.forms.registerform import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from alhimik_work_class.data.forms.loginform import LoginForm
from alhimik_work_class.data.forms.news_form import NewsForm
from alhimik_work_class.data.forms.jobs_Form import Jobs_Form
from alhimik_work_class.data.resourses import users_resource, news_resources, jobs_resource
import datetime
# from alhimik_work_class.data import news_api
# from alhimik_work_class.data import jobs_api
from flask_restful import reqparse, abort, Api, Resource
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('table.html')


def main():
    # db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
