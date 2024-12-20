from flask import Flask

from GET.user import get_user_blueprint
from GET.news import get_news_blueprint

from POST.user import post_user_blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = '12foefwjf039423wd2808d'

app.register_blueprint(get_user_blueprint)
app.register_blueprint(get_news_blueprint)

app.register_blueprint(post_user_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=1234)