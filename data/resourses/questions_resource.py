from flask_restful import reqparse, abort, Api, Resource
from Proect.data import db_session
from Proect.data.Test_model import Test
from flask import abort, jsonify


class TestResource(Resource):
    def get(self, test_id):
        abort_if_news_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        return jsonify({'tests': test.to_dict(
            only=('question', 'answers_options', 'answer'))})


class TestListResource(Resource):
    def get(self):
        session = db_session.create_session()
        test = session.query(Test).all()
        return jsonify({'test': [item.to_dict(
            only=('question', 'answers_options', 'answer')) for item in test]})


def abort_if_news_not_found(test_id):
    session = db_session.create_session()
    test = session.query(Test).get(test_id)
    if not test:
        abort(404, message=f"News {test_id} not found")
