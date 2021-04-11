from flask import Flask, redirect, request, abort, jsonify, make_response
from data import db_session
from data.Users import User
from data.Test_model import Test
from flask import render_template
# from Proect.data.forms.registerform import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.forms.loginform import LoginForm
from data.resourses.user_resourses import UserListResource, UserResource
from data.forms.Delete_student_form import DeleteStudentForm
# from Proect.data.forms.news_form import NewsForm
# from Proect.data.forms.jobs_Form import Jobs_Form
# from Proect.data.resourses import users_resource, news_resources, jobs_resource
import datetime
# from alhimik_work_class.data import news_api
# from alhimik_work_class.data import jobs_api
from flask_restful import reqparse, abort, Api, Resource
import random

app = Flask(__name__)


api = Api(app)
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserListResource, '/api/users/')
'''api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(news_resources.NewsListResource, '/api/v2/news')
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')'''
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.teacher:
                return redirect("/user_teacher")
            elif user.teacher:
                return redirect("/user_student")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/user_teacher', methods=['GET', 'POST'])
def login():
    db_sess = db_session.create_session()
    sp = db_sess.query(User).filter(User.is_teacher == 0)
    print(sp)
    # return render_template('table_student.html', title='Таблица учеников', students=sp)


''' @app.route('/student_delete', methods=['GET', 'POST'])
@login_required
def jobs_delete():
    form = DeleteStudentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        student = db_sess.query(User).filter(User.login == form.login.data).first()
        if student and current_user.check_password(form.password.data):
            db_sess.delete(student)
            db_sess.commit()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='удаление ученика', form=form)


@app.route('/student/app', methods=['GET', 'POST'])
@login_required
def student_app():
    form = RegistForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
                name=form.name.data,
                email=form.email.data,
        )
        //user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            modified_date=form.modified_date.data
        )//
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/user_teacher')'''
# return render_template('register.html', title='Регистрация', form=form)


@app.route("/user_student_entrance/<string:log>")
def index(log):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == log)
    if user.ball == 0:
        return render_template("ready.html", user=user, ball=0)
    else:
        return render_template("ready.html", user=user, ball=user.ball)


@app.route('/user_student/<string:log>', methods=['GET', 'POST'])
def student_login(log):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        quest = db_sess.query(Test).all()
        user = db_sess.query(User).filter(User.login == log)
        sp = []
        sp_id = []
        ch = 0
        while ch != 10:
            z = random.choice(quest)
            if z['id'] in [i[0] for i in sp]:
                sp.append(z)
                sp_id.append(str(z['id']))
                ch += 1
        user.questions_id = ' '.join(sp_id)
        db_sess.commit()
        return render_template("Test_form.html", qustions=sp)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == log)
        quest = db_sess.query(Test).all()
        ch = 0
        for i in quest:
            if i['id'] in user.qustions_id:
                if request.form[str(i['id'])] == i['otvet']:
                    ch += 1
        user.ball = ch
        db_sess.commit()
        return redirect(f"/user_student_entrance/{log}")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

'''
@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )'''


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.db")
    user = User()
    user.name = 'Алексей'
    user.surname = 'Кузнецов'
    user.login = 'K1'
    user.password = 'qwerty1'
    user.is_teacher = False
    user.ball = 0
    user.klass = 10
    user.questions_id = ''
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    user = User()
    user.name = 'Ярослав'
    user.surname = 'Рюрикович'
    user.login = 'K2'
    user.password = 'qwerty1'
    user.is_teacher = False
    user.ball = 0
    user.klass = 10
    user.questions_id = ''
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    user = User()
    user.name = 'Иван'
    user.surname = 'Кузнец'
    user.login = 'K3'
    user.password = 'qwerty1'
    user.is_teacher = True
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()
