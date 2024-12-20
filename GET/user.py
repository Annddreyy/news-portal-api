from flask import Blueprint, jsonify
from db import get_connection

get_user_blueprint = Blueprint('user', __name__)

@get_user_blueprint.route('/api/v1/users', methods=['get'])
def get_users():
    global cur, con
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM user')

        users = cur.fetchall()
        
        users_json = []
        for user in users:
            users_json.append(
                {
                    'id': user[0],
                    'surname': user[1],
                    'name': user[2],
                    'patronymic': user[3],
                    'login': user[4],
                    'password': user[5],
                    'photo': user[6]
                }
            )
        return jsonify(users_json)

    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()


@get_user_blueprint.route('/api/v1/users/<int:user_id>', methods=['get'])
def get_user(user_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM user WHERE user_id={user_id}')

        user = cur.fetchone()

        if user:
            user_json = {
                'id': user[0],
                'surname': user[1],
                'name': user[2],
                'patronymic': user[3],
                'login': user[4],
                'password': user[5],
                'photo': user[6]
            }
            return jsonify(user_json)
        
        return {
            'status': 'error',
            'code': 404,
            'message': f'User with ID {user_id} not found'
        }

    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()
        
