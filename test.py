from requests import get
from requests import post
from requests import delete

print(get('http://localhost:5000/api/users/K99').json())
print(delete('http://localhost:5000/api/users/K99').json())
print(get('http://localhost:5000/api/users/K1').json())

print(get('http://localhost:5000/api/users').json())
print(post('http://localhost:5000/api/users', json={}).json())
print(post('http://localhost:5000/api/users', json={'name': 'qwe'}).json())

print(get('http://localhost:5000/api/users').json())
print(post('http://localhost:5000/api/users', json={'id': 4,
                                                    'name': 'qwe',
                                                    'surname': 'asd',
                                                    'klass': 12,
                                                    'login': 'engener',
                                                    'hashed_password': 'qwerty1',
                                                    }).json())
print(get('http://localhost:5000/api/users').json())
print(delete('http://localhost:5000/api/users/engener').json())
print(get('http://localhost:5000/api/users').json())

print()
print()
print()

print(get('http://localhost:5000/api/tests').json())
print(get('http://localhost:5000/api/tests/1').json())
