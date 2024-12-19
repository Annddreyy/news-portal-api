from flask import Blueprint, jsonify, request
from db import get_connection
import base64

post_user_blueprint = Blueprint('post_user', __name__)

@post_user_blueprint.route('/api/v1/users', methods=['POST'])
def post_user():
    conn = get_connection()
    cur = conn.cursor()

    user = request.get_json()

    surname = user['surname']
    name = user['name']
    patronymic = user['patronymic']

    login = user['login']
    password = user['password']

    image = user['photo']

    cur.execute('INSERT INTO user(surname, name, patronymic, login, password, photo) ' +
                f"VALUES('{surname}', '{name}', '{patronymic}', '{login}', '{password}', '{image}')")
                
    conn.commit()

    cur.execute(f"SELECT user_id FROM user WHERE login='{login}' AND password='{password}'")
    user_id = int(cur.fetchone()[0])

    cur.close()
    conn.close()

    return {
        'status': 'ok',
        'id': user_id
    }
