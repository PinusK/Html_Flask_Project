from flask_restful import abort, Resource
from Proect.data import db_session
from Proect.data.Users import User
from Proect.data.resourses.parser_users import parser
from flask import abort, jsonify


class UserResource(Resource):
    def get(self, login):

        abort_if_news_not_found(login)
        session = db_session.create_session()
        user = session.query(User).filter(User.login == login).first()
        return jsonify({'users': user.to_dict(
            only=('name', 'surname', 'login'))})

    def delete(self, login):
        abort_if_news_not_found(login)
        session = db_session.create_session()
        user = session.query(User).filter(User.login == login).first()
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('name', 'surname', 'login')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            login=args['login'],
            hashed_password=args['hashed_password'],
            klass=args['klass'],
            ball=0,
            is_teacher=0,
            questions_id=''
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(login):
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    if not user:
        abort(404, message=f"News {login} not found")
