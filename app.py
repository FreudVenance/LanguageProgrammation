from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app=app)

# Configuration de mysql:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Programmation_Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    AUTHOR_NAME = db.Column(db.String(100), unique=True, nullable=False)
    AUTHOR_PROFILE = db.Column(db.String(500), unique=True, nullable=False)
    LOGO = db.Column(db.String(200), unique=True, nullable=False)
    FRAMEWORKS = db.relationship('Framework', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.NAME}', '{self.AUTHOR}')"
    
class Framework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    AUTHOR_NAME = db.Column(db.String(100), unique=True, nullable=False)
    AUTHOR_PROFILE = db.Column(db.String(500), unique=True, nullable=False)
    LOGO = db.Column(db.String(200), unique=True, nullable=False)
    PROGRAMMATION_LANGUAGE = db.Column(db.Integer, db.ForeignKey(Programmation_Language.id), nullable=True)

    def __repr__(self):
        return f"User('{self.NAME}', '{self.AUTHOR}')"

with app.app_context():
    db.create_all()

@app.route("/language/post", methods=["POST", "GET"])
def postLanguage():
    if request.method == "POST":
        NAME = request.form["NAME"]
        AUTHOR_NAME = request.form["AUTHOR_NAME"]
        AUTHOR_PROFILE = request.form["AUTHOR_PROFILE"]
        LOGO = request.form["LOGO"]

        db.session.add(Programmation_Language(
            NAME = NAME,
            AUTHOR_NAME = AUTHOR_NAME,
            AUTHOR_PROFILE = AUTHOR_PROFILE,
            LOGO = LOGO
        ))

        db.session.commit()
        return redirect(url_for('index')) 
    return render_template("postLanguage.html")

@app.route("/language/post/framework/", methods=["POST", "GET"])
def postLanguageFrameworks():
    if request.method == "POST":
        NAME = request.form["NAME"]
        AUTHOR_NAME = request.form["AUTHOR_NAME"]
        AUTHOR_PROFILE = request.form["AUTHOR_PROFILE"]
        LOGO = request.form["LOGO"]
        PROGRAMMATION_LANGUAGE_ID = request.form["PROGRAMMATION_LANGUAGE"]  # Utilisation de l'ID du langage de programmation

        # Trouver l'objet Programmation_Language avec l'ID
        programmation_language = Programmation_Language.query.get(PROGRAMMATION_LANGUAGE_ID)

        if programmation_language:  # Si un langage de programmation est trouvé
            db.session.add(Framework(
                NAME = NAME,
                AUTHOR_NAME = AUTHOR_NAME,
                AUTHOR_PROFILE = AUTHOR_PROFILE,
                LOGO = LOGO,
                PROGRAMMATION_LANGUAGE_ID = PROGRAMMATION_LANGUAGE_ID  # Associer l'ID de programmation
            ))
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('postFrameWork.html')
    return render_template("postFrameWork.html")

@app.route('/')
def index():
    LANGUAGES = Programmation_Language.query.all()
    return render_template('index.html', LANGUAGES=LANGUAGES)

@app.route("/user/<name>")
def user_name(name):
    return render_template("user.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/login/")
def login():
    return render_template(template_name_or_list="login.html")

if __name__=="__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)
