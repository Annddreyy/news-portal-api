from flask import Blueprint, jsonify
from db import get_connection

get_news_blueprint = Blueprint('news', __name__)

@get_news_blueprint.route('/api/v1/news')
def get_news():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * from news')

        news = cur.fetchall()

        news_json = []
        for one_news in news:
            cur.execute(f'SELECT group_id, title, color FROM subgroup WHERE subgroup_id={one_news[4]}')
            subgroup = cur.fetchone()

            group_id = subgroup[0]
            subgroup_title = subgroup[1]

            cur.execute(f'SELECT title FROM group_of_news WHERE group_id={group_id}')
            group = cur.fetchone()[0]

            news_json.append(
                {
                    'id': one_news[0],
                    'author_id': one_news[1],
                    'author_role': one_news[5],
                    'title': one_news[2],
                    'group': group,
                    'subgroup': subgroup_title,
                    'text': one_news[3],
                    'video': one_news[6],
                    'poster': one_news[7],
                    'short_description': one_news[8],
                    'color': subgroup[2],
                    'date': one_news[9]
                }
            )
        
        return jsonify(news_json)

    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()


@get_news_blueprint.route('/api/v1/news/<int:news_id>')
def get_one_news(news_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM news WHERE news_id={news_id}')

        news = cur.fetchone()

        if news:
            cur.execute(f'SELECT group_id, title, color FROM subgroup WHERE subgroup_id={news[4]}')
            subgroup = cur.fetchone()

            group_id = subgroup[0]
            subgroup_title = subgroup[1]

            cur.execute(f'SELECT title FROM group_of_news WHERE group_id={group_id}')
            group = cur.fetchone()[0]

            news_json = {
                'id': news[0],
                'author_id': news[1],
                'author_role': news[5],
                'title': news[2],
                'group': group,
                'subgroup': subgroup_title,
                'text': news[3],
                'video': news[6],
                'poster': news[7],
                'short_description': news[8],
                'color': subgroup[2],
                'date': news[9]
            }

            return jsonify(news_json)
            
        return {
            'status': 'error',
            'code': 404,
            'message': f'News with ID {news_id} not found'
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