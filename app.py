from flask import Flask
from controller import blueprint as controller
import service
from database import mdb_client

app = Flask(__name__, template_folder='./templates')
app.secret_key = "secretkey"

# register Blueprint
app.register_blueprint(controller)


# populate db
def populate():
    service.add_skills()
    service.add_consultant()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    mdb_client.drop_database("test_database")
    populate()
    app.run(debug=True, use_reloader=False)
