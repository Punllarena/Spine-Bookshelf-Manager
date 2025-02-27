from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import home, search, volume_info, upcoming, add, edit, delete, view_series

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshelf.db'
Bootstrap5(app)


# Initialize the database
# The database object is defined in models.py because it needs to have access to
# the class definitions of the models. The models.py file imports the db object
# and uses it to create the database tables.
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# # Register routes
app.add_url_rule('/edit/<string:volume_id>', view_func=edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<string:volume_id>', view_func=delete)
app.add_url_rule('/volumeInfo/<string:volume_id>', view_func=volume_info)
app.add_url_rule('/viewSeries/<string:series_id>', view_func=view_series)
app.add_url_rule('/search/page/<int:page>/', 
                 view_func=search, methods=['GET', 'POST'])
app.add_url_rule('/search/', view_func=search, methods=['GET', 'POST'])
app.add_url_rule('/add/<string:volume_id>?<string:shelf>', view_func=add)
app.add_url_rule('/', view_func=home)
app.add_url_rule('/upcoming', view_func=upcoming)

if __name__ == '__main__':
    app.run(debug=True)