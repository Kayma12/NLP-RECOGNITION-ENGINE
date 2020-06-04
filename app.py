from flask import Flask
from src.controller import blueprint as module_a

app = Flask(__name__, template_folder='./templates')
app.secret_key = "secretkey"

# register Blueprint
app.register_blueprint(module_a)

if __name__ == '__main__':
    app.run(debug=True)
