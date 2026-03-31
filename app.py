from flask import Flask
from extensions import mail
from routes.auth_routes import auth
from routes.admin_routes import admin
from routes.user_routes import user



app = Flask(__name__)
app.secret_key = "quiz_secret"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'quizwebsite2026@gmail.com'
app.config['MAIL_PASSWORD'] = 'zviy zssq rgli dwna'  # NOT normal password

 # 🔹 Initialize mail
mail.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
