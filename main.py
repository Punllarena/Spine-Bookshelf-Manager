from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
# from models import Base
from routes import home, search, volume_info

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap5(app)

# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# # Create the database tables
# with app.app_context():
#     db.create_all()

# # Register routes
# app.add_url_rule('/edit/<int:movie_id>', view_func=edit)
# app.add_url_rule('/delete/<int:movie_id>', view_func=delete)
app.add_url_rule('/volumeInfo/<string:volume_id>', view_func=volume_info)
app.add_url_rule('/search/<string:query>/page/<int:page>', 
                 view_func=search)
app.add_url_rule('/search/<string:query>', view_func=search, methods=['GET'])
# app.add_url_rule('/add/<int:tmdb_ID>', view_func=add)
app.add_url_rule('/', view_func=home)

if __name__ == '__main__':
    app.run(debug=True)