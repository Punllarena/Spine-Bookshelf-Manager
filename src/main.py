from flask import Flask
from flask_bootstrap import Bootstrap5

from models import db
from routes import home, search, volume_info, upcoming, add, edit, delete, view_series, full_shelf, shelf, timeline, settings
import os

instance_path = os.path.join(os.path.dirname(__file__), 'instance')

os.makedirs(instance_path, exist_ok=True)  # Ensure the folder exists
db_path = os.path.join(instance_path, 'bookshelf.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thishastobeeditedonproduction'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

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
app.add_url_rule('/shelf/<string:tag>?page=<int:page_num>', view_func=shelf)
app.add_url_rule('/full_shelf/<int:page_num>', view_func=full_shelf)
app.add_url_rule('/timeline', view_func=timeline)
app.add_url_rule('/edit/<string:volume_id>', view_func=edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<string:volume_id>', view_func=delete)
app.add_url_rule('/volumeInfo/<string:volume_id>', view_func=volume_info)
app.add_url_rule('/viewSeries/<string:series_id>', view_func=view_series)
app.add_url_rule('/search/page/<int:page>/', view_func=search, methods=['GET', 'POST'])
app.add_url_rule('/search/', view_func=search, methods=['GET', 'POST'])
app.add_url_rule('/add/<string:volume_id>?<string:shelf>', view_func=add)
app.add_url_rule('/settings', view_func=settings, methods=['GET', 'POST'])
app.add_url_rule('/upcoming', view_func=upcoming)
app.add_url_rule('/', view_func=home)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)