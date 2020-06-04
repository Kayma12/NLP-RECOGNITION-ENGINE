from flask import Flask
from src.controller import blueprint as module_a
from src import database

app = Flask(__name__, template_folder='./templates')
app.secret_key = "secretkey"
database.add_consultant()

# register Blueprint
app.register_blueprint(module_a)


if __name__ == '__main__':
    app.run(debug=True)




