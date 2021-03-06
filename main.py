from flask import Flask, redirect, request, jsonify, make_response
from Proect.data import db_session
from Proect.data.Users import User
from Proect.data.Test_model import Test
from flask import render_template
from Proect.data.forms.RegisterForm import RegistForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Proect.data.forms.loginform import LoginForm
from Proect.data.resourses.user_resourses import UserListResource, UserResource
from Proect.data.resourses.questions_resource import TestListResource, TestResource
from Proect.data.forms.Delete_student_form import DeleteStudentForm
from flask_restful import Api
import random

app = Flask(__name__)


api = Api(app)
api.add_resource(UserResource, '/api/users/<string:login>')
api.add_resource(UserListResource, '/api/users/')
api.add_resource(TestListResource, '/api/tests/')
api.add_resource(TestResource, '/api/tests/<int:test_id>')
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
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            if user.is_teacher:
                return redirect("/user_teacher")
            else:
                return redirect("/user_student_entrance")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/user_teacher', methods=['GET', 'POST'])
def teacher_login():
    db_sess = db_session.create_session()
    sp = db_sess.query(User).filter(User.is_teacher == 0)
    return render_template('table_student.html', title='Таблица учеников', students=sp)


@app.route('/student_delete', methods=['POST', 'GET'])
@login_required
def student_delete():
    form = DeleteStudentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        student = db_sess.query(User).filter(User.login == form.login.data).first()
        if student and current_user.hashed_password == form.password.data:
            db_sess.delete(student)
            db_sess.commit()
            return redirect('/user_teacher')
        return render_template('Delete_student.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('Delete_student.html', title='удаление ученика', form=form)


@app.route('/student/app', methods=['POST', 'GET'])
@login_required
def student_app():
    form = RegistForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).get(form.login.data):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
                name=form.name.data,
                surname=form.surname.data,
                login=form.login.data,
                ball=0)
        user.hashed_password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/user_teacher')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/user_student_entrance")
def index():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    if user.ball == 0:
        return render_template("ready.html", user=user, ball=0)
    else:
        return render_template("ready.html", user=user, ball=int(user.ball))


@app.route('/user_student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        quest = db_sess.query(Test).all()
        user = db_sess.query(User).filter(User.login == current_user.login).first()
        sp = []
        sp_id = []
        sp_ans = []
        ch = 0
        while ch != 10:
            z = random.choice(quest)
            if z.id not in [i.id for i in sp]:
                s = z.answers_options.split('\n')
                sp_ans.append([])
                for i in s:
                    if i:
                        sp_ans[-1].append(i)
                sp.append(z)
                sp_id.append(str(z.id))
                ch += 1
        user.questions_id = ' '.join(sp_id)
        db_sess.commit()
        return render_template("Test_form.html", questions=sp, ans_opt=sp_ans)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == current_user.login).first()
        quest = db_sess.query(Test).all()
        ch = 0
        for i in quest:
            if str(i.id) in user.questions_id.split():
                if str(request.form.get(str(i.id))).split(')')[0] == i.answer:
                    ch += 1
        user.ball = ch
        db_sess.commit()
        return redirect("/user_student_entrance")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.db")
    '''user = User()
    user.name = 'Алексей'
    user.surname = 'Кузнецов'
    user.login = 'K1'
    user.password = user.set_password('qwerty1')
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
    user.password = user.set_password('qwerty1')
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
    user.password = user.set_password('qwerty1')
    user.is_teacher = True
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()'''
    app.run()


if __name__ == '__main__':
    main()
