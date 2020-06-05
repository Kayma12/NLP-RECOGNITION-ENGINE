from flask import Flask
from controller import blueprint as controller
import service

app = Flask(__name__, template_folder='./templates')
app.secret_key = "secretkey"

# register Blueprint
app.register_blueprint(controller)


# populate db
def populate():
    service.add_skills()
    service.add_consultant()


if __name__ == '__main__':
    populate()
    app.run(debug=True, use_reloader=False)
